import os
import cv2
import numpy as np
import tensorflow as tf

# Load Echo CNN
echo_model = tf.keras.models.load_model("models/echo_mobilenet.keras")


# -------------------------------------------------
# Image Preprocessing
# -------------------------------------------------

def preprocess_image(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = cv2.resize(image, (112, 112))

    image = image.astype(np.float32) / 255.0

    image = np.expand_dims(image, axis=0)

    return image


# -------------------------------------------------
# Predict Image
# -------------------------------------------------

def predict_image(image):

    img = preprocess_image(image)

    pred = echo_model.predict(img, verbose=0)

    return float(pred[0][0])


# -------------------------------------------------
# Predict Video
# -------------------------------------------------

def predict_video(video_path):

    cap = cv2.VideoCapture(video_path)

    predictions = []

    frame_no = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_no += 1

        # Take every 10th frame
        if frame_no % 10 != 0:
            continue

        predictions.append(
            predict_image(frame)
        )

    cap.release()

    if len(predictions) == 0:
        raise ValueError("Unable to read video.")

    return float(np.mean(predictions))


# -------------------------------------------------
# Main Prediction
# -------------------------------------------------

def predict_echo(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    image_formats = [".jpg", ".jpeg", ".png"]

    video_formats = [".mp4", ".avi", ".mov"]

    if extension in image_formats:

        image = cv2.imread(file_path)

        if image is None:
            raise ValueError("Invalid image.")

        probability = predict_image(image)

    elif extension in video_formats:

        probability = predict_video(file_path)

    else:

        raise ValueError("Unsupported file format.")

    probability = max(0.0, min(1.0, probability))

    risk = round(probability * 100, 2)

    if risk < 30:
        level = "Low Risk"

    elif risk < 70:
        level = "Moderate Risk"

    else:
        level = "High Risk"

    return {

        "probability": probability,

        "risk_percent": risk,

        "risk_level": level

    }


if __name__ == "__main__":

    print(
        predict_echo("uploads/echo/sample.jpg")
    )