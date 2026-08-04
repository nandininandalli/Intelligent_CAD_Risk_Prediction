def fuse_predictions(clinical, ecg=None, echo=None, tmt=None):
    """
    Clinical = 60%
    ECG      = 15%
    Echo     = 15%
    TMT      = 10%

    If ECG/Echo/TMT are missing, their weights are
    redistributed among the available optional models.
    """

    clinical_weight = 0.60
    optional_weight = 0.40

    score = clinical * clinical_weight

    available = []

    if ecg is not None:
        available.append(("ecg", ecg, 0.15))

    if echo is not None:
        available.append(("echo", echo, 0.15))

    if tmt is not None:
        available.append(("tmt", tmt, 0.10))

    # Only clinical available
    if len(available) == 0:
        final_score = round(clinical, 2)

    else:
        total = sum(weight for _, _, weight in available)

        for _, value, weight in available:

            redistributed = optional_weight * weight / total

            score += value * redistributed

        final_score = round(score, 2)

    # Risk Level
    if final_score < 30:
        risk_level = "Low Risk"

    elif final_score < 70:
        risk_level = "Moderate Risk"

    else:
        risk_level = "High Risk"

    # Recommendation
    if risk_level == "Low Risk":
        recommendation = (
            "Maintain a healthy lifestyle and continue regular check-ups."
        )

    elif risk_level == "Moderate Risk":
        recommendation = (
            "Consult a cardiologist for further evaluation."
        )

    else:
        recommendation = (
            "Immediate cardiology consultation is strongly recommended."
        )

    return {
        "final_score": final_score,
        "risk_level": risk_level,
        "recommendation": recommendation
    }