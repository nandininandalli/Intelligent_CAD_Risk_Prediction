import os
import shutil
import random

# Change these paths
ECG_DATASET = r"D:datasets\ecg\ecg_labels.csv"
ECHO_DATASET = r"D:\echo\echo_images,npy"

# Your Flask upload folders
ECG_UPLOAD = r"uploads\ecg"
ECHO_UPLOAD = r"uploads\echo"

os.makedirs(ECG_UPLOAD, exist_ok=True)
os.makedirs(ECHO_UPLOAD, exist_ok=True)


def get_random_file(folder, ext):
    files = [f for f in os.listdir(folder) if f.lower().endswith(ext)]
    return random.choice(files)


# ---------------- ECG ----------------

low_ecg = get_random_file(os.path.join(ECG_DATASET, "Normal"), ".csv")
high_ecg = get_random_file(os.path.join(ECG_DATASET, "CAD"), ".csv")

shutil.copy(
    os.path.join(ECG_DATASET, "Normal", low_ecg),
    os.path.join(ECG_UPLOAD, "sample_ecg_low.csv")
)

shutil.copy(
    os.path.join(ECG_DATASET, "CAD", high_ecg),
    os.path.join(ECG_UPLOAD, "sample_ecg_high.csv")
)


# ---------------- Echo ----------------

low_echo = get_random_file(os.path.join(ECHO_DATASET, "Normal"), ".jpg")
high_echo = get_random_file(os.path.join(ECHO_DATASET, "CAD"), ".jpg")

shutil.copy(
    os.path.join(ECHO_DATASET, "Normal", low_echo),
    os.path.join(ECHO_UPLOAD, "sample_echo_low.jpg")
)

shutil.copy(
    os.path.join(ECHO_DATASET, "CAD", high_echo),
    os.path.join(ECHO_UPLOAD, "sample_echo_high.jpg")
)

print("Done!")
print("Low ECG :", low_ecg)
print("High ECG:", high_ecg)
print("Low Echo :", low_echo)
print("High Echo:", high_echo)