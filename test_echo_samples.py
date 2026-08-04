import numpy as np
import cv2

from prediction.echo_predict import predict_echo

images = np.load("datasets/echo/echo_images.npy")
labels = np.load("datasets/echo/echo_labels.npy")

# Find one positive and one negative image
low = np.where(labels == 0)[0][0]
high = np.where(labels == 1)[0][0]

cv2.imwrite("low.jpg", (images[low] * 255).astype(np.uint8))
cv2.imwrite("high.jpg", (images[high] * 255).astype(np.uint8))

print("Actual label:", labels[low])
print(predict_echo("low.jpg"))

print()

print("Actual label:", labels[high])
print(predict_echo("high.jpg"))