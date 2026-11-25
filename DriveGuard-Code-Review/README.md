# DriveGuard AI

## Real-Time Driver Drowsiness Detection and Monitoring System Using Computer Vision

### Overview

DriveGuard AI is a real-time Driver Monitoring System (DMS) developed using Computer Vision and Artificial Intelligence techniques. The system continuously monitors the driver's behaviour through a webcam and identifies fatigue-related activities such as prolonged eye closure, yawning, abnormal head movement, and mobile phone usage.

The application combines multiple computer vision modules to calculate a fatigue score and classify the driver's condition as **Safe**, **Warning**, or **Drowsy**. When the fatigue level exceeds a predefined threshold, an audible warning is generated to alert the driver. In addition, the application records session information in CSV format for later analysis and visualization.

---

## Problem Statement

Driver fatigue and distraction are among the major causes of road accidents. Existing commercial Driver Monitoring Systems are often integrated only into premium vehicles and require specialized hardware.

The objective of this project is to provide a software-based solution capable of monitoring driver alertness using a standard webcam and open-source computer vision technologies.

---

## Objectives

- Detect the driver's face in real time.
- Monitor eye closure using Eye Aspect Ratio (EAR).
- Detect yawning using Mouth Aspect Ratio (MAR).
- Estimate head orientation to identify distraction.
- Detect mobile phone usage using YOLOv8.
- Calculate an overall fatigue score.
- Generate warning alarms for drowsy drivers.
- Record session data for future analysis.

---

## Features

- Real-time face detection
- Eye blink monitoring
- Yawn detection
- Head pose estimation
- Mobile phone detection
- Fatigue score calculation
- Audio alert system
- CSV report generation
- Streamlit dashboard

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Application Development |
| OpenCV | Image Processing |
| MediaPipe | Face Detection and Face Mesh |
| YOLOv8 | Mobile Phone Detection |
| Streamlit | Dashboard |
| CSV | Session Logging |
| Visual Studio Code | Development Environment |

---

## Project Structure

```text
DriveGuard-AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── camera.py
│   ├── face_detection.py
│   ├── eye_detection.py
│   ├── yawn_detection.py
│   ├── head_pose.py
│   ├── phone_detection.py
│   ├── fatigue_score.py
│   ├── alarm.py
│   └── report_generator.py
│
├── dashboard/
│   └── app.py
│
├── reports/
├── screenshots/
└── yolov8n.pt
```

---

## Software Requirements

- Python 3.11 or later
- OpenCV
- MediaPipe
- Ultralytics YOLOv8
- Streamlit
- Windows 10/11

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/DriveGuard-AI.git
```

Navigate to the project directory:

```bash
cd DriveGuard-AI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Driver Monitoring System:

```bash
python app.py
```

To launch the dashboard:

```bash
streamlit run dashboard/app.py
```

---

## Output

The application provides:

- Continuous driver monitoring
- Eye and yawn detection
- Head pose estimation
- Phone detection
- Fatigue score calculation
- Audio warning alerts
- Session report generation
- Dashboard visualization

---

## Future Enhancements

- Deployment on NVIDIA Jetson devices
- Cloud-based monitoring
- GPS integration
- Database support
- Voice-assisted alerts
- Mobile application
- Improved deep learning models

---

## Author

**Shashank B R**

B.Tech – Computer Science and Engineering

Presidency University

---

## Acknowledgement

This project was developed as part of the NVIDIA AI Internship Program under the guidance of **Dr. Jayachandran A**.

---

## License

This repository is intended for academic learning, internship evaluation, and educational purposes.