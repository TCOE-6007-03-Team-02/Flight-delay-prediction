import pickle
import numpy as np

model = pickle.load(open("models/delay_predictor.pkl", "rb"))

# Example input: [velocity, altitude, temperature, wind_speed]
sample = np.array([[180, 8000, 15, 2.5]])

prediction = model.predict(sample)[0]
labels = {0: "✅ On-Time", 1: "⚠️ Minor Delay", 2: "⛔ Significant Delay"}

print("Prediction:", labels[prediction])


