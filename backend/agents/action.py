def take_action(decision):
    try:
        if not decision or "⚠️" in decision:
            raise Exception("Invalid decision")

        return {
            "action_type": "irrigation",
            "priority": "medium",
            "steps": [
                {
                    "command": "Start irrigation",
                    "parameters": {
                        "duration_minutes": 20,
                        "zone": "Field A"
                    }
                }
            ]
        }

    except Exception as e:
        print("Action error:", e)

        return {
            "action_type": "manual_check",
            "priority": "low",
            "steps": [
                {
                    "command": "Inspect field manually",
                    "parameters": {}
                }
            ]
        }
