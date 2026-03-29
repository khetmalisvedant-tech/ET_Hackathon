# backend/agents/memory.py

memory_store = []

def save_memory(entry):
    """
    Saves past queries and results
    """
    memory_store.append(entry)


def get_memory():
    return memory_store

conversation_history = []

def run_workflow(user_input):
    conversation_history.append({"role": "user", "content": user_input})

    context = str(conversation_history[-3:])  # last 3 messages

    data = generate_response(
    f"""
    Understand context from conversation:

    {context}
    """)