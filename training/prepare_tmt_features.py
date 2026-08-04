import pandas as pd
import numpy as np

subjects = pd.read_csv("datasets/tmt/subject-info.csv")
tests = pd.read_csv("datasets/tmt/test_measure.csv")

rows = []

for test_id, df in tests.groupby("ID_test"):

    subject = subjects[subjects["ID_test"] == test_id]

    if len(subject) == 0:
        continue

    age = subject.iloc[0]["Age"]
    sex = subject.iloc[0]["Sex"]
    weight = subject.iloc[0]["Weight"]
    height = subject.iloc[0]["Height"]

    max_hr = df["HR"].max()
    resting_hr = df["HR"].iloc[0]
    hr_recovery = max_hr - df["HR"].iloc[-1]

    max_speed = df["Speed"].max()

    max_vo2 = df["VO2"].max()
    avg_vo2 = df["VO2"].mean()

    max_vco2 = df["VCO2"].max()

    max_rr = df["RR"].max()

    max_ve = df["VE"].max()

    duration = df["time"].max()

    rows.append([
        test_id,
        age,
        sex,
        weight,
        height,
        resting_hr,
        max_hr,
        hr_recovery,
        max_speed,
        max_vo2,
        avg_vo2,
        max_vco2,
        max_rr,
        max_ve,
        duration
    ])

features = pd.DataFrame(rows, columns=[
    "ID_test",
    "Age",
    "Sex",
    "Weight",
    "Height",
    "RestHR",
    "MaxHR",
    "HRRecovery",
    "MaxSpeed",
    "MaxVO2",
    "AvgVO2",
    "MaxVCO2",
    "MaxRR",
    "MaxVE",
    "Duration"
])

features.to_csv("datasets/tmt/tmt_features.csv", index=False)

print(features.head())
print(features.shape)
print("Saved Successfully!")