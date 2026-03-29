from services.llm import generate_response

def monitor_conditions(context):

    prompt = f"""
        You are a Monitoring Agent.

        Context:
        {context}

        Output rules:

        Soil Moisture:
        - >70% STOP irrigation
        - <40% INCREASE irrigation

        Temperature:
        - >35°C increase watering

        Nutrient Level:
        - Low → apply fertilizer
        - Optimal → maintain
        - High → stop fertilization

        Keep it structured and short.
        """
    return generate_response(prompt)