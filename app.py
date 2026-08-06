import cv2
import time
import numpy as np

from modules.camera import Camera
from modules.face_detection import FaceDetector
from modules.eye_detection import EyeDetector
from modules.yawn_detection import YawnDetector
from modules.head_pose import HeadPoseDetector
from modules.phone_detection import PhoneDetector
from modules.fatigue_score import FatigueEngine
from modules.alarm import Alarm
from modules.report_generator import ReportGenerator

# ==========================================================
#                   DRIVEGUARD AI v2.0
# ==========================================================

# Dashboard Size
DASHBOARD_WIDTH = 360

# Colors (BGR)
BG = (28, 28, 30)
CARD = (42, 42, 45)
WHITE = (245, 245, 245)
GREEN = (0, 220, 120)
RED = (0, 0, 255)
ORANGE = (0, 165, 255)
YELLOW = (0, 255, 255)
BLUE = (255, 170, 0)
GRAY = (170, 170, 170)

FONT = cv2.FONT_HERSHEY_DUPLEX

# FPS
fps = 0
prev_time = time.time()


# ==========================================================
# Rounded Rectangle
# ==========================================================

def rounded_rect(img, pt1, pt2, color, radius=15, thickness=-1):

    x1, y1 = pt1
    x2, y2 = pt2

    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)

    cv2.circle(img, (x1 + radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, color, thickness)


# ==========================================================
# Draw Card
# ==========================================================

def draw_card(img, x, y, w, h, title, value, color):

    rounded_rect(img, (x, y), (x + w, y + h), CARD)

    cv2.putText(
        img,
        title,
        (x + 15, y + 25),
        FONT,
        0.55,
        GRAY,
        1,
    )

    cv2.putText(
        img,
        value,
        (x + 15, y + 58),
        FONT,
        0.8,
        color,
        2,
    )


# ==========================================================
# Progress Bar
# ==========================================================

def draw_progress(img, x, y, w, h, percent):

    rounded_rect(img, (x, y), (x + w, y + h), (55, 55, 55))

    fill = int((percent / 100) * w)

    if percent < 40:
        color = GREEN
    elif percent < 70:
        color = ORANGE
    else:
        color = RED

    rounded_rect(
        img,
        (x, y),
        (x + fill, y + h),
        color,
    )

    cv2.putText(
        img,
        f"{percent}%",
        (x + w + 15, y + 18),
        FONT,
        0.55,
        WHITE,
        1,
    )


# ==========================================================
# Status Color
# ==========================================================

def status_color(status):

    if status == "SAFE":
        return GREEN

    if status == "WARNING":
        return ORANGE

    return RED
    # ==========================================================
# Dashboard Header
# ==========================================================

def draw_header(canvas, fps, elapsed):

    rounded_rect(
        canvas,
        (15, 15),
        (DASHBOARD_WIDTH - 15, 80),
        (50, 50, 55),
    )

    cv2.putText(
        canvas,
        "DRIVEGUARD AI",
        (30, 48),
        FONT,
        0.9,
        YELLOW,
        2,
    )

    cv2.putText(
        canvas,
        f"FPS : {fps:.1f}",
        (30, 70),
        FONT,
        0.45,
        WHITE,
        1,
    )

    minutes = elapsed // 60
    seconds = elapsed % 60

    cv2.putText(
        canvas,
        f"TIME : {minutes:02}:{seconds:02}",
        (170, 70),
        FONT,
        0.45,
        WHITE,
        1,
    )


# ==========================================================
# Dashboard Cards
# ==========================================================

def draw_dashboard(
        canvas,
        faces,
        eye_status,
        ear,
        blinks,
        yawn_status,
        mar,
        yawns,
        head_direction,
        phone_detected,
        fatigue_score,
        fatigue_status,
):

    y = 100

    draw_card(
        canvas,
        15,
        y,
        330,
        70,
        "Driver",
        "DETECTED" if faces else "NOT FOUND",
        GREEN if faces else RED,
    )

    y += 82

    draw_card(
        canvas,
        15,
        y,
        330,
        70,
        "Eye Status",
        eye_status,
        GREEN if eye_status == "ALERT" else RED,
    )

    y += 82

    draw_card(
        canvas,
        15,
        y,
        160,
        70,
        "EAR",
        f"{ear:.3f}",
        BLUE,
    )

    draw_card(
        canvas,
        185,
        y,
        160,
        70,
        "Blinks",
        str(blinks),
        WHITE,
    )

    y += 82

    draw_card(
        canvas,
        15,
        y,
        160,
        70,
        "MAR",
        f"{mar:.3f}",
        BLUE,
    )

    draw_card(
        canvas,
        185,
        y,
        160,
        70,
        "Yawns",
        str(yawns),
        WHITE,
    )

    y += 82

    draw_card(
        canvas,
        15,
        y,
        330,
        70,
        "Head Direction",
        head_direction,
        ORANGE,
    )

    y += 82

    draw_card(
        canvas,
        15,
        y,
        330,
        70,
        "Phone",
        "DETECTED" if phone_detected else "NOT DETECTED",
        RED if phone_detected else GREEN,
    )

    y += 82

    cv2.putText(
        canvas,
        "Fatigue Score",
        (20, y),
        FONT,
        0.55,
        WHITE,
        1,
    )

    draw_progress(
        canvas,
        20,
        y + 15,
        280,
        20,
        fatigue_score,
    )

    y += 55

    draw_card(
        canvas,
        15,
        y,
        330,
        70,
        "Driver Status",
        fatigue_status,
        status_color(fatigue_status),
    )


# ==========================================================
# Warning Banner
# ==========================================================

def draw_warning(frame, fatigue_status):

    if fatigue_status != "DROWSY":
        return

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, 0),
        (frame.shape[1], 80),
        (0, 0, 255),
        -1,
    )

    frame[:] = cv2.addWeighted(
        overlay,
        0.35,
        frame,
        0.65,
        0,
    )

    cv2.putText(
        frame,
        "⚠ DROWSINESS DETECTED - PLEASE TAKE A BREAK",
        (30, 50),
        FONT,
        0.9,
        WHITE,
        2,
    )
    # ==========================================================
# Main
# ==========================================================

def main():

    global prev_time, fps

    camera = Camera()
    detector = FaceDetector()
    eye_detector = EyeDetector()
    yawn_detector = YawnDetector()
    head_detector = HeadPoseDetector()
    phone_detector = PhoneDetector()
    fatigue_engine = FatigueEngine()
    alarm = Alarm()
    report = ReportGenerator()

    start_time = time.time()

    cv2.namedWindow(
        "DriveGuard AI",
        cv2.WINDOW_NORMAL
    )

    while True:

        frame = camera.read()

        if frame is None:
            break

        # ------------------------------------------
        # Resize camera for better UI
        # ------------------------------------------

        frame = cv2.resize(frame, (960, 720))

        # ------------------------------------------
        # Detection Pipeline
        # ------------------------------------------

        frame, faces = detector.detect(frame)

        ear, blinks, eye_status = eye_detector.detect(frame)

        mar, yawns, yawn_status = yawn_detector.detect(frame)

        head_direction = head_detector.detect(frame)

        frame, phone_detected = phone_detector.detect(frame)

        fatigue_score, fatigue_status = fatigue_engine.calculate(
            eye_status,
            yawn_status,
            head_direction,
            phone_detected,
        )

        report.write(
            faces,
            eye_status,
            yawn_status,
            head_direction,
            phone_detected,
            fatigue_score,
            fatigue_status,
        )

        if fatigue_status == "DROWSY":
            alarm.play_alarm()
        else:
            alarm.stop()

        # ------------------------------------------
        # FPS
        # ------------------------------------------

        current = time.time()

        fps = 1 / (current - prev_time)

        prev_time = current

        elapsed = int(current - start_time)

        # ------------------------------------------
        # Dashboard Canvas
        # ------------------------------------------

        dashboard = np.full(
            (720, DASHBOARD_WIDTH, 3),
            BG,
            dtype=np.uint8,
        )

        draw_header(
            dashboard,
            fps,
            elapsed,
        )
        draw_dashboard(
            dashboard,
            faces,
            eye_status,
            ear,
            blinks,
            yawn_status,
            mar,
            yawns,
            head_direction,
            phone_detected,
            fatigue_score,
            fatigue_status,
        )

        draw_warning(
            frame,
            fatigue_status,
        )

        # ------------------------------------------
        # Combine Dashboard + Camera
        # ------------------------------------------

        output = np.hstack(
            (
                dashboard,
                frame,
            )
        )

        cv2.imshow(
            "DriveGuard AI",
            output,
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == ord("Q") or key == 27:
            break

    camera.release()


if __name__ == "__main__":
    main()