import os
import numpy as np
import pandas as pd
import joblib

# ---------------------------------------------------------
# Load ECG dataset
# ---------------------------------------------------------

X = np.load(
    "datasets/ecg/processed/X.npy"
)

print("Dataset shape:", X.shape)


# ---------------------------------------------------------
# Load trained model
# ---------------------------------------------------------

model = joblib.load(
    "models/ecg_random_forest.pkl"
)


# ---------------------------------------------------------
# Feature extraction
# MUST MATCH train_ecg.py
# ---------------------------------------------------------

def extract_features(X):

    all_features = []

    for sample in X:

        sample_features = []

        for lead in range(12):

            signal = sample[:, lead].astype(np.float32)

            signal = np.nan_to_num(
                signal,
                nan=0.0,
                posinf=0.0,
                neginf=0.0
            )

            sample_features.extend([
                np.mean(signal),
                np.std(signal),
                np.min(signal),
                np.max(signal),
                np.median(signal),
                np.ptp(signal),
                np.sqrt(np.mean(signal ** 2)),
                np.mean(np.abs(signal))
            ])

        all_features.append(sample_features)

    return np.array(
        all_features,
        dtype=np.float32
    )


# ---------------------------------------------------------
# Calculate probabilities for all ECG samples
# ---------------------------------------------------------

print("\nCalculating ECG probabilities...")

features = extract_features(X)

probabilities = model.predict_proba(
    features
)[:, 1]


# ---------------------------------------------------------
# Find samples for each risk category
# ---------------------------------------------------------

low_indices = np.where(
    probabilities < 0.30
)[0]

moderate_indices = np.where(
    (probabilities >= 0.30) &
    (probabilities < 0.35)
)[0]

high_indices = np.where(
    probabilities >= 0.35
)[0]


print("\nAvailable samples:")
print("Low      :", len(low_indices))
print("Moderate :", len(moderate_indices))
print("High     :", len(high_indices))


# ---------------------------------------------------------
# Number of samples to create
# ---------------------------------------------------------

NUMBER_OF_SAMPLES = 10


# ---------------------------------------------------------
# Create folders
# ---------------------------------------------------------

os.makedirs("test_ecg/low", exist_ok=True)
os.makedirs("test_ecg/moderate", exist_ok=True)
os.makedirs("test_ecg/high", exist_ok=True)


# ---------------------------------------------------------
# Function to save ECG files
# ---------------------------------------------------------

def save_samples(indices, folder, risk_name):

    count = min(
        NUMBER_OF_SAMPLES,
        len(indices)
    )

    print(
        f"\nCreating {count} {risk_name} ECG files..."
    )

    for number, index in enumerate(
        indices[:count],
        start=1
    ):

        ecg = X[index]

        probability = probabilities[index]

        filename = os.path.join(
            folder,
            f"ecg_{risk_name.lower()}_{number}.csv"
        )

        pd.DataFrame(ecg).to_csv(
            filename,
            index=False,
            header=False
        )

        print(
            f"{filename} -> "
            f"{probability * 100:.2f}% "
            f"(Dataset index: {index})"
        )


# ---------------------------------------------------------
# Create files
# ---------------------------------------------------------

save_samples(
    low_indices,
    "test_ecg/low",
    "LOW"
)

save_samples(
    moderate_indices,
    "test_ecg/moderate",
    "MODERATE"
)

save_samples(
    high_indices,
    "test_ecg/high",
    "HIGH"
)


# ---------------------------------------------------------
# Finished
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("ECG TEST FILES CREATED")
print("=" * 60)

print("""
test_ecg/
│
├── low/
│   ├── ecg_low_1.csv
│   ├── ecg_low_2.csv
│   ├── ...
│   └── ecg_low_10.csv
│
├── moderate/
│   ├── ecg_moderate_1.csv
│   ├── ecg_moderate_2.csv
│   ├── ...
│   └── ecg_moderate_10.csv
│
└── high/
    ├── ecg_high_1.csv
    ├── ecg_high_2.csv
    ├── ...
    └── ecg_high_10.csv
""")