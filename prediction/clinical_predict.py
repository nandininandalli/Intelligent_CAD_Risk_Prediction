import joblib
import pandas as pd

# =====================================================
# Load Model
# =====================================================

clinical_model = joblib.load("models/clinical_model.pkl")
clinical_imputer = joblib.load("models/clinical_imputer.pkl")
clinical_encoders = joblib.load("models/clinical_label_encoders.pkl")

# =====================================================
# Prediction Function
# =====================================================

def predict_clinical(form_data):

    # -----------------------------
    # Read values from form
    # -----------------------------
    data = {

        "Age": float(form_data["Age"]),
        "Sex": form_data["Sex"],
        "BMI": float(form_data["BMI"]),

        "DM": int(form_data["DM"]),
        "HTN": int(form_data["HTN"]),
        "Current Smoker": int(form_data["Current Smoker"]),
        "FH": int(form_data["FH"]),
        "Typical Chest Pain": int(form_data["Typical Chest Pain"]),

        "Dyspnea": form_data["Dyspnea"],

        "BP": float(form_data["BP"]),
        "PR": float(form_data["PR"]),
        "FBS": float(form_data["FBS"]),
        "LDL": float(form_data["LDL"]),
        "HDL": float(form_data["HDL"]),
        "TG": float(form_data["TG"])

    }

    # -----------------------------
    # Create dataframe
    # -----------------------------
    df = pd.DataFrame([data])

    print("\n===== ORIGINAL INPUT =====")
    print(df)

    # -----------------------------
    # Encode categorical columns
    # -----------------------------
    print("\nLoaded Encoders :", clinical_encoders.keys())

    for col, encoder in clinical_encoders.items():

        if col in df.columns:

            print(f"Encoding {col}")

            print("Before :", df[col].values)

            df[col] = encoder.transform(
                df[col].astype(str)
            )

            print("After :", df[col].values)

    # -----------------------------
    # Match training columns
    # -----------------------------
    expected_columns = list(
        clinical_imputer.feature_names_in_
    )

    for col in expected_columns:

        if col not in df.columns:
            df[col] = 0

    df = df[expected_columns]

    # -----------------------------
    # Impute
    # -----------------------------
    df = pd.DataFrame(

        clinical_imputer.transform(df),

        columns=expected_columns

    )

    print("\n===== FINAL MODEL INPUT =====")
    print(df)

    # -----------------------------
    # Prediction
    # -----------------------------
    probability = clinical_model.predict_proba(df)[0][0]

    risk_percent = round(
        probability * 100,
        2
    )

    print("\nProbability :", probability)
    print("Risk % :", risk_percent)

    # -----------------------------
    # Risk Level
    # -----------------------------
    if risk_percent < 30:

        level = "Low Risk"

    elif risk_percent < 70:

        level = "Moderate Risk"

    else:

        level = "High Risk"

    # -----------------------------
    # Return
    # -----------------------------
    return {

        "risk_percent": risk_percent,

        "risk_level": level,

        "probability": probability

    }