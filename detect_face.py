import face_recognition
import cv2
import numpy as np
import mediapipe as mp
import time


# -------------------------------
# Step 2: Load known face encodings
# -------------------------------
def load_face_encodings():
    known_face_encodings = []
    known_face_names = []

    faces = {
        "allowed_faces/barackObama.jpg": "Barack Obama",
        "allowed_faces/elonMusk.jpg": "Elon Musk",
        "allowed_faces/tigerWoods.jpg": "Tiger Woods",
        "allowed_faces/ziadImage.jpeg": "Ziad Arnaout"
    }

    for file_path, name in faces.items():
        image = face_recognition.load_image_file(file_path)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)

    return known_face_encodings, known_face_names

# -------------------------------
# Step 3: Face recognition function
# -------------------------------
def recognize_face(frame, known_face_encodings, known_face_names, process_this_frame=True):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_names = []

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

        scaled_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]
    else:
        scaled_locations = []

    return scaled_locations, face_names

# -------------------------------
# Step 4: Lock functions for temporary delays
# -------------------------------
def is_locked(lock_until):
    return time.time() < lock_until

def start_lock(duration_seconds):
    return time.time() + duration_seconds

# -------------------------------
# Step 5: Main 2-step authentication
# -------------------------------

