import os
import random
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# CHANGE THIS PATH according to your system
DATASET_PATH = r"C:\Users\marsa\datasets-A\Driver Drowsiness Dataset (DDD)"

DROWSY_DIR = os.path.join(DATASET_PATH, "Drowsy")
NON_DROWSY_DIR = os.path.join(DATASET_PATH, "Non Drowsy")

print("Drowsy folder exists:", os.path.exists(DROWSY_DIR))
print("Non-drowsy folder exists:", os.path.exists(NON_DROWSY_DIR))

drowsy_images = os.listdir(DROWSY_DIR)
non_drowsy_images = os.listdir(NON_DROWSY_DIR)

print("Number of drowsy images:", len(drowsy_images))
print("Number of non-drowsy images:", len(non_drowsy_images))
print("Total images:", len(drowsy_images) + len(non_drowsy_images))

plt.figure(figsize=(10, 3))

sample_drowsy = random.sample(drowsy_images, 5)

for i, img_name in enumerate(sample_drowsy):
    img_path = os.path.join(DROWSY_DIR, img_name)
    img = Image.open(img_path)
    
    plt.subplot(1, 5, i+1)
    plt.imshow(img)
    plt.title("Drowsy")
    plt.axis("off")

plt.show()

sample_image_path = os.path.join(DROWSY_DIR, drowsy_images[0])
img = Image.open(sample_image_path)

print("Image size (width, height):", img.size)
print("Image mode (RGB expected):", img.mode)

img_array = np.array(img)
print("Image array shape:", img_array.shape)
