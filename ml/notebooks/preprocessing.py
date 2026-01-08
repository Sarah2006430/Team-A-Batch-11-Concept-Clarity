import os
import random
from PIL import Image
import numpy as np 
from sklearn.model_selection import train_test_split

DATASET_PATH = r"C:\Users\marsa\datasets-A\Driver Drowsiness Dataset (DDD)"

DROWSY_DIR = os.path.join(DATASET_PATH, "Drowsy")
NON_DROWSY_DIR = os.path.join(DATASET_PATH, "Non Drowsy")

SAMPLES_PER_CLASS = 500   
IMG_SIZE = (227, 227)

def load_images(folder, label, limit):
    images = []
    labels = []
    files = os.listdir(folder)
    selected = random.sample(files, min(limit, len(files)))
    
    for fname in selected:
        path = os.path.join(folder, fname)
        img = Image.open(path).convert("RGB")
        img = img.resize(IMG_SIZE)
        arr = np.array(img, dtype=np.float32) / 255.0  # ***normalization**
        images.append(arr)
        labels.append(label)
        
    return images, labels

X_drowsy, y_drowsy = load_images(DROWSY_DIR, label=1, limit=SAMPLES_PER_CLASS)
X_non, y_non = load_images(NON_DROWSY_DIR, label=0, limit=SAMPLES_PER_CLASS)

X = np.array(X_drowsy + X_non)
y = np.array(y_drowsy + y_non)

print("Loaded images:", X.shape)
print("Loaded labels:", y.shape)

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("X_train:", X_train.shape)
print("y_train:", y_train.shape)
print("X_val:", X_val.shape)
print("y_val:", y_val.shape)

print("Pixel range (train):", X_train.min(), "to", X_train.max())
print("Class balance (train):", np.bincount(y_train))
print("Class balance (val):", np.bincount(y_val))
np.save("../scripts/X_train.npy", X_train)
np.save("../scripts/y_train.npy", y_train)
np.save("../scripts/X_val.npy", X_val)
np.save("../scripts/y_val.npy", y_val)

print("Preprocessed data saved to ml/scripts/")

