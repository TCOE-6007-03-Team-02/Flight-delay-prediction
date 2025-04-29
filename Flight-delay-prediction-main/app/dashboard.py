import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load processed data
df = pd.read_csv("data/processed_data.csv")

# Define features and target
features = df[["month", "day", "hour", "temperature", "wind_speed"]]
target = df["status"]

# Train/test split (optional - or just train on full)
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train a new model on the fly
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on full data
df["predicted_label"] = model.predict(features)