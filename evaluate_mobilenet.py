import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Load dataset
X = np.load("datasets/echo/echo_images.npy").astype("float32")

if X.max() > 1:
    X /= 255.0

y = np.load("datasets/echo/echo_labels.npy")

# Same split as training
_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Load saved model
model = tf.keras.models.load_model("models/echo_mobilenet.keras")

# Evaluate
loss, acc = model.evaluate(
    X_test,
    y_test,
    verbose=1
)

print("=" * 60)
print("TEST RESULTS")
print("=" * 60)
print("Loss     :", loss)
print("Accuracy :", acc)