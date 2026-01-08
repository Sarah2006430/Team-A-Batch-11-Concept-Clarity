import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)


X_val = np.load("../scripts/X_val.npy")
y_val = np.load("../scripts/y_val.npy")

print("Validation data:", X_val.shape, y_val.shape)


model = load_model("../models/drowsiness_cnn_model.keras")
print("Model loaded successfully")


y_prob = model.predict(X_val)
y_pred = (y_prob > 0.5).astype(int).flatten()

acc = accuracy_score(y_val, y_pred)
print("\nAccuracy:", acc)

print("\nClassification Report:")
print(classification_report(y_val, y_pred, target_names=["Non-Drowsy", "Drowsy"]))


cm = confusion_matrix(y_val, y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Non-Drowsy", "Drowsy"]
)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix - Driver Drowsiness Detection")
plt.show()
