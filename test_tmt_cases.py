import pandas as pd
import joblib

# Load dataset and trained model
df = pd.read_csv("datasets/tmt/tmt_features_with_cad.csv")

model = joblib.load("models/tmt_model.pkl")
scaler = joblib.load("models/tmt_scaler.pkl")

FEATURES = [
    "Age",
    "Sex",
    "Weight",
    "Height",
    "RestHR",
    "MaxHR",
    "HRRecovery",
    "MaxSpeed",
    "AvgVO2",
    "Duration"
]

# Prepare data exactly like training
X = df[FEATURES].copy()

# Encode Sex
X["Sex"] = (
    X["Sex"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({
        "male": 1,
        "m": 1,
        "1": 1,
        "female": 0,
        "f": 0,
        "0": 0
    })
)

X["Sex"] = X["Sex"].fillna(0)

# Fill missing values
for col in X.columns:
    X[col] = X[col].fillna(X[col].median())

# Scale
X_scaled = scaler.transform(X)

# Predict probabilities
probabilities = model.predict_proba(X_scaled)[:, 1]

df["Predicted_Probability"] = probabilities
df["Risk_Percent"] = probabilities * 100

# Find examples for each category
low = df[df["Risk_Percent"] < 30]
moderate = df[
    (df["Risk_Percent"] >= 30) &
    (df["Risk_Percent"] < 70)
]
high = df[df["Risk_Percent"] >= 70]

print("\n================ LOW RISK ================\n")
print(
    low[
        FEATURES + ["CAD", "Risk_Percent"]
    ].head(5).to_string(index=False)
)

print("\n================ MODERATE RISK ================\n")
print(
    moderate[
        FEATURES + ["CAD", "Risk_Percent"]
    ].head(5).to_string(index=False)
)

print("\n================ HIGH RISK ================\n")
print(
    high[
        FEATURES + ["CAD", "Risk_Percent"]
    ].head(5).to_string(index=False)
)

print("\nCounts:")
print("Low      :", len(low))
print("Moderate :", len(moderate))
print("High     :", len(high))