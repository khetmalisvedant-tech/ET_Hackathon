from llm import generate_response

memory_store = []
conversation_history = []


def save_memory(entry: dict):
    """Save a past query and its result to memory."""
    memory_store.append(entry)


def get_memory() -> list:
    """Return all stored memories."""
    return memory_store


def get_context_summary() -> str:
    """
    Generate a brief context summary from the last 3 conversation turns.
    Useful for injecting history into agent prompts.
    """
    if not conversation_history:
        return ""

    recent = conversation_history[-3:]
    context_text = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}" for msg in recent
    )

    summary = generate_response(
        f"Summarise this conversation context in 1-2 sentences:\n\n{context_text}"
    )
    return summary or context_text


def add_to_history(role: str, content: str):
    """Add a message to conversation history."""
    conversation_history.append({"role": role, "content": content})