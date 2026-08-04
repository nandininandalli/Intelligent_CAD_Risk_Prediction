import pandas as pd
import ast
from collections import Counter

print("=" * 70)
print("PTB-XL SCP CODE ANALYSIS")
print("=" * 70)

df = pd.read_csv("datasets/ecg/ptbxl_database.csv")

counter = Counter()

for codes in df["scp_codes"]:
    try:
        code_dict = ast.literal_eval(codes)
        counter.update(code_dict.keys())
    except Exception:
        continue

print("\nTop 30 SCP Codes:\n")

for code, count in counter.most_common(30):
    print(f"{code:15} {count}")