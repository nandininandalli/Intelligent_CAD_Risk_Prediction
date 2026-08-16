import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

print("=" * 70)
print("FAST ECHO MODEL EVALUATION")
print("=" * 70)

# =========================================================
# LOAD DATA
# =========================================================

X = np.load(
    "datasets/echo/echo_images.npy"
).astype("float32")

y = np.load(
    "datasets/echo/echo_labels.npy"
)

if X.max() > 1:
    X /= 255.0

print("Dataset:", X.shape)

# =========================================================
# RECREATE SAME TEST SPLIT
# =========================================================

_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Full test set:", X_test.shape)

# =========================================================
# TAKE ONLY 500 TEST SAMPLES
# =========================================================

np.random.seed(42)

indices = np.random.choice(
    len(X_test),
    size=500,
    replace=False
)

X_small = X_test[indices]
y_small = y_test[indices]

print("Evaluation samples:", X_small.shape[0])

# =========================================================
# LOAD ALREADY TRAINED MODEL
# =========================================================

print("\nLoading trained Echo model...")

model = tf.keras.models.load_model(
    "models/echo_mobilenet.keras"
)

print("Model loaded.")

# =========================================================
# PREDICT
# =========================================================

print("\nPredicting 500 samples...")

probabilities = model.predict(
    X_small,
    batch_size=64,
    verbose=1
).ravel()

predictions = (
    probabilities >= 0.5
).astype(int)

# =========================================================
# METRICS
# =========================================================

accuracy = accuracy_score(
    y_small,
    predictions
)

precision = precision_score(
    y_small,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_small,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_small,
    predictions,
    zero_division=0
)

auc = roc_auc_score(
    y_small,
    probabilities
)

cm = confusion_matrix(
    y_small,
    predictions
)

# =========================================================
# RESULTS
# =========================================================

print("\n")
print("=" * 70)
print("ECHO MODEL RESULTS")
print("=" * 70)

print(
    f"Accuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision * 100:.2f}%"
)

print(
    f"Recall    : {recall * 100:.2f}%"
)

print(
    f"F1-Score  : {f1 * 100:.2f}%"
)

print(
    f"ROC-AUC   : {auc:.4f}"
)

print("\nConfusion Matrix:")
print(cm)

print("=" * 70)
print("Evaluation completed.")
print("=" * 70)