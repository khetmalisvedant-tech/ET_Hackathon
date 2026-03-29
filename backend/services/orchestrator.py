from agents.decision import make_decision
from agents.action import take_action
from agents.monitor import monitor_conditions
from agents.verification import verify_output
from services.weather import get_weather_by_coords
from services.date import get_month


def calculate_wsi(temp, humidity):
    try:
        return round(temp - (humidity / 5), 2)
    except:
        return None


def interpret_wsi(wsi):
    if wsi is None:
        return "unknown"
    if wsi < 15:
        return "Low"
    elif wsi <= 25:
        return "Medium"
    else:
        return "High"


def run_workflow(user_input, location=None):

    logs = []

    # 🌍 Weather
    if location:
        logs.append("Fetching real-time weather data...")
        weather = get_weather_by_coords(location["lat"], location["lon"])
        city = "Detected Location"
    else:
        logs.append("Using fallback weather data...")
        weather = {
            "temperature": 30,
            "humidity": 60,
            "condition": "unknown"
        }
        city = "Unknown"

    month = get_month()

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

    # 🧠 Agents
    logs.append("Decision Agent running...")
    decision = make_decision(context, user_input)

    logs.append("Action Agent generating plan...")
    action = take_action(decision)

    logs.append("Monitoring Agent setting thresholds...")
    monitor = monitor_conditions(context)

    logs.append("Verification Agent validating output...")
    verification = verify_output(action)

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