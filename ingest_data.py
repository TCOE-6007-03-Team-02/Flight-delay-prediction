import requests
import json
import datetime

def fetch_flight_data():
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)
    return response.json()

def fetch_weather_data(city):
    key = "YOUR_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
    response = requests.get(url)
    return response.json()

def main():
    flight_data = fetch_flight_data()
    weather_data = fetch_weather_data("New York")  # example

    # Combine data
    combined = {
        "timestamp": str(datetime.datetime.utcnow()),
        "flight": flight_data,
        "weather": weather_data
    }

    # Save locally (simulate S3)
    with open("data/raw_ingestion.json", "w") as f:
        json.dump(combined, f, indent=4)

if __name__ == "__main__":
    main()
