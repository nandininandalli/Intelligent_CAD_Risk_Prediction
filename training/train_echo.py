import os
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight

import tensorflow as tf

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout

from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

print("=" * 70)
print("TRAINING IMPROVED ECHO CNN")
print("=" * 70)

####################################################
# LOAD DATA
####################################################

X = np.load("datasets/echo/echo_images.npy")
y = np.load("datasets/echo/echo_labels.npy")

print("\nImages :", X.shape)
print("Labels :", y.shape)

####################################################
# NORMALIZE
####################################################

X = X.astype(np.float32)

if X.max() > 1:
    X = X / 255.0

####################################################
# TRAIN TEST SPLIT
####################################################

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)

print("\nTraining :", X_train.shape)
print("Testing  :", X_test.shape)

####################################################
# CLASS WEIGHTS
####################################################

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

####################################################
# DATA AUGMENTATION
####################################################

train_generator = ImageDataGenerator(

    rotation_range=10,

    width_shift_range=0.08,

    height_shift_range=0.08,

    zoom_range=0.10,

    horizontal_flip=True

)

####################################################
# CNN MODEL
####################################################

model = Sequential()

model.add(
    Conv2D(
        32,
        (3,3),
        activation="relu",
        padding="same",
        input_shape=(112,112,3)
    )
)

model.add(BatchNormalization())

model.add(MaxPooling2D())

####################################################

model.add(
    Conv2D(
        64,
        (3,3),
        activation="relu",
        padding="same"
    )
)

model.add(BatchNormalization())

model.add(MaxPooling2D())

####################################################

model.add(
    Conv2D(
        128,
        (3,3),
        activation="relu",
        padding="same"
    )
)

model.add(BatchNormalization())

model.add(MaxPooling2D())

####################################################

model.add(
    Conv2D(
        256,
        (3,3),
        activation="relu",
        padding="same"
    )
)

model.add(BatchNormalization())

model.add(MaxPooling2D())

####################################################

model.add(GlobalAveragePooling2D())

####################################################

model.add(Dense(256, activation="relu"))

model.add(BatchNormalization())

model.add(Dropout(0.5))

####################################################

model.add(Dense(128, activation="relu"))

model.add(BatchNormalization())

model.add(Dropout(0.4))

####################################################

model.add(Dense(64, activation="relu"))

model.add(Dropout(0.3))

####################################################

model.add(Dense(1, activation="sigmoid"))

####################################################

model.summary()

####################################################
# COMPILE
####################################################

model.compile(

    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.0001
    ),

    loss="binary_crossentropy",

    metrics=["accuracy"]

)

####################################################
# CALLBACKS
####################################################

os.makedirs("models", exist_ok=True)

checkpoint = ModelCheckpoint(

    "models/echo_cnn.keras",

    monitor="val_accuracy",

    save_best_only=True,

    mode="max",

    verbose=1

)

earlystop = EarlyStopping(

    monitor="val_loss",

    patience=8,

    restore_best_weights=True,

    verbose=1

)

####################################################
# TRAIN
####################################################

history = model.fit(

    train_generator.flow(
        X_train,
        y_train,
        batch_size=16
    ),

    validation_data=(X_test, y_test),

    epochs=35,

    class_weight=class_weights,

    callbacks=[
        checkpoint,
        earlystop
    ]

)

####################################################
# TEST
####################################################

loss, accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=1
)

print("\n")
print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)

print("Loss     :", round(loss,4))
print("Accuracy :", round(accuracy,4))

####################################################
# SAVE
####################################################

model.save("models/echo_cnn_final.keras")

print("\nModel Saved Successfully!")
print("Saved To : models/echo_cnn_final.keras")