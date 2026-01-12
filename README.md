backend/    -> FastAPI server and API logic  
frontend/   -> User interface (web/app)  
ml/         -> CNN model, training & prediction code  
data/       -> Dataset used for training  
docs/       -> Project documentation and reports  
README.md   -> Project overview  
.gitignore  -> Ignored files

# Driver Drowsiness Detection System

This project detects whether a driver is **DROWSY** or **NON-DROWSY** using a
Convolutional Neural Network (CNN) trained on face images.

The system has three major parts:

1. **ML Module** – Training and testing the model using Python + TensorFlow  
2. **Backend API** – FastAPI server that loads the trained model  
3. **Frontend** – React UI that uploads images/videos and shows results  

Important:
This project requires **Python 3.10 or 3.11 only**.  
TensorFlow 2.12.1 does NOT work on Python 3.12 / 3.13.

Each major part has its own setup guide:

- ML setup → `ml/README.md`
- Backend setup → `backend/README.md`

Both ML and Backend use their **own virtual environments (venv)** to avoid
dependency conflicts.
