import pandas as pd

files = [
    "datasets/clinical/Z-Alizadeh sani dataset.xlsx",
    "datasets/clinical/z_alizadeh_extension.xlsx"
]

for file in files:
    print("=" * 80)
    print(file)

    excel = pd.ExcelFile(file)

    print("\nSheets:")
    print(excel.sheet_names)

    for sheet in excel.sheet_names:
        print("\nSheet:", sheet)

        df = pd.read_excel(file, sheet_name=sheet)

        print("Shape:", df.shape)
        print("\nColumns:")
        print(df.columns.tolist())

        print("\nFirst 5 rows:")
        print(df.head())

        print("\nMissing values:")
        print(df.isnull().sum())