import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load processed data
df = pd.read_csv("data/processed_data.csv")

# Features and label
X = df[["velocity", "altitude", "temperature", "wind_speed"]]
y = df["delay_label"]

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Print performance
print("✅ Model Evaluation Report:\n")
print(classification_report(y_test, y_pred, target_names=["On-Time", "Minor Delay", "Significant Delay"]))

# Save model

import joblib
...
joblib.dump(model, "models/delay_predictor.joblib")


print("🎉 Model trained and saved to models/delay_predictor.pkl")

