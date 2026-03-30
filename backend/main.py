from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    # Frontend should send ONE of these:
    lat: Optional[float] = None      # GPS latitude
    lon: Optional[float] = None      # GPS longitude
    city: Optional[str] = None       # City name typed by user


# ---------------------------
# 🌦 WEATHER AGENT (Open-Meteo — free, no API key)
# ---------------------------

# WMO weather code → human-readable condition
WMO_CONDITIONS = {
    0: "Clear", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy Fog",
    51: "Light Drizzle", 53: "Drizzle", 55: "Heavy Drizzle",
    61: "Light Rain", 63: "Rain", 65: "Heavy Rain",
    71: "Light Snow", 73: "Snow", 75: "Heavy Snow",
    80: "Showers", 81: "Rain Showers", 82: "Heavy Showers",
    95: "Thunderstorm", 96: "Thunderstorm with Hail", 99: "Heavy Thunderstorm",
}

# Default coords: Nashik, Maharashtra
NASHIK_LAT, NASHIK_LON = 19.9975, 73.7898


def _geocode_city(city: str) -> tuple[float, float, str] | None:
    """Convert city name → (lat, lon, display_name) using Open-Meteo geocoding."""
    try:
        res = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json",
            timeout=5
        )
        results = res.json().get("results", [])
        if not results:
            return None
        r = results[0]
        return r["latitude"], r["longitude"], r.get("name", city.title())
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None


def _fetch_open_meteo(lat: float, lon: float) -> dict:
    """Call Open-Meteo current weather endpoint."""
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,weathercode"
        f"&timezone=auto"
    )
    res = requests.get(url, timeout=5)
    data = res.json()
    current = data["current"]
    code = current.get("weathercode", 0)
    return {
        "temp": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "condition": WMO_CONDITIONS.get(code, "Unknown")
    }


def get_weather(lat: float = None, lon: float = None, city: str = None) -> tuple[dict | None, str]:
    """
    Fetch weather via Open-Meteo (free, no API key required).
    Priority: GPS coords → city name → fallback Nashik.
    Returns (weather_dict, location_label).
    """
    # Priority 1: GPS coordinates from frontend
    if lat is not None and lon is not None:
        try:
            weather = _fetch_open_meteo(lat, lon)
            return weather, "Your Location"
        except Exception as e:
            print(f"Weather (coords) error: {e}")

    # Priority 2: City name typed by user
    if city:
        try:
            geocoded = _geocode_city(city)
            if geocoded:
                c_lat, c_lon, display_name = geocoded
                weather = _fetch_open_meteo(c_lat, c_lon)
                return weather, display_name
        except Exception as e:
            print(f"Weather (city) error: {e}")

    # Priority 3: Default to Nashik
    try:
        weather = _fetch_open_meteo(NASHIK_LAT, NASHIK_LON)
        return weather, "Nashik (default)"
    except Exception as e:
        print(f"Weather fallback also failed: {e}")
        return None, "Unknown"


# ---------------------------
# 📊 WSI CALCULATION
# ---------------------------
def calculate_wsi(temp: float, humidity: float) -> float:
    try:
        wsi = (temp / 50) * (1 - humidity / 100)
        return round(max(0.0, min(1.0, wsi)), 2)
    except Exception:
        return None


def interpret_wsi(wsi: float) -> str:
    if wsi is None:
        return "Unknown"
    if wsi < 0.2:
        return "Low"
    elif wsi < 0.4:
        return "Moderate"
    elif wsi < 0.6:
        return "High"
    else:
        return "Critical"


# ---------------------------
# 🧠 DECISION AGENT (GROQ)
# ---------------------------
def decision_agent(query: str, weather: dict, wsi: float, wsi_level: str, location: str) -> str:
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise Exception("No GROQ_API_KEY set")

        prompt = f"""
You are an agricultural AI assistant helping farmers in India.

User Query: {query}

Location: {location}

Current Weather:
- Temperature: {weather['temp']}°C
- Humidity: {weather['humidity']}%
- Condition: {weather['condition']}

Water Stress Index (WSI): {wsi} ({wsi_level} stress)

Respond in EXACTLY this format (use these exact headings):

Decision:
[1-2 sentences on what the farmer should do]

Action:
[Specific steps: what, how much, when]

Monitoring:
[What to watch for and thresholds]

Verification:
[How to confirm the action worked]
"""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4
        }

        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=15
        )
        data = res.json()

        if "choices" not in data:
            raise Exception(f"Groq error: {data}")

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"LLM Error: {e}")
        return None


# ---------------------------
# 🔄 PARSER
# ---------------------------
def parse_response(text: str) -> dict | None:
    try:
        sections = {
            "decision": "",
            "action": "",
            "monitoring": "",
            "verification": ""
        }

        parts = text.replace("**", "")
        keys = ["Decision", "Action", "Monitoring", "Verification"]

        for i, key in enumerate(keys):
            lower_key = key.lower()
            try:
                start = parts.lower().index(f"{lower_key}:") + len(key) + 1
                if i + 1 < len(keys):
                    next_key = keys[i + 1]
                    end = parts.lower().index(f"{next_key.lower()}:")
                    sections[lower_key] = parts[start:end].strip()
                else:
                    sections[lower_key] = parts[start:].strip()
            except ValueError:
                sections[lower_key] = "Not available"

        if all(v in ("", "Not available") for v in sections.values()):
            return None

        return sections

    except Exception as e:
        print(f"Parse error: {e}")
        return None


# ---------------------------
# 🚀 MAIN ROUTE
# ---------------------------
@app.post("/chat")
def chat(req: ChatRequest):
    # Fetch weather using whichever location info was provided
    weather, location_label = get_weather(
        lat=req.lat,
        lon=req.lon,
        city=req.city
    )

    if not weather:
        return fallback_response(location="Unknown")

    wsi = calculate_wsi(weather["temp"], weather["humidity"])
    wsi_level = interpret_wsi(wsi)

    ai_output = decision_agent(req.message, weather, wsi, wsi_level, location_label)

    if not ai_output:
        return fallback_response(weather, wsi, wsi_level, location_label)

    parsed = parse_response(ai_output)

    if not parsed:
        return {
            "decision": ai_output,
            "action": "See decision above",
            "monitoring": "Monitor temperature and soil moisture daily",
            "verification": "Inspect crop health after 48 hours",
            "weather": weather,
            "wsi": wsi,
            "wsi_level": wsi_level,
            "location": location_label
        }

    return {
        **parsed,
        "weather": weather,
        "wsi": wsi,
        "wsi_level": wsi_level,
        "location": location_label
    }


# ---------------------------
# 🌍 LOCATION CHECK ROUTE
# ---------------------------
@app.get("/location-required")
def location_required():
    """
    Frontend can call this to know whether to prompt user for location.
    Always returns True — location is always needed for accurate advice.
    """
    return {"required": True, "message": "Please share your location for accurate weather data."}


# ---------------------------
# 🛡 FALLBACK
# ---------------------------
def fallback_response(weather=None, wsi=None, wsi_level=None, location="Unknown"):
    return {
        "decision": "Irrigation is recommended based on typical seasonal conditions.",
        "action": "Irrigate the field for 20–25 minutes. Prefer early morning (5–7 AM) to reduce evaporation.",
        "monitoring": "Check soil moisture every 6 hours. Stop irrigation if moisture exceeds 70%.",
        "verification": "Inspect plant leaves for wilting after 24 hours. Healthy leaves indicate sufficient water.",
        "weather": weather or {"temp": 30, "humidity": 60, "condition": "Clear"},
        "wsi": wsi or 0.3,
        "wsi_level": wsi_level or "Moderate",
        "location": location
    }


# ---------------------------
# ❤️ HEALTH CHECK
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}