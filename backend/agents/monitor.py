from llm import generate_response


def monitor_conditions(context: dict) -> str:
    """
    Generate monitoring thresholds and alerts based on current conditions.
    """
    prompt = f"""
You are a Monitoring Agent for a smart farming system.

Current Conditions:
- Temperature: {context['weather']['temperature']}°C
- Humidity: {context['weather']['humidity']}%
- Condition: {context['weather']['condition']}
- Water Stress Index: {context.get('wsi', 'N/A')} ({context.get('wsi_level', 'Unknown')} stress)

Apply these rules:
- Soil Moisture >70%: STOP irrigation
- Soil Moisture <40%: INCREASE irrigation
- Temperature >35°C: increase watering frequency
- Nutrient Low: apply fertilizer | Optimal: maintain | High: stop fertilization

Output a short, structured monitoring report with thresholds and recommended actions.
"""
    result = generate_response(prompt)
    if not result:
        return "⚠️ Monitor temperature and humidity every 6 hours. Maintain soil moisture between 40–70%."
    return result