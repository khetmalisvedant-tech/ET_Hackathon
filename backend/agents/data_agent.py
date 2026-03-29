# backend/agents/data_agent.py

def get_data(task):
    """
    Simulates agricultural data retrieval
    (later you can integrate real APIs)
    """

    # simple rule-based simulation
    data = {
        "weather": "No rain expected",
        "temperature": "32°C",
        "soil_status": "Dry",
        "crop": "Wheat",
        "crop_water_need": "High"
    }

    return data