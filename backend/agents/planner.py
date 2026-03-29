# backend/agents/planner.py
def plan_task(input_text):
    return {
        "input": input_text,
        "steps": ["Understand user query", "Generate response"]
    }