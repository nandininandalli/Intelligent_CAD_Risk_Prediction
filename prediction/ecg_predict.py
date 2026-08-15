import numpy as np
import pandas as pd
import joblib


# =======================================================
# LOAD ECG RANDOM FOREST MODEL
# =======================================================

ecg_model = joblib.load(
    "models/ecg_random_forest.pkl"
)

# Load feature medians used during training
feature_medians = joblib.load(
    "models/ecg_feature_medians.pkl"
)


# =======================================================
# ECG FEATURE EXTRACTION
# =======================================================

def extract_ecg_features(ecg):

    """
    Convert ECG signal from:

        (1000, 12)

    into:

        (1, 96)

    Same feature extraction used during training.
    """

    features = []

    for lead in range(ecg.shape[1]):

        signal = ecg[:, lead].astype(
            np.float32
        )

        signal = np.nan_to_num(
            signal,
            nan=0.0,
            posinf=0.0,
            neginf=0.0
        )

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

        features.extend([
            mean_value,
            std_value,
            min_value,
            max_value,
            median_value,
            range_value,
            rms_value,
            mean_abs_value
        ])

    return np.array(
        features,
        dtype=np.float32
    ).reshape(1, -1)


# =======================================================
# PREPROCESS ECG CSV
# =======================================================

def preprocess_ecg(csv_path):

    """
    Supports:

    - 1 row × 12 columns
    - Multiple rows × 12 columns

    Converts ECG into:

        1000 × 12
    """

    df = pd.read_csv(
        csv_path,
        header=None
    )

    # Convert to numeric
    df = df.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Remove completely empty rows
    df = df.dropna(
        how="all"
    )

    # Fill missing values
    df = df.fillna(0)

    print("\n========== ECG INPUT ==========")

    print(
        "Original Shape :",
        df.shape
    )

    # ---------------------------------------------------
    # Check columns
    # ---------------------------------------------------

    if df.shape[1] < 12:

        raise ValueError(
            f"ECG CSV must contain at least "
            f"12 columns. Found {df.shape[1]}"
        )

    # Keep first 12 leads
    ecg = df.iloc[
        :, :12
    ].values.astype(
        np.float32
    )

    # ---------------------------------------------------
    # Adjust number of samples
    # ---------------------------------------------------

    # One row
    if ecg.shape[0] == 1:

        ecg = np.repeat(
            ecg,
            1000,
            axis=0
        )

    # Less than 1000 samples
    elif ecg.shape[0] < 1000:

        padding = np.zeros(
            (
                1000 - ecg.shape[0],
                12
            ),
            dtype=np.float32
        )

        ecg = np.vstack(
            (
                ecg,
                padding
            )
        )

    # More than 1000 samples
    elif ecg.shape[0] > 1000:

        ecg = ecg[
            :1000
        ]

    print(
        "Processed Shape :",
        ecg.shape
    )

    return ecg


# =======================================================
# PREDICTION
# =======================================================

def predict_ecg(csv_path):

    # ---------------------------------------------------
    # Preprocess ECG
    # ---------------------------------------------------

    ecg = preprocess_ecg(
        csv_path
    )

    # ---------------------------------------------------
    # Extract features
    # ---------------------------------------------------

    features = extract_ecg_features(
        ecg
    )

    print(
        "Feature Shape :",
        features.shape
    )

    # ---------------------------------------------------
    # Handle missing values
    # ---------------------------------------------------

    feature_df = pd.DataFrame(
        features
    )

    # ---------------------------------------------------
    # Random Forest prediction
    # ---------------------------------------------------

    prediction = ecg_model.predict_proba(
        features
    )

    probability = float(
        prediction[0][1]
    )

    probability = max(
        0.0,
        min(
            1.0,
            probability
        )
    )

    risk_percent = round(
        probability * 100,
        2
    )

    # ---------------------------------------------------
    # Risk classification
    # ---------------------------------------------------

    if risk_percent < 30:

        risk_level = "Low Risk"

    elif risk_percent < 70:

        risk_level = "Moderate Risk"

    else:

        risk_level = "High Risk"

    # ---------------------------------------------------
    # Display result
    # ---------------------------------------------------

    print(
        "\n========== ECG RESULT =========="
    )

    print(
        "Probability :",
        probability
    )

    print(
        "Risk %      :",
        risk_percent
    )

    print(
        "Risk Level  :",
        risk_level
    )

    # ---------------------------------------------------
    # Return result
    # ---------------------------------------------------

    return {

        "probability":
            probability,

        "risk_percent":
            risk_percent,

        "risk_level":
            risk_level

    }


# =======================================================
# TEST
# =======================================================

if __name__ == "__main__":

    result = predict_ecg(
        "uploads/ecg/sample_ecg_high.csv"
    )

    print(
        "\nFinal Result:"
    )

    print(result)