from services.llm import generate_response

def verify_output(action):

    prompt = f"""
You are a Verification Agent.

Action Plan:
{action}

Tasks:
- Check if action is realistic
- Check if it aligns with environmental conditions
- Detect hallucinations
- Identify unsafe or impractical steps

Output STRICT format:

Status: valid / invalid
Confidence: (0–100)
Reason:
"""

    return generate_response(prompt)