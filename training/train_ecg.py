import os
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv1D,
    MaxPooling1D,
    BatchNormalization,
    GlobalAveragePooling1D,
    Dense,
    Dropout
)
from tensorflow.keras.callbacks import EarlyStopping

print("=" * 70)
print("TRAINING ECG CNN")
print("=" * 70)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

X = np.load("datasets/ecg/processed/X.npy")
y = np.load("datasets/ecg/processed/y.npy")

print("Dataset Shape :", X.shape)
print("Labels Shape  :", y.shape)

print("\nClass Distribution")
unique, counts = np.unique(y, return_counts=True)

for u, c in zip(unique, counts):
    print(f"Class {u} : {c}")

# ---------------------------------------------------
# Train Test Split
# ---------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ---------------------------------------------------
# Class Weights
# ---------------------------------------------------

weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y_train),
    y=y_train
)

class_weights = {
    0: weights[0],
    1: weights[1]
}

print("\nClass Weights")
print(class_weights)

# ---------------------------------------------------
# Build CNN
# ---------------------------------------------------

model = Sequential([

    Conv1D(
        filters=64,
        kernel_size=7,
        activation="relu",
        input_shape=(1000,12)
    ),

    BatchNormalization(),

    MaxPooling1D(2),

    Conv1D(
        filters=128,
        kernel_size=5,
        activation="relu"
    ),

    BatchNormalization(),

    MaxPooling1D(2),

    Conv1D(
        filters=256,
        kernel_size=3,
        activation="relu"
    ),

    BatchNormalization(),

    GlobalAveragePooling1D(),

    Dense(
        256,
        activation="relu"
    ),

    Dropout(0.40),

    Dense(
        1,
        activation="sigmoid"
    )

])

model.summary()

# ---------------------------------------------------
# Compile
# ---------------------------------------------------

model.compile(

    optimizer="adam",

    loss="binary_crossentropy",

    metrics=["accuracy"]

)

# ---------------------------------------------------
# Early Stopping
# ---------------------------------------------------

early_stop = EarlyStopping(

    monitor="val_loss",

    patience=8,

    restore_best_weights=True

)

# ---------------------------------------------------
# Train
# ---------------------------------------------------

history = model.fit(

    X_train,

    y_train,

    validation_split=0.20,

    epochs=50,

    batch_size=32,

    class_weight=class_weights,

    callbacks=[early_stop],

    verbose=1

)

# ---------------------------------------------------
# Evaluate
# ---------------------------------------------------

loss, accuracy = model.evaluate(

    X_test,

    y_test,

    verbose=0

)

print("\n")
print("=" * 70)
print("FINAL TEST RESULTS")
print("=" * 70)

print("Loss     :", round(loss,4))
print("Accuracy :", round(accuracy,4))

# ---------------------------------------------------
# Save Model
# ---------------------------------------------------

os.makedirs("models", exist_ok=True)

model.save("models/ecg_cnn.keras")

print("\nModel Saved Successfully!")
print("Saved To : models/ecg_cnn.keras")