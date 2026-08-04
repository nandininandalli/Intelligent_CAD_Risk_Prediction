import pandas as pd
import os

print("=" * 70)
print("PTB-XL ECG DATASET INSPECTION")
print("=" * 70)

df = pd.read_csv("datasets/ecg/ptbxl_database.csv")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst Five Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nrecords100 exists:", os.path.exists("datasets/ecg/records100"))
print("records500 exists:", os.path.exists("datasets/ecg/records500"))

if os.path.exists("datasets/ecg/records100"):
    print("\nSample files in records100:")
    print(os.listdir("datasets/ecg/records100")[:10])