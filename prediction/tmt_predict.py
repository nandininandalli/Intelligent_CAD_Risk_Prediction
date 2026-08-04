import joblib
import numpy as np

# ----------------------------------------------------
# Load Model
# ----------------------------------------------------

tmt_model = joblib.load("models/tmt_model.pkl")
tmt_scaler = joblib.load("models/tmt_scaler.pkl")


# ----------------------------------------------------
# Prediction Function
# ----------------------------------------------------

def predict_tmt(
    age,
    sex,
    weight,
    height,
    rest_hr,
    max_hr,
    hr_recovery,
    max_speed,
    avg_vo2,
    duration
):

    # -----------------------------------------
    # Encode Sex
    # -----------------------------------------

    if isinstance(sex, str):

        sex = sex.strip().lower()

        if sex in ["male", "m"]:
            sex = 1
        else:
            sex = 0

    else:
        sex = int(sex)

    # -----------------------------------------
    # Feature Order
    # MUST MATCH train_tmt.py
    # -----------------------------------------

    features = np.array([[
        float(age),
        float(sex),
        float(weight),
        float(height),
        float(rest_hr),
        float(max_hr),
        float(hr_recovery),
        float(max_speed),
        float(avg_vo2),
        float(duration)
    ]])

    print("\n========== TMT INPUT ==========")
    print(features)

    # -----------------------------------------
    # Scale
    # -----------------------------------------

    features = tmt_scaler.transform(features)

    print("\n========== TMT SCALED ==========")
    print(features)

    # -----------------------------------------
    # Predict Probability
    # -----------------------------------------

    probability = float(
        tmt_model.predict_proba(features)[0][1]
    )

    risk_percent = round(probability * 100, 2)

    # -----------------------------------------
    # Risk Level
    # -----------------------------------------

    if risk_percent < 30:
        risk_level = "Low Risk"

    elif risk_percent < 70:
        risk_level = "Moderate Risk"

    else:
        risk_level = "High Risk"

    print("\n========== TMT RESULT ==========")
    print("Probability :", probability)
    print("Risk %      :", risk_percent)
    print("Risk Level  :", risk_level)

    return {

        "probability": probability,

        "risk_percent": risk_percent,

        "risk_level": risk_level

    }


# ----------------------------------------------------
# Testing
# ----------------------------------------------------

if __name__ == "__main__":

    result = predict_tmt(

        age=25,

        sex="Male",

        weight=65,

        height=168,

        rest_hr=65,

        max_hr=170,

        hr_recovery=35,

        max_speed=12,

        avg_vo2=42,

        duration=900

    )

    print(result)