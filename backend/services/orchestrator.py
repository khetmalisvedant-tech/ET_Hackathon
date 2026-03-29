def run_workflow(user_input, location=None):

    logs = []

    # 🌍 Weather
    try:
        if location:
            logs.append("Fetching real-time weather data...")
            weather = get_weather_by_coords(location["lat"], location["lon"])
            city = "Detected Location"
        else:
            raise Exception("No location")
    except Exception as e:
        logs.append("Weather fallback used")
        weather = {
            "temperature": 30,
            "humidity": 60,
            "condition": "unknown"
        }
        city = "Unknown"

    # 📅 Month
    try:
        month = get_month()
    except:
        month = "Unknown"

    # 📊 WSI
    logs.append("Calculating Water Stress Index (WSI)...")
    try:
        wsi = calculate_wsi(weather["temperature"], weather["humidity"])
        wsi_level = interpret_wsi(wsi)
    except:
        wsi = None
        wsi_level = "Unknown"

    context = {
        "location": city,
        "weather": weather,
        "month": month,
        "wsi": wsi,
        "wsi_level": wsi_level
    }

    # 🧠 Decision
    logs.append("Decision Agent running...")
    try:
        decision = make_decision(context, user_input)
    except Exception as e:
        logs.append("Decision agent failed")
        decision = "⚠️ Unable to generate decision"

    # ⚙️ Action
    logs.append("Action Agent generating plan...")
    try:
        action = take_action(decision)
    except Exception as e:
        logs.append("Action agent failed")
        action = {"error": "Action generation failed"}

    # 📊 Monitor
    logs.append("Monitoring Agent setting thresholds...")
    try:
        monitor = monitor_conditions(context)
    except Exception as e:
        logs.append("Monitoring agent failed")
        monitor = "⚠️ Monitoring unavailable"

    # ✅ Verification
    logs.append("Verification Agent validating output...")
    try:
        verification = verify_output(action)
    except Exception as e:
        logs.append("Verification agent failed")
        verification = "⚠️ Verification unavailable"

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
