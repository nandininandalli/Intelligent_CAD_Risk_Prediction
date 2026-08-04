import pandas as pd
import joblib

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# -------------------------------
# Load Dataset
# -------------------------------

df = pd.read_excel("datasets/clinical/Z-Alizadeh sani dataset.xlsx")   # <-- change path if needed

# -------------------------------
# Features to use
# -------------------------------

FEATURES = [
    "Age",
    "Sex",
    "BMI",
    "DM",
    "HTN",
    "Current Smoker",
    "FH",
    "Typical Chest Pain",
    "Dyspnea",
    "BP",
    "PR",
    "FBS",
    "LDL",
    "HDL",
    "TG"
]

TARGET = "Cath"

# -------------------------------
# Keep only required columns
# -------------------------------

df = df[FEATURES + [TARGET]]

# -------------------------------
# Encode categorical columns
# -------------------------------

encoders = {}

for col in FEATURES:

    if df[col].dtype == object:

        le = LabelEncoder()

        df[col] = df[col].astype(str)

        df[col] = le.fit_transform(df[col])

        encoders[col] = le

# -------------------------------
# Missing values
# -------------------------------

X = df[FEATURES]
y = df[TARGET]

imputer = SimpleImputer(strategy="most_frequent")

X = pd.DataFrame(
    imputer.fit_transform(X),
    columns=FEATURES
)

# -------------------------------
# Split
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------------
# Model
# -------------------------------

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_leaf=3,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)
print("Model Classes:", model.classes_)
pred = model.predict(X_test)

print("Accuracy :", accuracy_score(y_test, pred))

# -------------------------------
# Save
# -------------------------------

joblib.dump(model, "models/clinical_model.pkl")
joblib.dump(imputer, "models/clinical_imputer.pkl")
joblib.dump(encoders, "models/clinical_label_encoders.pkl")

print("\nClinical Model Saved Successfully")