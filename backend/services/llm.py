import os
from groq import Groq

# Correct: use ENV VARIABLE NAME
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("LLM using Groq (LLaMA) 🚀")

def generate_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are an intelligent AI assistant helping users."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Error in LLM:", e)
        return "⚠️ Error generating response. Please try again."