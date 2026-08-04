import pandas as pd

print("=" * 70)
print("TMT DATASET INSPECTION")
print("=" * 70)

subject = pd.read_csv("datasets/tmt/subject-info.csv")
measure = pd.read_csv("datasets/tmt/test_measure.csv")

print("\nSubject Info Shape:")
print(subject.shape)

print("\nSubject Columns:")
print(subject.columns.tolist())

print("\nSubject Missing Values:")
print(subject.isnull().sum())

print("\nFirst Five Rows (Subject):")
print(subject.head())

print("\n" + "=" * 70)

print("\nTest Measure Shape:")
print(measure.shape)

print("\nTest Measure Columns:")
print(measure.columns.tolist())

print("\nTest Measure Missing Values:")
print(measure.isnull().sum())

print("\nFirst Five Rows (Test Measure):")
print(measure.head())