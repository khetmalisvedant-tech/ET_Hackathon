def take_action(decision: str) -> dict:
    """
    Generate an action plan from the decision text.
    Returns a structured dict with action_type, priority, and steps.
    """
    try:
        if not decision or "⚠️" in decision or len(decision.strip()) < 10:
            raise ValueError("Invalid or empty decision")

        # Derive priority from decision keywords
        decision_lower = decision.lower()
        if any(kw in decision_lower for kw in ["urgent", "critical", "immediately", "high stress"]):
            priority = "high"
            duration = 30
        elif any(kw in decision_lower for kw in ["moderate", "medium", "recommended"]):
            priority = "medium"
            duration = 20
        else:
            priority = "low"
            duration = 15

        return {
            "action_type": "irrigation",
            "priority": priority,
            "steps": [
                {
                    "command": "Start drip/sprinkler irrigation",
                    "parameters": {
                        "duration_minutes": duration,
                        "zone": "Field A",
                        "best_time": "5:00 AM – 7:00 AM"
                    }
                },
                {
                    "command": "Record soil moisture after irrigation",
                    "parameters": {
                        "target_moisture": "50–65%"
                    }
                }
            ]
        }

    except Exception as e:
        print(f"Action error: {e}")
        return {
            "action_type": "manual_check",
            "priority": "low",
            "steps": [
                {
                    "command": "Inspect field manually",
                    "parameters": {
                        "note": "Automated plan unavailable — check soil moisture visually."
                    }
                }
            ]
        }