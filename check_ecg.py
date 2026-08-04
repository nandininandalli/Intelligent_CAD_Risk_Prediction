from tensorflow.keras.models import load_model

model = load_model("models/ecg_cnn.keras")

model.summary()

print("\nInput Shape:", model.input_shape)
print("Output Shape:", model.output_shape)