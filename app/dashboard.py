import streamlit as st
import pandas as pd
import joblib
import json

model = joblib.load("models/delay_predictor.joblib")

with open("data/raw_data.json", "r") as f:
    raw_data = json.load(f)

# Load processed data
df = pd.read_csv("data/processed_data.csv")

# Make predictions
features = df[["velocity", "altitude", "temperature", "wind_speed"]]
df["predicted_label"] = model.predict(features)

# Map prediction labels to readable text
label_map = {
    0: "✅ On-Time",
    1: "⚠️ Minor Delay",
    2: "⛔ Significant Delay"
}
df["predicted_label"] = df["predicted_label"].map(label_map)

# ---------------- STREAMLIT UI ----------------
st.title("🛫 Real-Time Flight Delay Prediction Dashboard")

st.markdown(f"**Data Timestamp:** `{raw_data['timestamp']}`")

# Weather Display
st.subheader("🌦️ Current Weather")
weather = raw_data["weather_data"]
st.write(f"**Temperature:** {weather['main']['temp']} °C")
st.write(f"**Wind Speed:** {weather['wind']['speed']} m/s")
st.write(f"**Condition:** {weather['weather'][0]['description'].capitalize()}")

# Flight Delay Predictions
st.subheader("✈️ Predicted Flight Delays")
st.dataframe(df[["callsign", "velocity", "altitude", "predicted_label"]])

# Bar chart of delay category counts
st.subheader("📊 Delay Category Distribution")
st.bar_chart(df["predicted_label"].value_counts())

st.markdown("---")
st.caption("Built with ❤️ by Team Binary Minds")

