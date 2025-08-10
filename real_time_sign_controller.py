import cv2
import joblib
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import os
import pyautogui
import time
import subprocess  # used only for system apps (e.g., calc.exe)

# Load trained model
model = joblib.load("sign_classifier_knn.pkl")

# Webcam and Hand Detector
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

# Map labels to applications


def perform_action(label):
    print(f"[ACTION] Triggering for: {label}")

    # Apps to open
    SIGN_TO_APP = {
    "a_Palm": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "b_Palm": "calc.exe",
    "c_Palm": "notepad.exe",
    "d_Palm": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.exe",
    "e_Palm": "explorer",
    "k_Palm": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.exe",
    "m_Palm": "taskmgr.exe",
    "h_Back": r'"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE" /s "C:\Users\Nithin\Desktop\major project review 2 (1).pptx"',
}
    # System key actions
    SYSTEM_ACTIONS = {
        "1_Back": lambda: pyautogui.press('left'),          # Previous slide
        "2_Back": lambda: pyautogui.press('right'),         # Next slide
        "4_Back": lambda: pyautogui.press('volumeup'),      # Volume up
        "5_Back": lambda: pyautogui.press('volumedown'),    # Volume down
        "x_Palm": lambda: pyautogui.hotkey('alt', 'f4'),    # Close app
    }

    if label in SYSTEM_ACTIONS:
        try:
            SYSTEM_ACTIONS[label]()  # Call the function
            print(f"[OK] Performed system action: {label}")
        except Exception as e:
            print(f"[ERROR] Failed system action {label} → {e}")
    elif label in SIGN_TO_APP:
        try:
            app_path = SIGN_TO_APP[label]
            print(f"[LAUNCHING] {app_path}")
            try:
                if ".pptx" in app_path or "/s" in app_path:
                    subprocess.Popen(app_path, shell=True)
                elif app_path.endswith(".exe"):
                    subprocess.Popen(app_path)
                else:
                    os.startfile(app_path)
                print(f"[LAUNCHED] {app_path}")
            except Exception as e:
                print(f"[ERROR] Could not open {label} → {e}")

        except Exception as e:
            print(f"[ERROR] Could not open {label} → {e}")
    else:
        print(f"[WARNING] No action mapped for: {label}")

# Normalize landmarks
def get_normalized_landmarks(lmList):
    base_x, base_y = lmList[0][0], lmList[0][1]
    return [(x - base_x, y - base_y) for (x, y, z) in lmList]

# Cooldown mechanism
last_prediction = ""
cooldown_frames = 30
cooldown_counter = 0

while True:
    success, img = cap.read()
    if not success:
        break

    hands, img = detector.findHands(img, flipType=False)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        normalized = get_normalized_landmarks(lmList)
        data = np.array(normalized).flatten().reshape(1, -1)

        prediction = model.predict(data)[0].strip()

        # Show prediction on screen
        cv2.putText(img, f"Detected: {prediction}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Perform app action
        if prediction != last_prediction and cooldown_counter == 0:
            last_prediction = prediction
            cooldown_counter = cooldown_frames
            perform_action(prediction)


        else:
            last_prediction = ""

    if cooldown_counter > 0:
        cooldown_counter -= 1

    cv2.imshow("Live Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
