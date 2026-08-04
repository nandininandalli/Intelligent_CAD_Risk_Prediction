import pandas as pd
import ast

print("=" * 70)
print("PREPARING PTB-XL ECG DATASET")
print("=" * 70)

df = pd.read_csv("datasets/ecg/ptbxl_database.csv")

CAD_CODES = {
    "AMI",
    "IMI",
    "ASMI",
    "ILMI",
    "ISC_",
    "ISCAL",
    "STD_",
    "QWAVE"
}


def create_label(code_string):
    try:
        codes = ast.literal_eval(code_string)

        for code in codes.keys():
            if code in CAD_CODES:
                return 1

        return 0

    except:
        return 0


df["cad_label"] = df["scp_codes"].apply(create_label)

print("\nLabel Distribution:")
print(df["cad_label"].value_counts())

df.to_csv(
    "datasets/ecg/ecg_labels.csv",
    index=False
)

print("\nSaved:")
print("datasets/ecg/ecg_labels.csv")