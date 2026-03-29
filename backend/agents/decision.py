from services.llm import generate_response

def make_decision(context, user_input):

  prompt = f"""
        You are a Decision Agent in an agricultural AI system.

        Context:
        Location: {context['location']}
        Weather: {context['weather']}
        Month: {context['month']}
        WSI: {context['wsi']} ({context['wsi_level']})

        User Query:
        {user_input}

        Rules:
        - MUST consider both irrigation AND fertilization
        - If soil stress or growth phase → suggest fertilizer
        - If only water stress → irrigation
        - If both → combined recommendation

        Output format:
        Decision:
        Reasoning:
        Risk Level:
        """

  return generate_response(prompt)