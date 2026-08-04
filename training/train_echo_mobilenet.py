import os
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

print("="*70)
print("TRAINING MOBILENETV2 FOR ECHO")
print("="*70)

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

X = np.load("datasets/echo/echo_images.npy").astype("float32")

if X.max() > 1:
    X /= 255.0

y = np.load("datasets/echo/echo_labels.npy")

print("Images :", X.shape)
print("Labels :", y.shape)

# ----------------------------------------------------
# Split
# ----------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train,
    y_train,
    test_size=0.20,
    random_state=42,
    stratify=y_train
)

print("Train :", X_train.shape)
print("Val   :", X_val.shape)
print("Test  :", X_test.shape)

# ----------------------------------------------------
# Class weights
# ----------------------------------------------------

weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y_train),
    y=y_train
)

class_weights = dict(enumerate(weights))

print(class_weights)

# ----------------------------------------------------
# MobileNetV2
# ----------------------------------------------------

base_model = MobileNetV2(
    include_top=False,
    weights="imagenet",
    input_shape=(112,112,3)
)

base_model.trainable = False

inputs = Input(shape=(112,112,3))

x = base_model(inputs, training=False)

x = GlobalAveragePooling2D()(x)

x = Dropout(0.4)(x)

x = Dense(128, activation="relu")(x)

x = Dropout(0.3)(x)

outputs = Dense(1, activation="sigmoid")(x)

model = Model(inputs, outputs)

model.summary()

# ----------------------------------------------------
# Compile
# ----------------------------------------------------

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

os.makedirs("models", exist_ok=True)

checkpoint = ModelCheckpoint(
    "models/echo_mobilenet.keras",
    monitor="val_accuracy",
    save_best_only=True,
    mode="max"
)

earlystop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

# ----------------------------------------------------
# Train
# ----------------------------------------------------

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=15,
    batch_size=64,
    class_weight=class_weights,
    callbacks=[checkpoint, earlystop]
)

# ----------------------------------------------------
# Test
# ----------------------------------------------------
loss, acc = model.evaluate(
    X_test,
    y_test,
    verbose=1
)

print("="*70)
print("FINAL RESULTS")
print("="*70)

print("Loss :", loss)
print("Accuracy :", acc)

model.save("models/echo_mobilenet_final.keras")

print("Model Saved")