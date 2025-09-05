# SmartDoor 🔐  

SmartDoor is a **2-step authentication system** that combines **face recognition** and **finger-based PIN entry** using computer vision.  
The project leverages **OpenCV**, **MediaPipe**, and **face_recognition** to create a secure and intuitive access control mechanism.  

---

## 🚀 Features
- **Face Recognition**: Identifies registered users in real time.  
- **Hand Gesture PIN**: Enter a numeric PIN by showing fingers to the camera.  
- **Two-Factor Authentication**: Both face + correct PIN are required to unlock.  
- **Stabilized Input**: Finger counts are stabilized to reduce noise.  
- **Timeout & Lock**: Prevents brute-force attempts with delays.  

---

## 🛠️ Tech Stack
- **Python 3.10+**  
- [OpenCV](https://opencv.org/) – Image processing & webcam capture  
- [MediaPipe Hands](https://developers.google.com/mediapipe) – Finger detection  
- [face_recognition](https://github.com/ageitgey/face_recognition) – Face detection & encoding  
- **NumPy** – Array operations  

---

## 📂 Project Structure

SmartDoor/
│── main.py                 # Entry point – runs authentication
│── detect_face.py           # Face recognition logic
│── detect_fingers.py        # Finger counting logic
│── allowed_faces/           # Store known faces here
│── env/                     # Virtual environment (ignored in git)
│── __pycache__/             # Cache files (ignored in git)

## ⚙️ Installation

## Clone the repo:

git clone https://github.com/ZiadArnaout2003/SmartDoor.git
cd SmartDoor


## Create a virtual environment:

python -m venv env
source env/bin/activate   # On Linux/Mac
env\Scripts\activate      # On Windows


## Install dependencies:

pip install -r requirements.txt


Add your face images inside allowed_faces/.

## ▶️ Usage

Run the authentication system:

python main.py


## Steps:

Look at the camera – if your face matches a registered user, proceed.

Show your PIN sequence using fingers (e.g., [4, 3, 5]).

If both checks pass ✅, access is granted.

## 🔒 Security Notes

PIN is customizable in main.py (PIN=[4,3,5]).

Add multiple users by saving their face encodings in allowed_faces/.

Timeout can be used to prevent repeated wrong attempts.
