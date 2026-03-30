from llm import generate_response


def make_decision(context: dict, user_input: str) -> str:
    """
    Use LLM to generate a farming decision based on context and user query.
    Falls back to a rule-based response if LLM fails.
    """
    try:
        prompt = f"""
You are an agricultural expert AI helping Indian farmers.

Context:
- Location: {context.get('location', 'Unknown')}
- Temperature: {context['weather']['temperature']}°C
- Humidity: {context['weather']['humidity']}%
- Condition: {context['weather']['condition']}
- Month: {context.get('month', 'Unknown')}
- Water Stress Index: {context.get('wsi', 'N/A')} ({context.get('wsi_level', 'Unknown')} stress)

User Query:
{user_input}

Give a clear, actionable farming decision in 2-3 sentences.
"""
        response = generate_response(prompt)

        if not response or len(response.strip()) < 10:
            raise Exception("Empty or too-short LLM response")

        return response

    except Exception as e:
        print(f"Decision error: {e}")
        temp = context.get('weather', {}).get('temperature', 'N/A')
        humidity = context.get('weather', {}).get('humidity', 'N/A')
        return (
            f"Based on current conditions (Temp: {temp}°C, Humidity: {humidity}%), "
            "irrigation is recommended. Monitor soil moisture regularly."
        )