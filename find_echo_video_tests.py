import os
import shutil
import cv2
import numpy as np
import tensorflow as tf

# ============================================================
# SETTINGS
# ============================================================

VIDEO_FOLDER = "datasets/echo/Videos"
MODEL_PATH = "models/echo_mobilenet.keras"

OUTPUT_FOLDER = "datasets/echo/test_samples"

LOW_LIMIT = 5
MODERATE_LIMIT = 5
HIGH_LIMIT = 5

# ============================================================
# CREATE OUTPUT FOLDERS
# ============================================================

low_folder = os.path.join(OUTPUT_FOLDER, "low")
moderate_folder = os.path.join(OUTPUT_FOLDER, "moderate")
high_folder = os.path.join(OUTPUT_FOLDER, "high")

os.makedirs(low_folder, exist_ok=True)
os.makedirs(moderate_folder, exist_ok=True)
os.makedirs(high_folder, exist_ok=True)

# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 70)
print("SEARCHING AND SAVING ECHO TEST VIDEOS")
print("=" * 70)

print("\nLoading Echo model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")

# ============================================================
# GET VIDEOS
# ============================================================

video_files = []

for file in os.listdir(VIDEO_FOLDER):

    if file.lower().endswith((".avi", ".mp4", ".mov")):

        video_files.append(
            os.path.join(VIDEO_FOLDER, file)
        )

print("\nTotal videos:", len(video_files))

# ============================================================
# PREPROCESS FRAME
# ============================================================

def preprocess_frame(frame):

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    frame = cv2.resize(
        frame,
        (112, 112)
    )

    frame = frame.astype(
        np.float32
    ) / 255.0

    frame = np.expand_dims(
        frame,
        axis=0
    )

    return frame


# ============================================================
# PREDICT VIDEO
# ============================================================

def predict_video(video_path):

    cap = cv2.VideoCapture(video_path)

    predictions = []

    frame_no = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_no += 1

        # Same as predict_echo.py
        if frame_no % 10 != 0:
            continue

        processed = preprocess_frame(frame)

        prediction = model.predict(
            processed,
            verbose=0
        )

        predictions.append(
            float(prediction[0][0])
        )

    cap.release()

    if len(predictions) == 0:
        return None

    return float(
        np.mean(predictions)
    )


# ============================================================
# STORAGE
# ============================================================

low_cases = []
moderate_cases = []
high_cases = []

# ============================================================
# SEARCH VIDEOS
# ============================================================

for index, video_path in enumerate(video_files):

    if (
        len(low_cases) >= LOW_LIMIT
        and
        len(moderate_cases) >= MODERATE_LIMIT
        and
        len(high_cases) >= HIGH_LIMIT
    ):
        break

    try:

        probability = predict_video(video_path)

        if probability is None:
            continue

        risk = probability * 100

        filename = os.path.basename(video_path)

        # ====================================================
        # LOW
        # ====================================================

        if risk < 30:

            if len(low_cases) < LOW_LIMIT:

                number = len(low_cases) + 1

                destination = os.path.join(
                    low_folder,
                    f"low_{number}.avi"
                )

                shutil.copy2(
                    video_path,
                    destination
                )

                low_cases.append(
                    (
                        video_path,
                        destination,
                        risk
                    )
                )

                print("\nLOW RISK FOUND")
                print("Original :", video_path)
                print("Saved as :", destination)
                print("Risk     :", round(risk, 2), "%")

        # ====================================================
        # MODERATE
        # ====================================================

        elif risk < 70:

            if len(moderate_cases) < MODERATE_LIMIT:

                number = len(moderate_cases) + 1

                destination = os.path.join(
                    moderate_folder,
                    f"moderate_{number}.avi"
                )

                shutil.copy2(
                    video_path,
                    destination
                )

                moderate_cases.append(
                    (
                        video_path,
                        destination,
                        risk
                    )
                )

                print("\nMODERATE RISK FOUND")
                print("Original :", video_path)
                print("Saved as :", destination)
                print("Risk     :", round(risk, 2), "%")

        # ====================================================
        # HIGH
        # ====================================================

        else:

            if len(high_cases) < HIGH_LIMIT:

                number = len(high_cases) + 1

                destination = os.path.join(
                    high_folder,
                    f"high_{number}.avi"
                )

                shutil.copy2(
                    video_path,
                    destination
                )

                high_cases.append(
                    (
                        video_path,
                        destination,
                        risk
                    )
                )

                print("\nHIGH RISK FOUND")
                print("Original :", video_path)
                print("Saved as :", destination)
                print("Risk     :", round(risk, 2), "%")

    except Exception as e:

        print(
            "\nError processing:",
            video_path
        )

        print(
            "Error:",
            e
        )


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("FINAL ECHO TEST SAMPLES")
print("=" * 70)

# ============================================================
# LOW
# ============================================================

print("\nLOW RISK")
print("-" * 70)

for i, (original, saved, risk) in enumerate(
    low_cases,
    start=1
):

    print(
        f"{i}. {saved}"
    )

    print(
        f"   Risk: {risk:.2f}%"
    )


# ============================================================
# MODERATE
# ============================================================

print("\nMODERATE RISK")
print("-" * 70)

for i, (original, saved, risk) in enumerate(
    moderate_cases,
    start=1
):

    print(
        f"{i}. {saved}"
    )

    print(
        f"   Risk: {risk:.2f}%"
    )


# ============================================================
# HIGH
# ============================================================

print("\nHIGH RISK")
print("-" * 70)

for i, (original, saved, risk) in enumerate(
    high_cases,
    start=1
):

    print(
        f"{i}. {saved}"
    )

    print(
        f"   Risk: {risk:.2f}%"
    )


# ============================================================
# COUNTS
# ============================================================

print("\n")
print("=" * 70)
print("COUNTS")
print("=" * 70)

print("Low      :", len(low_cases))
print("Moderate :", len(moderate_cases))
print("High     :", len(high_cases))

print("\nSaved test videos in:")
print(OUTPUT_FOLDER)

print("=" * 70)