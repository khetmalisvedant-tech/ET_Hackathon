import ollama

print("LLM using Ollama")

def generate_response(prompt):
    response = ollama.chat(
        model="llama3",   # you can also use mistral
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']