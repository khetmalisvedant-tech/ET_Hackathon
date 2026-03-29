from datetime import datetime

def get_current_time():
    now = datetime.now()
    return {
        "time": now.strftime("%H:%M"),
        "date": now.strftime("%Y-%m-%d"),
        "day": now.strftime("%A")
    }