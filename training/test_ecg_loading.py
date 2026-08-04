import pandas as pd
import wfdb
import numpy as np
import os

print("=" * 70)
print("TESTING PTB-XL ECG LOADING")
print("=" * 70)

df = pd.read_csv("datasets/ecg/ecg_labels.csv")

# First ECG record
record_path = "datasets/ecg/" + df.iloc[0]["filename_lr"]

print("Loading:", record_path)

record = wfdb.rdrecord(record_path)

signal = record.p_signal

print("\nSignal Shape:")
print(signal.shape)

print("\nNumber of Leads:")
print(signal.shape[1])

print("\nSamples:")
print(signal.shape[0])

print("\nSampling Frequency:")
print(record.fs)

print("\nLead Names:")
print(record.sig_name)

print("\nFirst 5 signal values:")
print(signal[:5])