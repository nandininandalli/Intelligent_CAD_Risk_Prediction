import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

print("="*70)
print("PREPARING ECHONET DATASET (MULTIPLE FRAMES)")
print("="*70)

CSV_PATH = "datasets/echo/FileList.csv"
VIDEO_FOLDER = "datasets/echo/Videos"

IMG_SIZE = 112

df = pd.read_csv(CSV_PATH)

images = []
labels = []

count = 0

for _, row in tqdm(df.iterrows(), total=len(df)):


    video_path = os.path.join(
        VIDEO_FOLDER,
        row["FileName"] + ".avi"
    )

    if not os.path.exists(video_path):
        continue

    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames < 10:
        cap.release()
        continue

    # Extract 5 frames
    frame_numbers = np.linspace(
        total_frames * 0.1,
        total_frames * 0.9,
        5,
        dtype=int
    )

    ef = row["EF"]

    label = 1 if ef < 50 else 0

    for frame_no in frame_numbers:

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)

        ret, frame = cap.read()

        if not ret:
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))

        frame = frame.astype(np.float32)

        images.append(frame)

        labels.append(label)

    cap.release()

    count += 1

images = np.array(images, dtype=np.float32)
labels = np.array(labels)

print("\nImages :", images.shape)
print("Labels :", labels.shape)

os.makedirs("datasets/echo", exist_ok=True)

np.save("datasets/echo/echo_images.npy", images)
np.save("datasets/echo/echo_labels.npy", labels)

print("\nDataset Saved Successfully!")