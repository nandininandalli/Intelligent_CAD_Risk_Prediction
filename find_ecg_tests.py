import numpy as np
import joblib

# ---------------------------------------------------------
# Load ECG dataset and model
# ---------------------------------------------------------

X = np.load("datasets/ecg/processed/X.npy")

model = joblib.load(
    "models/ecg_random_forest.pkl"
)

print("Dataset shape:", X.shape)


# ---------------------------------------------------------
# Extract exactly the same 96 features used during training
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
# Extract features
# ---------------------------------------------------------

print("\nExtracting features...")

F = extract_features(X)

print("Feature shape:", F.shape)


# ---------------------------------------------------------
# Get probabilities
# ---------------------------------------------------------

probabilities = model.predict_proba(F)[:, 1]


# ---------------------------------------------------------
# Find examples
# ---------------------------------------------------------

low = np.where(
    probabilities < 0.30
)[0]

moderate = np.where(
    (probabilities >= 0.30) &
    (probabilities < 0.35)
)[0]

high = np.where(
    probabilities >= 0.35
)[0]


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("ECG TEST INSTANCES")
print("=" * 60)

print("\nLOW RISK")

for i in low[:10]:

    print(
        "Index:",
        i,
        "Probability:",
        round(probabilities[i] * 100, 2),
        "%"
    )


print("\nMODERATE RISK")

for i in moderate[:10]:

    print(
        "Index:",
        i,
        "Probability:",
        round(probabilities[i] * 100, 2),
        "%"
    )


print("\nHIGH RISK")

for i in high[:10]:

    print(
        "Index:",
        i,
        "Probability:",
        round(probabilities[i] * 100, 2),
        "%"
    )


# ---------------------------------------------------------
# Counts
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("COUNTS")
print("=" * 60)

print("Low      :", len(low))
print("Moderate :", len(moderate))
print("High     :", len(high))