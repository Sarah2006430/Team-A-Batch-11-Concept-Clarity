from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# ---------------- CONFIG ----------------
IMG_SIZE = 227
MODEL_PATH = "../ml/models/drowsiness_cnn_model_fixed.keras"
UPLOAD_DIR = "uploads"
THRESHOLD = 0.4

FRAME_INTERVAL = 30
VIDEO_RATIO_THRESHOLD = 0.35

os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- LOAD MODEL ----------------
model = load_model(MODEL_PATH, compile=False)
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
def predict_face(face_bgr):
    # EXACTLY same as inference.py
    face_rgb = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2RGB)
    img = cv2.resize(face_rgb, (IMG_SIZE, IMG_SIZE))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
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

    if len(faces) > 0:
        x, y, w, h = faces[0]
        face = img_cv[y:y+h, x:x+w]
    else:
        face = img_cv  # fallback like inference.py

    prob = predict_face(face)
    label = "DROWSY" if prob >= THRESHOLD else "NON-DROWSY"

    print("BACKEND IMAGE PROB:", prob)

    return {
        "raw_probability": prob,
        "prediction": label,
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

    probs = []
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
            else:
                face = frame

            prob = predict_face(face)
            probs.append(prob)

        frame_count += 1

    cap.release()

    if not probs:
        return {"error": "No frames processed"}

    drowsy_like = sum(1 for p in probs if p >= THRESHOLD)
    ratio = drowsy_like / len(probs)
    label = "DROWSY" if ratio >= VIDEO_RATIO_THRESHOLD else "NON-DROWSY"

    print("BACKEND VIDEO AVG:", sum(probs) / len(probs))

    return {
        "raw_probability": float(sum(probs) / len(probs)),
        "prediction": label,
        "frames_analyzed": len(probs),
    }
