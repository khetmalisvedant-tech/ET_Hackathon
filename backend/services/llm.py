import os
import requests
from dotenv import load_dotenv

load_dotenv()


def generate_response(prompt: str, model: str = "llama-3.3-70b-versatile") -> str | None:
    """
    Send a prompt to Groq and return the response text.
    Returns None on any error.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("❌ GROQ_API_KEY not set")
            return None

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4
        }

        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=15
        )

        if res.status_code != 200:
            print(f"Groq HTTP {res.status_code}: {res.text}")
            return None

        data = res.json()

        if "choices" not in data:
            print(f"Groq unexpected response: {data}")
            return None

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"LLM Exception: {e}")
        return None