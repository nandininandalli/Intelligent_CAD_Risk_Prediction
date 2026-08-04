from tensorflow.keras.models import load_model

model = load_model("models/echo_cnn.h5")

model.summary()

print("\nInput Shape:", model.input_shape)
print("Output Shape:", model.output_shape)