# Sign Language System Controller

## Overview
The **Sign Language System Controller** is an assistive technology project designed to bridge the communication gap between sign language users and those unfamiliar with it.  
Using computer vision and machine learning, the system detects and interprets hand gestures in real-time, translating them into text or commands that can be understood by others or used to control devices.

---

## Objectives
- Enable **real-time sign language recognition** using a camera.
- Provide an **intuitive interface** for communication.
- Demonstrate **gesture-based device control** as a proof of concept.
- Promote inclusivity for the hearing and speech-impaired community.

---

## Features
- **Live Gesture Detection** – Uses a webcam or camera feed.
- **ML-based Gesture Classification** – Pre-trained model stored as a `.pkl` file.
- **Text Output** – Displays recognized signs as readable text.
- **Device Control Mode** – Gestures mapped to control actions.
- **Scalable Dataset Integration** – Can be extended for more sign gestures.

---

## Tech Stack
- **Programming Language:** Python  
- **Libraries & Tools:**  
  - OpenCV (Image processing)    
  - NumPy, Pandas (Data handling)  
- **Hardware:** Standard webcam or external camera
- **Model File:** `.pkl` file containing the trained machine learning model.

## Requirements!!
import cv2
import joblib
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import os
import pyautogui
import time
import subprocess

`using pip install -r requirements.txt `
