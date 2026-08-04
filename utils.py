import joblib
from tensorflow.keras.models import load_model

# Clinical
clinical_model = joblib.load("models/clinical_model.pkl")
clinical_imputer = joblib.load("models/clinical_imputer.pkl")
# ECGclinical_encoder = joblib.load("models/clinical_label_encoders.pkl")
ecg_model = load_model("models/ecg_cnn.keras")

# Echo
from tensorflow.keras.models import load_model

echo_model = load_model("models/echo_cnn.keras")
# TMT
tmt_model = joblib.load("models/tmt_model.pkl")
tmt_scaler = joblib.load("models/tmt_scaler.pkl")