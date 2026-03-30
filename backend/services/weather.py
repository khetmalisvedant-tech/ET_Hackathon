import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(lat=19.99, lon=73.79, city=None):
    """Open-Meteo — free, no API key required."""
    try:
        # If city given, geocode it first
        if city:
            geo = requests.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1",
                timeout=5
            ).json()
            if geo.get("results"):
                lat = geo["results"][0]["latitude"]
                lon = geo["results"][0]["longitude"]

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,weathercode"
        )
        data = requests.get(url, timeout=5).json()
        current = data["current"]
        return {
            "temp": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "condition": "Clear" if current["weathercode"] == 0 else "Cloudy"
        }, "Detected Location"
    except Exception as e:
        print(f"Weather error: {e}")
        return None, "Unknown"