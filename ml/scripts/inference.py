import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import argparse

# CONFIG
IMG_SIZE = 227
MODEL_PATH = "../models/drowsiness_cnn_model.keras"
THRESHOLD = 0.5

# LOAD MODEL
model = load_model(MODEL_PATH)
print("Model loaded")

# LOAD FACE DETECTOR
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# PREPROCESS
def preprocess_image(img):
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# IMAGE INFERENCE
def predict_image(image_path):
    img_cv = cv2.imread(image_path)

    if img_cv is None:
        print("ERROR: Could not read image")
        return

    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        print("No face detected")
        return

    # Take the first detected face
    x, y, w, h = faces[0]
    face = img_cv[y:y+h, x:x+w]

    face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(face_rgb)
    img = preprocess_image(img)

    prob = model.predict(img, verbose=0)[0][0]
    label = "DROWSY" if prob > THRESHOLD else "NON-DROWSY"

    print(f"Prediction: {label}")
    print(f"Confidence: {prob:.2f}")

# VIDEO INFERENCE
def predict_video(video_path, frame_interval=30):
    cap = cv2.VideoCapture(video_path)
    

    if not cap.isOpened():
        print("ERROR: Could not open video")
        return

    frame_count = 0
    predictions = []
    last_label = "Detecting..."
    last_prob = 0.0
    last_color = (255, 255, 255)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                x, y, w, h = faces[0]
                face = frame[y:y+h, x:x+w]

                face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(face_rgb)
                img = preprocess_image(img)

                prob = model.predict(img, verbose=0)[0][0]
                predictions.append(prob)

                last_label = "DROWSY" if prob > THRESHOLD else "NON-DROWSY"
                last_prob = prob
                last_color = (0, 0, 255) if last_label == "DROWSY" else (0, 255, 0)

                # Draw face box
                cv2.rectangle(frame, (x, y), (x+w, y+h), last_color, 2)

        # Draw border + text
        cv2.rectangle(frame, (10, 10), (frame.shape[1]-10, frame.shape[0]-10), last_color, 4)

        cv2.putText(
            frame,
            f"{last_label} ({last_prob:.2f})",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            last_color,
            3
        )

        cv2.imshow("Driver Drowsiness Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    if predictions:
        avg_prob = np.mean(predictions)
        final_label = "DROWSY" if avg_prob > THRESHOLD else "NON-DROWSY"
        print("\nFinal Video Prediction:", final_label)
        print("Average confidence:", round(avg_prob, 2))
        print("Frames analyzed:", len(predictions))
    else:
        print("No valid face frames processed")

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, help="Path to image")
    parser.add_argument("--video", type=str, help="Path to video")

    args = parser.parse_args()

    if args.image:
        predict_image(args.image)
    elif args.video:
        predict_video(args.video)
    else:
        print("Provide --image or --video input")
