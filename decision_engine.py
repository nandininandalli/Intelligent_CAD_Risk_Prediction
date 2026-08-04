def generate_medical_recommendation(
    age,
    sex,

    clinical,
    ecg,
    echo,
    tmt,

    overall_score,
    risk_level,

    BP=None,
    FBS=None,
    LDL=None,
    HDL=None,
    TG=None,
    BMI=None,
    smoker=None,
    diabetes=None,
    hypertension=None
):

    recommendation = []

    ####################################################
    # Overall CAD Recommendation
    ####################################################

    if overall_score < 35:

        recommendation.append(
            "Overall CAD risk is LOW."
        )

        recommendation.append(
            "Continue annual cardiac screening and maintain a healthy lifestyle."
        )

    elif overall_score < 75:

        recommendation.append(
            "Overall CAD risk is MODERATE."
        )

        recommendation.append(
            "Cardiology consultation is recommended."
        )

    else:

        recommendation.append(
            "Overall CAD risk is HIGH."
        )

        recommendation.append(
            "Immediate cardiology evaluation is strongly advised."
        )

    ####################################################
    # Personalized Medical Advice
    ####################################################

    if age >= 60:
        recommendation.append(
            "Advanced age increases CAD risk. Regular cardiac follow-up is recommended."
        )

    if BMI is not None and BMI >= 30:
        recommendation.append(
            "Obesity is present. Weight reduction through diet and exercise is advised."
        )

    if BP is not None and BP >= 140:
        recommendation.append(
            "Blood pressure is elevated. Strict BP control is recommended."
        )

    if FBS is not None and FBS >= 126:
        recommendation.append(
            "Blood sugar is elevated, suggesting diabetes. Diabetic control is essential."
        )

    if LDL is not None and LDL >= 130:
        recommendation.append(
            "LDL cholesterol is high. Lipid-lowering therapy should be considered."
        )

    if HDL is not None and HDL < 40:
        recommendation.append(
            "HDL cholesterol is low. Regular exercise may help improve HDL."
        )

    if TG is not None and TG >= 200:
        recommendation.append(
            "Triglycerides are elevated. Dietary modification is recommended."
        )

    if smoker:
        recommendation.append(
            "Smoking significantly increases CAD risk. Complete smoking cessation is strongly advised."
        )

    if diabetes:
        recommendation.append(
            "Diabetes is a major cardiovascular risk factor. Maintain HbA1c below target."
        )

    if hypertension:
        recommendation.append(
            "Hypertension should be adequately controlled with medication and lifestyle modification."
        )

    if ecg is not None and ecg >= 60:
        recommendation.append(
            "ECG shows significant abnormalities. Further cardiac evaluation is advised."
        )

    if echo is not None and echo >= 60:
        recommendation.append(
            "Echo findings suggest structural cardiac involvement."
        )

    if tmt is not None and tmt >= 60:
        recommendation.append(
            "Positive TMT suggests exercise-induced ischemia. Coronary angiography may be considered."
        )

    ####################################################
    # Risk Factors
    ####################################################

    risk_factors = []

    if age >= 60:
        risk_factors.append("Advanced age")

    if BMI is not None and BMI >= 30:
        risk_factors.append("Obesity")

    if BP is not None and BP >= 140:
        risk_factors.append("Hypertension")

    if diabetes:
        risk_factors.append("Diabetes Mellitus")

    if smoker:
        risk_factors.append("Smoking")

    if LDL is not None and LDL >= 130:
        risk_factors.append("High LDL")

    if HDL is not None and HDL < 40:
        risk_factors.append("Low HDL")

    if TG is not None and TG >= 200:
        risk_factors.append("High Triglycerides")

    if clinical >= 60:
        risk_factors.append("Clinical model indicates high CAD probability")

    if ecg is not None and ecg >= 60:
        risk_factors.append("ECG abnormalities")

    if echo is not None and echo >= 60:
        risk_factors.append("Echo abnormalities")

    if tmt is not None and tmt >= 60:
        risk_factors.append("Positive TMT")

    ####################################################
    # Lifestyle
    ####################################################

    lifestyle = []
    # Exercise (always recommend)
    lifestyle.append({
        "icon": "fa-person-running",
        "title": "Exercise",
        "description": "30–45 minutes of brisk walking at least five days per week."
    })
    if BMI is not None and BMI >= 30:

        lifestyle.append({

            "icon":"fa-weight-scale",

            "title":"Weight Reduction",

            "description":"Your BMI indicates obesity. Losing even 5–10% body weight can significantly reduce heart disease risk."

        })
        
        
    if BP is not None and BP >= 140:

        lifestyle.append({

            "icon":"fa-heart-pulse",

            "title":"Blood Pressure Control",

            "description":"Reduce salt intake, monitor BP regularly and take antihypertensive medication as prescribed."

        })
    if FBS is not None and FBS >= 126:

        lifestyle.append({

            "icon":"fa-droplet",

            "title":"Blood Sugar Control",

            "description":"Maintain strict diabetic control through diet, medication and regular glucose monitoring."

        })
    if LDL is not None and LDL >= 130:

        lifestyle.append({

                "icon":"fa-apple-whole",

                "title":"Heart Healthy Diet",

                "description":"Reduce fried food, butter and red meat. Increase vegetables, fruits and whole grains."

        })
    if HDL is not None and HDL < 40:

        lifestyle.append({

                    "icon":"fa-dumbbell",

                    "title":"Increase Good Cholesterol",

                    "description":"Regular aerobic exercise and healthy fats like nuts and fish help improve HDL."

        })
    if TG is not None and TG >= 150:

        lifestyle.append({

                    "icon":"fa-cookie-bite",

                     "title":"Reduce Sugar Intake",

                        "description":"Avoid sweets, sugary drinks and refined carbohydrates."

        })
    if smoker:

        lifestyle.append({

        "icon":"fa-ban-smoking",

        "title":"Quit Smoking",

        "description":"Stopping smoking is one of the most effective ways to reduce CAD risk."

        })
    if tmt is not None and tmt >= 70:

        lifestyle.append({

        "icon":"fa-user-doctor",

        "title":"Cardiology Follow-up",

        "description":"Positive TMT indicates possible ischemia. Consult a cardiologist immediately."

        })

    return {

        "medical_recommendation":" ".join(recommendation),

        "risk_factors":risk_factors,

        "lifestyle":lifestyle

    }