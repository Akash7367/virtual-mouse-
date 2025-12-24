# Virtual Mouse using Hand Gestures

This project is a **virtual mouse** that lets you control the system cursor using **hand gestures** captured from your webcam. It uses **Python**, **OpenCV**, and **MediaPipe** for real‑time hand tracking, and an automation library (like PyAutoGUI) to perform mouse actions such as move, click, drag, and scroll. [web:6][web:7][web:15]

## Features

- Real‑time hand tracking using MediaPipe Hands. [web:17]
- Control mouse cursor using fingertip position.
- Gesture‑based left click, right click, drag, and (optionally) scroll. [web:6][web:13]
- Simple Python script that runs on a standard webcam.
- Easily customizable gestures and sensitivity in code. [web:6]

## Technologies Used

- **Python 3.x**
- **OpenCV (`opencv-python`)** – webcam capture and image processing. [web:1]
- **MediaPipe Hands (`mediapipe`)** – hand landmark detection (21 points). [web:17]
- **PyAutoGUI** (or similar) – to move the cursor and perform clicks. [web:9]
- **NumPy** – coordinate and distance calculations. [web:6]

## Installation

1. **Clone the repository**

2. **(Optional) Create a virtual environment**

3. **Install dependencies**
Make sure Python 3.7+ is installed. [web:1]
If `requirements.txt` is not present, install manually:

## Usage

1. Connect a webcam (default index is `0`). [web:7]
2. Run the main script (update the filename if your script is different):
3. A window will open with your webcam feed and hand landmarks drawn on it. Move your hand in front of the camera to control the cursor. [web:6]
4. Perform the configured gestures to click, drag, or scroll.
5. Press `q` or `Esc` in the OpenCV window to exit. [web:1][web:6]

## How It Works

1. **Capture frames** from the webcam using OpenCV. [web:1]
2. **Detect hand landmarks** (21 points) in each frame using MediaPipe Hands. [web:17]
3. **Map fingertip coordinates** (usually index finger tip) from camera space to screen coordinates using the screen resolution and an active interaction region. [web:6][web:13]
4. **Recognize gestures** by checking distances and relative positions between fingers (for example thumb–index pinch for click). [web:6][web:13]
5. **Trigger mouse events** (move, click, drag, scroll) via PyAutoGUI. [web:9]

## Example Gesture Mapping

Update this table to match your exact gestures:

| Gesture                     | Description                                | Mouse Action      |
|----------------------------|--------------------------------------------|-------------------|
| Index finger up            | Track index fingertip                      | Move cursor       |
| Thumb–index pinch          | Distance below a threshold                 | Left click        |
| Index + middle finger up   | Two fingers extended                       | Right click       |
| Pinch and move             | Hold pinch and move                        | Drag and drop     |
| Thumb–middle pinch + move  | Thumb and middle close, vertical movement  | Scroll up / down  |

These are common patterns used in virtual mouse systems with MediaPipe. [web:6][web:13][web:15]

## Configuration

You can tweak several parameters inside the script:

- **Camera index** (default `0`). [web:7]
- **Frame reduction / active area** to limit the region used for cursor mapping. [web:6]
- **Smoothing factor** for smoother cursor movement. [web:6]
- **Click distance thresholds** for pinch detection. [web:6][web:13]
- **Model complexity** in MediaPipe Hands for better accuracy vs speed. [web:17]

## Project Structure

Adapt this to match your repository layout:


This layout is similar to other MediaPipe/OpenCV virtual mouse projects. [web:6][web:19]

## Future Improvements

- Multi‑hand support (different gestures with both hands). [web:17]
- Better gesture recognition using a custom ML model on landmark data. [web:5]
- On‑screen overlay UI with gesture indicators. [web:16]
- Additional controls (volume, media, window management). [web:15]

Feel free to edit the script name (`virtual_mouse.py`), gestures, and feature list so they perfectly match your actual implementation.
# Virtual Mouse using Hand Gestures


