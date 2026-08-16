import numpy as np
import tensorflow as tf

print("=" * 60)
print("FINDING ECHO TEST INSTANCES")
print("=" * 60)

# Load dataset
X = np.load("datasets/echo/echo_images.npy").astype("float32")

if X.max() > 1:
    X = X / 255.0

print("Dataset shape:", X.shape)

# Load model
model = tf.keras.models.load_model(
    "models/echo_mobilenet.keras"
)

print("\nPredicting...")

probabilities = model.predict(
    X,
    batch_size=64,
    verbose=1
).ravel()

# --------------------------------------------------
# Find examples
# --------------------------------------------------

low = np.where(probabilities < 0.30)[0]

moderate = np.where(
    (probabilities >= 0.30) &
    (probabilities < 0.70)
)[0]

high = np.where(
    probabilities >= 0.70
)[0]


# --------------------------------------------------
# Display
# --------------------------------------------------

print("\n" + "=" * 60)
print("LOW RISK")
print("=" * 60)

for i in low[:10]:
    print(
        "Index:",
        i,
        "Probability:",
        round(probabilities[i] * 100, 2),
        "%"
    )


print("\n" + "=" * 60)
print("MODERATE RISK")
print("=" * 60)

for i in moderate[:10]:
    print(
        "Index:",
        i,
        "Probability:",
        round(probabilities[i] * 100, 2),
        "%"
    )


print("\n" + "=" * 60)
print("HIGH RISK")
print("=" * 60)

for i in high[:10]:
    print(
        "Index:",
        i,
        "Probability:",
        round(probabilities[i] * 100, 2),
        "%"
    )


# --------------------------------------------------
# Counts
# --------------------------------------------------

print("\n" + "=" * 60)
print("COUNTS")
print("=" * 60)

print("Low      :", len(low))
print("Moderate :", len(moderate))
print("High     :", len(high))