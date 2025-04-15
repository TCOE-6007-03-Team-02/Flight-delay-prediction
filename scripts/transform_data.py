import json
import pandas as pd
from datetime import datetime

def transform(input_file, output_file):
    # Load raw JSON data
    with open(input_file, "r") as f:
        raw = json.load(f)

    flights = raw["flight_data"].get("states", [])
    weather = raw["weather_data"]
    rows = []

    for flight in flights:
        try:
            rows.append({
                "callsign": flight[1].strip(),
                "country": flight[2],
                "velocity": float(flight[9]) if flight[9] is not None else 0,
                "altitude": float(flight[7]) if flight[7] is not None else 0,
                "temperature": float(weather["main"]["temp"]),
                "wind_speed": float(weather["wind"]["speed"]),
                "timestamp": datetime.utcfromtimestamp(flight[3]).isoformat()
            })
        except Exception as e:
            continue  # skip any bad records

    df = pd.DataFrame(rows)

    # Label delay based on velocity as a placeholder
    df["delay_label"] = df["velocity"].apply(
        lambda v: 0 if v > 200 else (1 if v > 100 else 2)
    )

    df.to_csv(output_file, index=False)
    print(f"✅ Transformed data saved to {output_file}")

if __name__ == "__main__":
    transform("data/raw_data.json", "data/processed_data.csv")

