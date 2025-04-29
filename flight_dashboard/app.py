import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import timedelta

# Set up page config
st.set_page_config(page_title="Flight Delay Prediction Dashboard", layout="wide")

# Load the new prediction data
df = pd.read_csv("predicted_flight_delays_rf.csv")

# Convert timestamp to datetime if available
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['predicted_arrival_time'] = df['timestamp'] + df['predicted_arrival_delay'].apply(lambda x: timedelta(minutes=x))
else:
    df['predicted_arrival_time'] = "Unknown"

# Page title
st.title("🛬 Flight Delay Prediction Dashboard (Random Forest)")
st.markdown("This dashboard visualizes predicted arrival delays and expected arrival times for upcoming flights using RandomForestRegressor.")

# --- Filters ---
col1, col2 = st.columns(2)
with col1:
    city = st.selectbox("Filter by Arrival City", options=["All"] + sorted(df['city'].dropna().unique().tolist()))
with col2:
    status = st.radio("Show Flights That Are...", options=["All", "On Time", "Delayed"])

# Apply filters
filtered = df.copy()
if city != "All":
    filtered = filtered[filtered['city'] == city]
if status != "All":
    filtered = filtered[filtered['predicted_status'] == status]

# --- Summary Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("🔁 Total Flights", len(filtered))
col2.metric("⏱️ Average Predicted Delay", f"{filtered['predicted_arrival_delay'].mean():.2f} min")
col3.metric("🚨 Max Predicted Delay", f"{filtered['predicted_arrival_delay'].max():.2f} min")

# --- Flight Delay Table ---
st.subheader("🗂️ Flight Delay Forecast")
st.dataframe(filtered[[
    'flight_iata', 'departure_airport', 'arrival_airport', 'city',
    'delay_hr_min', 'predicted_status', 'timestamp', 'predicted_arrival_time'
]].sort_values(by='predicted_arrival_time'), use_container_width=True)

# --- Plot: Predicted Delay Distribution ---
st.subheader("📊 Predicted Delay Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(filtered['predicted_arrival_delay'], bins=20, kde=True, ax=ax1)
ax1.set_xlabel("Predicted Delay (minutes)")
st.pyplot(fig1)

# --- Plot: Actual vs Predicted Arrival Times ---
if 'timestamp' in filtered.columns and pd.api.types.is_datetime64_any_dtype(filtered['timestamp']):
    st.subheader("🕒 Actual vs Predicted Arrival Times")
    
    timeline_df = filtered.dropna(subset=['timestamp', 'predicted_arrival_time', 'flight_iata']).copy()
    timeline_df['flight_iata'] = timeline_df['flight_iata'].astype(str)
    timeline_df = timeline_df.head(30)  # limit to 30 flights

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.scatter(timeline_df['timestamp'], timeline_df['flight_iata'], label="Scheduled", color='green')
    ax2.scatter(timeline_df['predicted_arrival_time'], timeline_df['flight_iata'], label="Predicted", color='red')
    ax2.legend()
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Flight IATA Code")
    ax2.set_title("Actual vs Predicted Arrival Times")
    st.pyplot(fig2)

# Footer
st.markdown("---")
st.caption("Built with Streamlit • Predictions powered by Random Forest Regression")
