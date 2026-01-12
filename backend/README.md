This backend loads the trained ML model and exposes prediction APIs for the frontend.

Requirements:
- Python **3.10 or 3.11**
- TensorFlow 2.12.1

---

## Setup

```bash
cd backend
python -m venv backend_env
backend_env\Scripts\Activate.ps1

## Install:

pip install -r requirements.txt


## Run server:

python -m uvicorn app:app --reload


Server runs at:
http://127.0.0.1:8000