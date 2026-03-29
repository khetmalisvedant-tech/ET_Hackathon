import requests

API_KEY = "8a2e2503f6a1c6dd6c180b55f03a1520"

def get_weather_by_coords(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    data = requests.get(url).json()

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"]
    }