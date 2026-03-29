from services.llm import generate_response
import json
import re

def take_action(decision):

    prompt = f"""
You are an Action Agent.

Convert the decision into executable agricultural actions.

Rules:
- If water needed → irrigation
- If nutrients needed → fertilizer
- If both → include both actions
- NEVER leave values empty

Output STRICT JSON:

{{
  "action_type": "irrigation / fertilization / combined",
  "steps": [
    {{
      "command": "apply_fertilizer",
      "parameters": {{
        "type": "NPK",
        "amount_kg": 20,
        "area": "field_A"
      }}
    }},
    {{
      "command": "execute_irrigation",
      "parameters": {{
        "zone": "A",
        "duration_minutes": 20
      }}
    }}
  ],
  "priority": "high / medium / low"
}}
"""

    response = generate_response(prompt)

    try:
        json_str = re.search(r'\{.*\}', response, re.DOTALL).group()
        return json.loads(json_str)
    except:
        return {"error": "Invalid JSON", "raw": response}