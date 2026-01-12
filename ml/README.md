This module handles feature extraction, model training,
evaluation, and inference for driver state prediction.

## Dataset

We use a publicly available Kaggle dataset for driver drowsiness detection.
The dataset contains labeled images of drivers categorized as:
- Drowsy
- Non-Drowsy

Due to size and licensing constraints, the dataset is not stored in the repository.


# ML Module – Inference & Testing

This module is used to test the trained model directly using `inference.py`.

⚠️ Requirements:
- Python **3.10 or 3.11**
- TensorFlow 2.12.1 compatible environment

---

## Setup

```bash
cd ml
python -m venv ml_env
ml_env\Scripts\Activate.ps1

## INSTALL DEPENDENCIES
pip install -r requirements.txt

## Run Inference
cd scripts
python inference.py --image ../data/images/test1.jpg
python inference.py --video ../data/videos/sample.mp4