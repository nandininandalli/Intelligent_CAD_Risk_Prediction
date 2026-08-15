import os
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

print("=" * 70)
print("TRAINING ECG RANDOM FOREST")
print("=" * 70)


# =========================================================
# LOAD DATASET
# =========================================================

X = np.load("datasets/ecg/processed/X.npy")
y = np.load("datasets/ecg/processed/y.npy")

print("\nOriginal Dataset Shape :", X.shape)
print("Labels Shape          :", y.shape)

print("\nClass Distribution")

unique, counts = np.unique(y, return_counts=True)

for u, c in zip(unique, counts):
    print(f"Class {u} : {c}")


# =========================================================
# ECG FEATURE EXTRACTION
# =========================================================

def extract_ecg_features(X):
    """
    Convert ECG signals from:

        (samples, 1000, 12)

    into:

        (samples, 12 * 8)

    Statistical features are extracted from each ECG lead.
    """

    features = []

    for sample in X:

        sample_features = []

        # Process all 12 ECG leads
        for lead in range(sample.shape[1]):

            signal = sample[:, lead].astype(np.float32)

            # Remove invalid values
            signal = np.nan_to_num(
                signal,
                nan=0.0,
                posinf=0.0,
                neginf=0.0
            )

            # -------------------------------------------------
            # Statistical ECG Features
            # -------------------------------------------------

            mean_value = np.mean(signal)

            std_value = np.std(signal)

            min_value = np.min(signal)

            max_value = np.max(signal)

            median_value = np.median(signal)

            range_value = max_value - min_value

            rms_value = np.sqrt(
                np.mean(signal ** 2)
            )

            mean_abs_value = np.mean(
                np.abs(signal)
            )

            # Add features for this lead
            sample_features.extend([
                mean_value,
                std_value,
                min_value,
                max_value,
                median_value,
                range_value,
                rms_value,
                mean_abs_value
            ])

        features.append(sample_features)

    return np.array(
        features,
        dtype=np.float32
    )


print("\n" + "=" * 70)
print("EXTRACTING ECG FEATURES")
print("=" * 70)

X_features = extract_ecg_features(X)

print("\nExtracted Feature Shape :", X_features.shape)

print(
    "Features per ECG       :",
    X_features.shape[1]
)


# =========================================================
# FEATURE NAMES
# =========================================================

feature_names = []

feature_types = [
    "Mean",
    "Std",
    "Min",
    "Max",
    "Median",
    "Range",
    "RMS",
    "MeanAbs"
]

for lead in range(1, 13):

    for feature in feature_types:

        feature_names.append(
            f"Lead{lead}_{feature}"
        )


print("\nTotal Feature Names :", len(feature_names))


# =========================================================
# CONVERT TO DATAFRAME
# =========================================================

X_df = pd.DataFrame(
    X_features,
    columns=feature_names
)

print("\nFeature Dataset Preview:")
print(X_df.head())


# =========================================================
# HANDLE MISSING VALUES
# =========================================================

X_df = X_df.replace(
    [np.inf, -np.inf],
    np.nan
)

X_df = X_df.fillna(
    X_df.median()
)

X_features = X_df.values


# =========================================================
# TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X_features,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)

print("\n" + "=" * 70)
print("TRAIN TEST SPLIT")
print("=" * 70)

print("Training Samples :", X_train.shape[0])
print("Testing Samples  :", X_test.shape[0])


# =========================================================
# CLASS WEIGHTS
# =========================================================

weights = compute_class_weight(

    class_weight="balanced",

    classes=np.unique(y_train),

    y=y_train
)

class_weights = {
    int(cls): float(weight)
    for cls, weight
    in zip(np.unique(y_train), weights)
}

print("\nClass Weights:")
print(class_weights)


# =========================================================
# RANDOM FOREST MODEL
# =========================================================

print("\n" + "=" * 70)
print("BUILDING RANDOM FOREST MODEL")
print("=" * 70)

model = RandomForestClassifier(

    n_estimators=500,

    max_depth=10,

    min_samples_split=5,

    min_samples_leaf=2,

    class_weight=class_weights,

    random_state=42,

    n_jobs=-1
)


# =========================================================
# TRAIN
# =========================================================

print("\nTraining Random Forest...")

model.fit(
    X_train,
    y_train
)

print("Training Completed Successfully!")


# =========================================================
# PREDICTION
# =========================================================

pred = model.predict(
    X_test
)

prob = model.predict_proba(
    X_test
)[:, 1]


# =========================================================
# EVALUATION
# =========================================================

accuracy = accuracy_score(
    y_test,
    pred
)

precision = precision_score(
    y_test,
    pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    pred,
    zero_division=0
)

try:

    roc_auc = roc_auc_score(
        y_test,
        prob
    )

except ValueError:

    roc_auc = 0.0


print("\n" + "=" * 70)
print("FINAL ECG RANDOM FOREST RESULTS")
print("=" * 70)

print(
    "\nAccuracy  :",
    round(accuracy, 4)
)

print(
    "Precision :",
    round(precision, 4)
)

print(
    "Recall    :",
    round(recall, 4)
)

print(
    "F1-Score  :",
    round(f1, 4)
)

print(
    "ROC-AUC   :",
    round(roc_auc, 4)
)


# =========================================================
# CLASSIFICATION REPORT
# =========================================================

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)

print(
    classification_report(
        y_test,
        pred,
        zero_division=0
    )
)


# =========================================================
# CONFUSION MATRIX
# =========================================================

print("\n" + "=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)

cm = confusion_matrix(
    y_test,
    pred
)

print(cm)


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

print("\n" + "=" * 70)
print("TOP ECG FEATURES")
print("=" * 70)

importance = pd.DataFrame({

    "Feature": feature_names,

    "Importance":
        model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

print(
    importance.head(20).to_string(
        index=False
    )
)


# =========================================================
# SAVE MODEL
# =========================================================

os.makedirs(
    "models",
    exist_ok=True
)


# Save Random Forest model
joblib.dump(

    model,

    "models/ecg_random_forest.pkl"

)


# Save feature names
joblib.dump(

    feature_names,

    "models/ecg_feature_names.pkl"

)


# Save feature medians
joblib.dump(

    X_df.median().to_dict(),

    "models/ecg_feature_medians.pkl"

)


print("\n" + "=" * 70)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 70)

print(
    "\nModel : models/ecg_random_forest.pkl"
)

print(
    "Features : models/ecg_feature_names.pkl"
)

print(
    "Medians : models/ecg_feature_medians.pkl"
)

print("\nECG Random Forest Training Completed!")