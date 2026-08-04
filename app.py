from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session
)

import os
from werkzeug.utils import secure_filename

from prediction.clinical_predict import predict_clinical
from prediction.ecg_predict import predict_ecg
from prediction.echo_predict import predict_echo
from prediction.tmt_predict import predict_tmt
from prediction.fusion import fuse_predictions
from decision_engine import generate_medical_recommendation
import sqlite3

#########################################################
# Flask App
#########################################################

app = Flask(__name__)

app.secret_key = "cardiovision_ai_secret_key"
def create_history_table():

    conn = sqlite3.connect("cad_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        patient_id TEXT,
        patient_name TEXT,
        date TEXT,
        age INTEGER,
        gender TEXT,

        clinical REAL,
        ecg REAL,
        echo REAL,
        tmt REAL,

        overall_score REAL,
        risk_level TEXT,

        recommendation TEXT
    )
    """)

    conn.commit()
    conn.close()

#########################################################
# Login Credentials
#########################################################

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


#########################################################
# Upload Folder
#########################################################

UPLOAD_FOLDER = "uploads"

ECG_FOLDER = os.path.join(UPLOAD_FOLDER, "ecg")
ECHO_FOLDER = os.path.join(UPLOAD_FOLDER, "echo")

os.makedirs(ECG_FOLDER, exist_ok=True)
os.makedirs(ECHO_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


#########################################################
# Login Page
#########################################################

@app.route("/")
def home():

    if "user" in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html")


#########################################################
# Login Authentication
#########################################################

@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

        session["user"] = username

        return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
        error="Invalid Username or Password"
    )


#########################################################
# Dashboard
#########################################################

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("home"))

    return render_template(
        "dashboard.html",
        username=session["user"]
    )


#########################################################
# Logout
#########################################################

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


#########################################################
# Prediction
#########################################################
# -----------------------------
# Clinical Assessment Page
# -----------------------------
@app.route("/clinical")
def clinical():

    if "user" not in session:
        return redirect("/")

    return render_template("clinical.html")
@app.route("/result")
def result():

    if "prediction_result" not in session:
        return redirect(url_for("clinical"))

    return render_template(
        "result.html",
        result=session["prediction_result"]
    )
@app.route("/history")
def history():

    conn = sqlite3.connect("cad_database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM prediction_history
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        history=history
    )
@app.route("/delete_prediction/<int:id>")
def delete_prediction(id):
    conn = sqlite3.connect("cad_database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM prediction_history WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("history"))
@app.route("/report")
def report():

    if "prediction_result" not in session:
        return redirect("/clinical")

    return render_template(
        "report.html",
        result=session["prediction_result"]
    )
@app.route("/predict", methods=["POST"])
def predict():
    print(request.form)
    print(request.files)
    try:

        #################################################
        # Clinical Prediction
        #################################################

        clinical_result = predict_clinical(request.form)

        clinical_score = clinical_result["risk_percent"]


        #################################################
        # ECG Prediction
        #################################################

        ecg_score = None

        if "ecg_file" in request.files:

            ecg = request.files["ecg_file"]

            if ecg.filename != "":

                filename = secure_filename(ecg.filename)

                path = os.path.join(ECG_FOLDER, filename)

                ecg.save(path)

                ecg_result = predict_ecg(path)

                ecg_score = ecg_result["risk_percent"]


        #################################################
        # Echo Prediction
        #################################################

        echo_score = None

        if "echo_file" in request.files:

            echo = request.files["echo_file"]

            if echo.filename != "":

                filename = secure_filename(echo.filename)

                path = os.path.join(ECHO_FOLDER, filename)

                echo.save(path)

                echo_result = predict_echo(path)

                echo_score = echo_result["risk_percent"]

        #################################################
        # TMT Prediction
        #################################################

        tmt_score = None

        try:

            rest_hr = request.form.get("rest_hr", "").strip()
            max_hr = request.form.get("max_hr", "").strip()
            hr_recovery = request.form.get("hr_recovery", "").strip()
            max_speed = request.form.get("max_speed", "").strip()
            avg_vo2 = request.form.get("avg_vo2", "").strip()
            duration = request.form.get("duration", "").strip()

            # Predict TMT only if ALL TMT values are entered
            if all([
                rest_hr,
                max_hr,
                hr_recovery,
                max_speed,
                avg_vo2,
                duration
            ]):

                print("\nRunning TMT Prediction...")

                tmt_result = predict_tmt(
                    age=float(request.form["Age"]),
                    sex=request.form["Sex"],
                    weight=float(request.form["weight"]),
                    height=float(request.form["height"]),
                    rest_hr=float(rest_hr),
                    max_hr=float(max_hr),
                    hr_recovery=float(hr_recovery),
                    max_speed=float(max_speed),
                    avg_vo2=float(avg_vo2),
                    duration=float(duration)
                )

                tmt_score = tmt_result["risk_percent"]

            else:

                print("\nTMT values not provided. Skipping TMT prediction.")

        except Exception as e:

            print("\nTMT Prediction Failed")
            print(e)

            tmt_score = None
        #################################################
        # Fusion
        #################################################

        final_result = fuse_predictions(

            clinical=clinical_score,

            ecg=ecg_score,

            echo=echo_score,

            tmt=tmt_score

        )

        print("\n========== INDIVIDUAL SCORES ==========")
        print("Clinical :", clinical_score)
        print("ECG      :", ecg_score)
        print("Echo     :", echo_score)
        print("TMT      :", tmt_score)
        #################################################
        # Return Result
        #################################################
        
        medical_plan = generate_medical_recommendation(

        age=float(request.form["Age"]),
        sex=request.form["Sex"],

        clinical=clinical_score,
        ecg=ecg_score,
        echo=echo_score,
        tmt=tmt_score,

        overall_score=final_result["final_score"],
        risk_level=final_result["risk_level"],

        BP=float(request.form["BP"]),
        FBS=float(request.form["FBS"]),
        LDL=float(request.form["LDL"]),
        HDL=float(request.form["HDL"]),
        TG=float(request.form["TG"]),
        BMI=float(request.form["BMI"]),

        smoker=bool(int(request.form["Current Smoker"])),
        diabetes=bool(int(request.form["DM"])),
        hypertension=bool(int(request.form["HTN"]))
    )
        print("MEDICAL PLAN =")
        print(medical_plan)
        result_data = {

    # ----------------------------
    # Patient Details
    # ----------------------------
            "patient_id": request.form.get("patient_id"),
            "patient_name": request.form.get("patient_name"),
            "age": request.form.get("Age"),
            "sex": request.form.get("Sex"),
            "phone": request.form.get("phone"),
            "date": request.form.get("date"),

            "weight": request.form.get("weight"),
            "height": request.form.get("height"),
            "bmi": request.form.get("BMI"),

            "bp": request.form.get("BP"),
            "pr": request.form.get("PR"),

            "fbs": request.form.get("FBS"),
            "ldl": request.form.get("LDL"),
            "hdl": request.form.get("HDL"),
            "tg": request.form.get("TG"),

    # ----------------------------
    # Prediction Scores
    # ----------------------------
            "clinical": clinical_score,
            "ecg": ecg_score,
            "echo": echo_score,
            "tmt": tmt_score,

    # ----------------------------
    # Final AI Decision
    # ----------------------------
            "overall_score": final_result["final_score"],
            "risk_level": final_result["risk_level"],
            "recommendation": final_result["recommendation"],

    # ----------------------------
    # AI Recommendation Engine
    # ----------------------------
            "medical_recommendation": medical_plan["medical_recommendation"],
            "risk_factors": medical_plan["risk_factors"],
            "lifestyle": medical_plan["lifestyle"]
        }
        print("\n========== RESULT DATA ==========")
        print(result_data)
        print("medical_recommendation =", result_data.get("medical_recommendation"))
        print("=================================\n")

        session["prediction_result"] = result_data
        print("\n===== JSON SENT TO BROWSER =====")
        print(result_data)
        conn = sqlite3.connect("cad_database.db")
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO prediction_history
        (
        patient_id,
        patient_name,
        date,
        age,
        gender,
        clinical,
        ecg,
        echo,
        tmt,
        overall_score,
        risk_level,
        recommendation
        )
        
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        
        (
        
        result_data["patient_id"],
        result_data["patient_name"],
        result_data["date"],
        result_data["age"],
        result_data["sex"],
        result_data["clinical"],
        result_data["ecg"],
        result_data["echo"],
        result_data["tmt"],
        result_data["overall_score"],
        result_data["risk_level"],
        result_data["medical_recommendation"]
        
        ))
        
        conn.commit()
        conn.close()
        return jsonify({

    "success": True,

    **result_data,
    "name": request.form["patient_name"],
    "age": float(request.form["Age"]),
    "sex": request.form["Sex"],

    "BP": float(request.form["BP"]),
    "FBS": float(request.form["FBS"]),
    "LDL": float(request.form["LDL"]),
    "HDL": float(request.form["HDL"]),
    "TG": float(request.form["TG"]),
    "BMI": float(request.form["BMI"]),

    "smoker": bool(int(request.form["Current Smoker"])),
    "diabetes": bool(int(request.form["DM"])),
    "hypertension": bool(int(request.form["HTN"]))

})

        

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Clinical :", clinical_score)
        print("ECG      :", ecg_score)
        print("Echo     :", echo_score)
        print("TMT      :", tmt_score)
        print("Final    :", final_result["final_score"])
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


#########################################################
# Run
#########################################################
create_history_table()

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )