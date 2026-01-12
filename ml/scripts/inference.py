import argparse
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "drowsiness_cnn_model_fixed.keras")
IMG_SIZE = 227

FRAME_THRESHOLD = 0.4
VIDEO_RATIO_THRESHOLD = 0.35

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def preprocess(img):
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_image(model, img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)

    used_fallback = False

    if len(faces) > 0:
        x, y, w, h = faces[0]
        roi = img[y:y+h, x:x+w]
    else:
        roi = img
        used_fallback = True

    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    input_img = preprocess(roi)

    prob = float(model.predict(input_img, verbose=0)[0][0])
    label = "DROWSY" if prob >= FRAME_THRESHOLD else "NON-DROWSY"

    return label, prob, used_fallback

def run_image(model, path):
    img = cv2.imread(path)
    if img is None:
        print("Unable to read image")
        return

    label, prob, fallback = predict_image(model, img)

    color = (0, 0, 255) if label == "DROWSY" else (0, 255, 0)
    text = f"{label} ({prob:.2f})"

    cv2.putText(img, text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    if fallback:
        cv2.putText(img, "Face not detected - fallback",
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    print("Image Result:")
    print(f"  Raw model probability: {prob:.4f}")
    print(f"  Final label: {label}")

    cv2.imshow("Inference Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def run_video(model, path):
    cap = cv2.VideoCapture(path)
    frame_id = 0
    probs = []

    print("\n--- Frame Log ---")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1
        if frame_id % 5 != 0:
            continue

        label, prob, fallback = predict_image(model, frame)
        probs.append(prob)

        color = (0, 0, 255) if label == "DROWSY" else (0, 255, 0)
        text = f"{label} ({prob:.2f})"

        cv2.putText(frame, text, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        print(f"Frame {frame_id:03d} -> {label} ({prob:.2f})")

        cv2.imshow("Video Inference", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if not probs:
        print("No frames analyzed")
        return

    drowsy_like = sum(1 for p in probs if p >= FRAME_THRESHOLD)
    ratio = drowsy_like / len(probs)
    final = "DROWSY" if ratio >= VIDEO_RATIO_THRESHOLD else "NON-DROWSY"

    print("\n--- Summary ---")
    print(f"Frames analyzed: {len(probs)}")
    print(f"Drowsy-like frames: {drowsy_like}")
    print(f"Drowsy ratio: {ratio:.2f}")
    print(f"Final Video Prediction: {final}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str)
    parser.add_argument("--video", type=str)
    args = parser.parse_args()

    print("Loading model...")
    model = load_model(MODEL_PATH, compile=False)
    print("Model loaded successfully")

    if args.image:
        run_image(model, args.image)
    elif args.video:
        run_video(model, args.video)
    else:
        print("Provide --image or --video")

if __name__ == "__main__":
    main()
