from weather import get_weather_by_coords, get_weather
from date import get_month
from decision import make_decision
from action import take_action
from monitor import monitor_conditions
from verification import verify_output


def calculate_wsi(temp: float, humidity: float) -> float:
    """Water Stress Index: 0 = no stress, 1 = critical stress."""
    try:
        wsi = (temp / 50) * (1 - humidity / 100)
        return round(max(0.0, min(1.0, wsi)), 2)
    except Exception:
        return None


def interpret_wsi(wsi: float) -> str:
    """Human-readable stress level from WSI value."""
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


def run_workflow(user_input: str, location: dict = None) -> dict:
    """
    Run the full multi-agent workflow.
    location: optional dict with 'lat' and 'lon' keys
    """
    logs = []

    # 🌍 Weather
    weather = None
    city = "Unknown"
    try:
        if location and "lat" in location and "lon" in location:
            logs.append("Fetching real-time weather by GPS coordinates...")
            raw = get_weather_by_coords(location["lat"], location["lon"])
            if raw:
                # Normalise key names from coords response
                weather = {
                    "temperature": raw.get("temperature", raw.get("temp", 30)),
                    "humidity": raw.get("humidity", 60),
                    "condition": raw.get("condition", "Unknown")
                }
                city = "Detected Location"
        if not weather:
            raise Exception("No GPS or coord fetch failed")
    except Exception:
        logs.append("Falling back to city-based weather (Nashik)...")
        raw = get_weather("Nashik")
        weather = {
            "temperature": raw.get("temp", 30),
            "humidity": raw.get("humidity", 60),
            "condition": raw.get("condition", "Unknown")
        }
        city = "Nashik"

    # 📅 Month
    try:
        month = get_month()
    except Exception:
        month = "Unknown"

    # 📊 WSI
    logs.append("Calculating Water Stress Index (WSI)...")
    wsi = calculate_wsi(weather["temperature"], weather["humidity"])
    wsi_level = interpret_wsi(wsi)

    context = {
        "location": city,
        "weather": weather,
        "month": month,
        "wsi": wsi,
        "wsi_level": wsi_level
    }

    # 🧠 Decision
    logs.append("Decision Agent analysing conditions...")
    try:
        decision = make_decision(context, user_input)
    except Exception as e:
        logs.append(f"Decision agent error: {e}")
        decision = "⚠️ Unable to generate decision. Please try again."

    # ⚙️ Action
    logs.append("Action Agent generating plan...")
    try:
        action = take_action(decision)
    except Exception as e:
        logs.append(f"Action agent error: {e}")
        action = {"error": "Action generation failed"}

    # 📊 Monitor
    logs.append("Monitoring Agent setting thresholds...")
    try:
        monitor = monitor_conditions(context)
    except Exception as e:
        logs.append(f"Monitoring agent error: {e}")
        monitor = "⚠️ Monitoring unavailable. Check conditions manually."

    # ✅ Verification
    logs.append("Verification Agent validating output...")
    try:
        verification = verify_output(action)
    except Exception as e:
        logs.append(f"Verification agent error: {e}")
        verification = "⚠️ Verification unavailable."

    logs.append("✅ Workflow complete")

    return {
        "decision": decision,
        "action": action,
        "monitor": monitor,
        "verification": verification,
        "logs": logs,
        "weather": weather,
        "location": city,
        "wsi": wsi,
        "wsi_level": wsi_level
    }