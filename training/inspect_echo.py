import os
import pandas as pd

print("=" * 70)
print("ECHONET DATASET INSPECTION")
print("=" * 70)

filelist = pd.read_csv("datasets/echo/FileList.csv")
volume = pd.read_csv("datasets/echo/VolumeTracings.csv")

print("\nFileList Shape:")
print(filelist.shape)

print("\nFileList Columns:")
print(filelist.columns.tolist())

print("\nFirst Five Rows:")
print(filelist.head())

print("\nMissing Values:")
print(filelist.isnull().sum())

print("\n" + "=" * 70)

print("\nVolumeTracings Shape:")
print(volume.shape)

print("\nVolumeTracings Columns:")
print(volume.columns.tolist())

print("\nFirst Five Rows:")
print(volume.head())

print("\nMissing Values:")
print(volume.isnull().sum())

video_path = "datasets/echo/Videos"

print("\nVideos Folder Exists:", os.path.exists(video_path))

if os.path.exists(video_path):
    videos = os.listdir(video_path)
    print("Total Videos:", len(videos))
    print("Sample Videos:", videos[:10])