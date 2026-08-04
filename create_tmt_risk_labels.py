import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load features
df = pd.read_csv("datasets/tmt/tmt_features.csv")

# Fill missing values
df = df.fillna(df.median(numeric_only=True))

# -------------------------
# Convert each feature to risk
# -------------------------

def high_risk(col):
    scaler = MinMaxScaler(feature_range=(0, 100))
    return scaler.fit_transform(df[[col]]).flatten()
def low_risk(col):
    scaler = MinMaxScaler(feature_range=(0, 100))
    values = scaler.fit_transform(df[[col]]).flatten()
    return 100 - values

df["Age_R"] = high_risk("Age")
df["RestHR_R"] = high_risk("RestHR")
df["HRRecovery_R"] = low_risk("HRRecovery")
df["MaxVO2_R"] = low_risk("MaxVO2")
df["Duration_R"] = low_risk("Duration")
df["MaxSpeed_R"] = low_risk("MaxSpeed")
df["MaxHR_R"] = low_risk("MaxHR")

# -------------------------
# Weighted CAD Risk
# -------------------------

df["CAD_Risk"] = (
      0.20 * df["Age_R"]
    + 0.15 * df["RestHR_R"]
    + 0.20 * df["HRRecovery_R"]
    + 0.20 * df["MaxVO2_R"]
    + 0.10 * df["Duration_R"]
    + 0.10 * df["MaxSpeed_R"]
    + 0.05 * df["MaxHR_R"]
)

# Convert to 0-100
df["CAD_Risk"] = df["CAD_Risk"].round(2)

# Binary label for training
df["CAD"] = (df["CAD_Risk"] >= 50).astype(int)

print(df["CAD"].value_counts())

df.to_csv(
    "datasets/tmt/tmt_features_with_cad.csv",
    index=False
)

print("Done.")