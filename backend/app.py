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

os.makedirs(UPLOAD_DIR, exist_ok=True)

model = load_model(MODEL_PATH)
print("Model loaded")

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

def predict_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    img = preprocess_image(img)
    prob = model.predict(img, verbose=0)[0][0]
    return prob

# ---------------- ROUTES ----------------
@app.get("/")
def root():
    return {"message": "Backend running"}

@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = Image.open(path).convert("RGB")
    img = preprocess_image(img)
    prob = model.predict(img, verbose=0)[0][0]

    label = "DROWSY" if prob > THRESHOLD else "NON-DROWSY"

    return {
        "prediction": label,
        "confidence": round(float(prob), 2)
    }

@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    cap = cv2.VideoCapture(path)
    predictions = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 30 == 0:  # for every ~1 sec
            prob = predict_frame(frame)
            predictions.append(prob)

        frame_count += 1

    cap.release()

    if not predictions:
        return {"error": "No frames processed"}

    avg_prob = float(np.mean(predictions))
    label = "DROWSY" if avg_prob > THRESHOLD else "NON-DROWSY"

    return {
        "prediction": label,
        "average_confidence": round(avg_prob, 2),
        "frames_analyzed": len(predictions)
    }
