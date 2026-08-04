import numpy as np
import pandas as pd
import tensorflow as tf

# -------------------------------------------------------
# Load ECG CNN Model
# -------------------------------------------------------

ecg_model = tf.keras.models.load_model("models/ecg_cnn.keras")


# -------------------------------------------------------
# Preprocess ECG CSV
# -------------------------------------------------------

def preprocess_ecg(csv_path):
    """
    Supports:
    - 1 row x 12 columns
    - Multiple rows x 12 columns
    Converts everything into (1,1000,12)
    """

    # Read CSV without header
    df = pd.read_csv(csv_path, header=None)

    # Convert to numeric
    df = df.apply(pd.to_numeric, errors="coerce")

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Fill NaN with 0
    df = df.fillna(0)

    print("\n========== ECG INPUT ==========")
    print("Original Shape :", df.shape)

    # Must contain 12 columns
    if df.shape[1] < 12:
        raise ValueError(
            f"ECG CSV must contain at least 12 columns. Found {df.shape[1]}"
        )

    # Keep first 12 columns
    ecg = df.iloc[:, :12].values.astype(np.float32)

    # If only one row, repeat it 1000 times
    if ecg.shape[0] == 1:

        ecg = np.repeat(ecg, 1000, axis=0)

    # If less than 1000 rows
    elif ecg.shape[0] < 1000:

        padding = np.zeros(
            (1000 - ecg.shape[0], 12),
            dtype=np.float32
        )

        ecg = np.vstack((ecg, padding))

    # If more than 1000 rows
    elif ecg.shape[0] > 1000:

        ecg = ecg[:1000]

    print("Processed Shape :", ecg.shape)

    # CNN input
    ecg = np.expand_dims(ecg, axis=0)

    print("CNN Shape :", ecg.shape)

    return ecg


# -------------------------------------------------------
# Prediction
# -------------------------------------------------------

def predict_ecg(csv_path):

    ecg = preprocess_ecg(csv_path)

    prediction = ecg_model.predict(ecg, verbose=0)
    print("Raw prediction:", prediction)
    probability = float(prediction[0][0])

    probability = max(0.0, min(1.0, probability))

    risk_percent = round(probability * 100, 2)

    if risk_percent < 30:
        risk_level = "Low Risk"

    elif risk_percent < 70:
        risk_level = "Moderate Risk"

    else:
        risk_level = "High Risk"

    print("\n========== ECG RESULT ==========")
    print("Probability :", probability)
    print("Risk %      :", risk_percent)
    print("Risk Level  :", risk_level)

    return {

        "probability": probability,

        "risk_percent": risk_percent,

        "risk_level": risk_level

    }


# -------------------------------------------------------
# Test
# -------------------------------------------------------

if __name__ == "__main__":

    result = predict_ecg("uploads/ecg/sample.csv")

    print(result)