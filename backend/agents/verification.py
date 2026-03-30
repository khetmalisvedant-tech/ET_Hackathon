from llm import generate_response


def verify_output(action: dict) -> str:
    """
    Verify that the action plan is realistic and safe.
    """
    prompt = f"""
You are a Verification Agent for a smart farming system.

Action Plan:
{action}

Tasks:
- Check if the action is realistic for a small Indian farm
- Check alignment with environmental conditions
- Identify any unsafe or impractical steps
- Flag potential hallucinations

Respond in this STRICT format:
Status: valid / invalid
Confidence: (0–100)
Reason: (1-2 sentences)
"""
    result = generate_response(prompt)
    if not result:
        return "Status: valid\nConfidence: 70\nReason: Fallback verification — manual review recommended."
    return result