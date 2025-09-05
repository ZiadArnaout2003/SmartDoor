import cv2
import numpy as np
import mediapipe as mp
import time
from detect_face import recognize_face,load_face_encodings,start_lock
from detect_fingers import count_fingers
# -------------------------------
# Step 0: Setup MediaPipe Hands
# -------------------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils



import cv2
import time
import mediapipe as mp
from detect_face import recognize_face, load_face_encodings, start_lock
from detect_fingers import count_fingers

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def authenticate_user(PIN=[4,3,5], timeout=20):
    """
    Authenticate a user using face recognition + finger PIN.
    Returns True if authenticated, False otherwise.
    Runs once per call (not infinite loop).
    """

    known_face_encodings, known_face_names = load_face_encodings()
    capture = cv2.VideoCapture(0)

    process_this_frame = True
    face_authenticated = False
    entered = []

    stabilized_fingers = 0
    last_fingers = None
    stable_start = None
    STABLE_TIME = 1  # seconds
    lock_until = 0
    text_start_time = 0
    TEXT_DURATION = 2

    start_time = time.time()
    authenticated = False

    with mp_hands.Hands(min_detection_confidence=0.7,
                        min_tracking_confidence=0.7,
                        max_num_hands=1) as hands:

        while True:
            ret, frame = capture.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            current_time = time.time()

            # # Timeout condition
            # if current_time - start_time > timeout:
            #     print("⏳ Timeout reached")
            #     break

            # Step 1: Face recognition
            if not face_authenticated:
                face_locations, face_names = recognize_face(
                    frame, known_face_encodings, known_face_names, process_this_frame
                )
                process_this_frame = not process_this_frame

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0,255,0), cv2.FILLED)
                    cv2.putText(frame, name, (left+4, bottom-4),
                                cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255), 2)

                    if name != "Unknown":
                        face_authenticated = True
                        text_start_time = current_time
                        print("✅ Face recognized:", name)

            # Step 2: PIN entry
            else:
                if current_time - text_start_time < TEXT_DURATION:
                    cv2.putText(frame, "Enter the PIN:", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if current_time >= lock_until:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(rgb)

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            fingers_up = count_fingers(hand_landmarks)
                            cv2.putText(frame, f"Fingers: {fingers_up}", (50, 100),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                            # Stabilization
                            if fingers_up == last_fingers:
                                if stable_start is None:
                                    stable_start = time.time()
                                elif time.time() - stable_start >= STABLE_TIME:
                                    stabilized_fingers = fingers_up
                            else:
                                last_fingers = fingers_up
                                stable_start = time.time()

                            # Update PIN
                            if stabilized_fingers != 0 and (len(entered) == 0 or stabilized_fingers != entered[-1]):
                                entered.append(stabilized_fingers)
                                print("PIN so far:", entered)

                                if entered == PIN:
                                    print("✅ Access Granted")
                                    authenticated = True
                                    lock_until = start_lock(2)
                                    break
                                elif len(entered) >= len(PIN):
                                    print("❌ Wrong PIN")
                                    entered.clear()
                                    lock_until = start_lock(2)

            cv2.imshow("2-Step Authentication", frame)
            if cv2.waitKey(1) & 0xFF in [27, ord('q')]:
                break

            if authenticated:
                break

    capture.release()
    cv2.destroyAllWindows()
    return authenticated
def main():
    authenticate_user()

if __name__ == "__main__":
    main()