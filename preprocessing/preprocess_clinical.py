import os
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

print("=" * 70)
print("PREPROCESSING Z-ALIZADEH SANI DATASET")
print("=" * 70)

# Load dataset
df = pd.read_excel(
    "datasets/clinical/Z-Alizadeh sani dataset.xlsx",
    sheet_name="Sheet 1 - Table 1"
)

print("\nDataset Shape:", df.shape)

# -----------------------------
# Convert Target
# -----------------------------
df["Cath"] = df["Cath"].replace({
    "Cad": 1,
    "CAD": 1,
    "Normal": 0
})

# -----------------------------
# Encode categorical columns
# -----------------------------
label_encoders = {}

for col in df.columns:

    if df[col].dtype == "object" and col != "Cath":

        le = LabelEncoder()

        df[col] = le.fit_transform(df[col].astype(str))

        label_encoders[col] = le

# -----------------------------
# Save encoders
# -----------------------------
os.makedirs("models", exist_ok=True)

joblib.dump(label_encoders, "models/clinical_label_encoders.pkl")

# -----------------------------
# Save processed dataset
# -----------------------------
df.to_csv(
    "datasets/clinical/clinical_processed.csv",
    index=False
)

print("\nProcessed Dataset Saved")

print("\nShape:", df.shape)

print("\nTarget Distribution:")

print(df["Cath"].value_counts())

print("\nFirst Five Rows:")

print(df.head())

print("\nPreprocessing Complete")