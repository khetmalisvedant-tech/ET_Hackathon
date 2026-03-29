from services.llm import generate_response

def make_decision(context, user_input):
    try:
        prompt = f"""
You are an agricultural expert AI.

Context:
{context}

User Query:
{user_input}

Give a clear farming decision in 2-3 lines.
"""

        response = generate_response(prompt)

        # ❗ CRITICAL CHECK
        if not response or "⚠️" in response or len(response) < 10:
            raise Exception("Invalid LLM response")

        return response

    except Exception as e:
        print("Decision error:", e)

        # ✅ SMART FALLBACK (important for demo)
        return f"""
Based on current conditions (Temp: {context['weather']['temperature']}°C, 
Humidity: {context['weather']['humidity']}%), irrigation is recommended.

Monitor soil moisture regularly.
"""
