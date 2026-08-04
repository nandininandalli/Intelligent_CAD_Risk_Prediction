import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

print("=" * 70)
print("TRAINING TMT CAD CLASSIFIER")
print("=" * 70)

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

df = pd.read_csv("datasets/tmt/tmt_features_with_cad.csv")

print("\nDataset Shape :", df.shape)

print("\nMissing Values")
print(df.isnull().sum())

# -------------------------------------------------
# Features (MUST MATCH YOUR HTML FORM)
# -------------------------------------------------

FEATURES = [
    "Age",
    "Sex",
    "Weight",
    "Height",
    "RestHR",
    "MaxHR",
    "HRRecovery",
    "MaxSpeed",
    "AvgVO2",
    "Duration"
]

TARGET = "CAD"

# -------------------------------------------------
# Keep required columns only
# -------------------------------------------------

df = df[FEATURES + [TARGET]]

# -------------------------------------------------
# Remove missing target
# -------------------------------------------------

df = df.dropna(subset=[TARGET])

# -------------------------------------------------
# Fill missing feature values
# -------------------------------------------------

X = df[FEATURES].copy()

for col in X.columns:
    if X[col].dtype != object:
        X[col] = X[col].fillna(X[col].median())

# -------------------------------------------------
# Encode Sex
# Male = 1
# Female = 0
# -------------------------------------------------

X["Sex"] = (
    X["Sex"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({
        "male": 1,
        "m": 1,
        "1": 1,
        "female": 0,
        "f": 0,
        "0": 0
    })
)

X["Sex"] = X["Sex"].fillna(0)

# -------------------------------------------------
# Target
# -------------------------------------------------

y = df[TARGET].astype(int)

print("\nCAD Distribution")
print(y.value_counts())

# -------------------------------------------------
# Train Test Split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# -------------------------------------------------
# Scaling
# -------------------------------------------------

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

# -------------------------------------------------
# Model
# -------------------------------------------------

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -------------------------------------------------
# Evaluation
# -------------------------------------------------

pred = model.predict(X_test)

prob = model.predict_proba(X_test)[:, 1]

print("\nAccuracy :", round(accuracy_score(y_test, pred), 4))

print("ROC AUC  :", round(roc_auc_score(y_test, prob), 4))

print("\nClassification Report\n")

print(classification_report(y_test, pred))

# -------------------------------------------------
# Feature Importance
# -------------------------------------------------

importance = pd.DataFrame({
    "Feature": FEATURES,
    "Importance": model.feature_importances_
})

print("\nFeature Importance")

print(
    importance.sort_values(
        by="Importance",
        ascending=False
    )
)

# -------------------------------------------------
# Save
# -------------------------------------------------

joblib.dump(model, "models/tmt_model.pkl")

joblib.dump(scaler, "models/tmt_scaler.pkl")

print("\nTraining Feature Order")

print(FEATURES)

print("\n✅ TMT Model Saved Successfully")