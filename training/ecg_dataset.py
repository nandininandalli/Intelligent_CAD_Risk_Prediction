import os
import wfdb
import numpy as np
import pandas as pd
from tqdm import tqdm

print("=" * 70)
print("CREATING ECG DATASET")
print("=" * 70)

# Load labels
df = pd.read_csv("datasets/ecg/ecg_labels.csv")

# -------- IMPORTANT --------
# Start with a subset for testing
# Later we will remove this line and use the full dataset.
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df = df.head(2000)

signals = []
labels = []

for _, row in tqdm(df.iterrows(), total=len(df)):

    record_path = "datasets/ecg/" + row["filename_lr"]

    try:
        record = wfdb.rdrecord(record_path)

        signal = record.p_signal.astype(np.float32)

        # Normalize ECG
        signal = (signal - np.mean(signal)) / (np.std(signal) + 1e-8)

        signals.append(signal)
        labels.append(row["cad_label"])

    except Exception as e:
        print("Skipped:", record_path, e)

X = np.array(signals, dtype=np.float32)
y = np.array(labels, dtype=np.int32)

print("\nDataset Shape:", X.shape)
print("Labels Shape:", y.shape)

os.makedirs("datasets/ecg/processed", exist_ok=True)

np.save("datasets/ecg/processed/X.npy", X)
np.save("datasets/ecg/processed/y.npy", y)

print("\nSaved Successfully!")