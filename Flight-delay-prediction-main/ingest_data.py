import requests
import json
from datetime import datetime

def fetch_flight_data():
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)
    return response.json()

def fetch_weather_data(city="New York"):
    api_key = "8e8f562bddc4e5b6c4de4a49f24b8ff0" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

def main():
    flight_data = fetch_flight_data()
    weather_data = fetch_weather_data()

    combined = {
        "timestamp": datetime.utcnow().isoformat(),
        "flight_data": flight_data,
        "weather_data": weather_data
    }

    with open("data/raw_data.json", "w") as f:

        json.dump(combined, f, indent=4)

    print("✅ Data collected and saved to raw_data.json")

if __name__ == "__main__":
    main()

