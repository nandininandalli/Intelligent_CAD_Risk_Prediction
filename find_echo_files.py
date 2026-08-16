import os
import pandas as pd

print("=" * 70)
print("ECHO DATASET FILE INFORMATION")
print("=" * 70)

# ---------------------------------------------------------
# Load FileList.csv
# ---------------------------------------------------------

filelist_path = "datasets/echo/FileList.csv"

df = pd.read_csv(filelist_path)

print("\nFileList columns:")
print(df.columns.tolist())

print("\nNumber of records:", len(df))

print("\nFirst 5 records:")
print(df.head().to_string())


# ---------------------------------------------------------
# List Echo videos
# ---------------------------------------------------------

video_folder = "datasets/echo/Videos"

videos = []

for root, dirs, files in os.walk(video_folder):

    for file in files:

        if file.lower().endswith(
            (".avi", ".mp4", ".mov")
        ):

            videos.append(
                os.path.join(root, file)
            )


print("\n" + "=" * 70)
print("VIDEO INFORMATION")
print("=" * 70)

print("Number of videos:", len(videos))

print("\nFirst 20 videos:")

for video in videos[:20]:
    print(video)


# ---------------------------------------------------------
# Labels
# ---------------------------------------------------------

import numpy as np

labels = np.load(
    "datasets/echo/echo_labels.npy"
)

print("\n" + "=" * 70)
print("LABEL INFORMATION")
print("=" * 70)

print("Labels shape:", labels.shape)

unique, counts = np.unique(
    labels,
    return_counts=True
)

for label, count in zip(unique, counts):

    print(
        "Label",
        label,
        ":",
        count
    )