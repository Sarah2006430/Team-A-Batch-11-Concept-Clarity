from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# ---------------- CONFIG ----------------
IMG_SIZE = 227
MODEL_PATH = "../ml/models/drowsiness_cnn_model.keras"
UPLOAD_DIR = "uploads"
THRESHOLD = 0.5
FRAME_INTERVAL = 30  # ~1 frame per second

os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- LOAD MODEL ----------------
model = load_model(MODEL_PATH)
print("Model loaded")

# ---------------- LOAD FACE DETECTOR ----------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------- FASTAPI APP ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HELPERS ----------------
def preprocess_image(img):
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def predict_face(face_bgr):
    face_rgb = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(face_rgb)
    img = preprocess_image(img)
    prob = model.predict(img, verbose=0)[0][0]
    return float(prob)


# ---------------- ROUTES ----------------
@app.get("/")
def root():
    return {"message": "Backend running"}


# ---------- IMAGE PREDICTION ----------
@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img_cv = cv2.imread(path)
    if img_cv is None:
        return {"error": "Could not read image"}

    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return {"error": "No face detected"}

    # Take first detected face
    x, y, w, h = faces[0]
    face = img_cv[y:y+h, x:x+w]

    prob = predict_face(face)
    label = "DROWSY" if prob > THRESHOLD else "NON-DROWSY"

    return {
        "prediction": label,
        "confidence": round(prob, 2)
    }


# ---------- VIDEO PREDICTION ----------
@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return {"error": "Could not open video"}

    predictions = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % FRAME_INTERVAL == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                x, y, w, h = faces[0]
                face = frame[y:y+h, x:x+w]

                prob = predict_face(face)

                # Ignore uncertain frames
                if 0.3 < prob < 0.7:
                    frame_count += 1
                    continue

                predictions.append(prob)

        frame_count += 1

    cap.release()

    if not predictions:
        return {"error": "No valid face frames processed"}

    avg_prob = float(np.mean(predictions))
    label = "DROWSY" if avg_prob > THRESHOLD else "NON-DROWSY"

    return {
        "prediction": label,
        "average_confidence": round(avg_prob, 2),
        "frames_analyzed": len(predictions)
    }
