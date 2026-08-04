"""
Fusion Engine

Combines Clinical, ECG, Echo and TMT
into one final CAD risk score.
"""


def fuse_predictions(
    clinical=None,
    ecg=None,
    echo=None,
    tmt=None
):

    base_weights = {

        "clinical": 0.60,

        "ecg": 0.15,

        "echo": 0.15,

        "tmt": 0.10

    }

    predictions = {}
    weights = {}

    if clinical is not None:
        predictions["clinical"] = clinical
        weights["clinical"] = base_weights["clinical"]

    if ecg is not None:
        predictions["ecg"] = ecg
        weights["ecg"] = base_weights["ecg"]

    if echo is not None:
        predictions["echo"] = echo
        weights["echo"] = base_weights["echo"]

    if tmt is not None:
        predictions["tmt"] = tmt
        weights["tmt"] = base_weights["tmt"]

    if len(predictions) == 0:
        raise ValueError("No prediction available.")

    total_weight = sum(weights.values())

    final_score = 0

    for model in predictions:

        final_score += (
            predictions[model]
            * (weights[model] / total_weight)
        )

    final_score = round(final_score, 2)

    if final_score < 35:

        risk = "Low Risk"

        recommendation = (
            "Maintain a healthy lifestyle, exercise regularly, "
            "and continue periodic cardiac check-ups."
        )

    elif final_score < 75:

        risk = "Moderate Risk"

        recommendation = (
            "Consult a cardiologist. Lifestyle modification and "
            "additional cardiac investigations are recommended."
        )

    else:

        risk = "High Risk"

        recommendation = (
            "Immediate cardiology consultation is advised. "
            "Further diagnostic evaluation and treatment are recommended."
        )

    return {

        "clinical": clinical,

        "ecg": ecg,

        "echo": echo,

        "tmt": tmt,

        "final_score": final_score,

        "risk_level": risk,

        "recommendation": recommendation

    }