import pandas as pd

print("=" * 60)
print("CLINICAL DATASET INSPECTION")
print("=" * 60)

# Change the filename if necessary
df = pd.read_csv("datasets/clinical/heart disease dataset.csv")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nTarget Distribution:")
print(df.iloc[:, -1].value_counts())

print("\nFirst Five Rows:")
print(df.head())