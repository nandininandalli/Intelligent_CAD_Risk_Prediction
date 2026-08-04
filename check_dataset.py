import numpy as np

X = np.load("datasets/ecg/processed/X.npy")

print("Shape:", X.shape)

print("One sample shape:", X[0].shape)

print("First sample:")
print(X[0][:5])