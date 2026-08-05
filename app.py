import cv2
import time

from modules.camera import Camera
from modules.face_detection import FaceDetector
from modules.eye_detection import EyeDetector
from modules.yawn_detection import YawnDetector
from modules.head_pose import HeadPoseDetector
from modules.phone_detection import PhoneDetector
from modules.fatigue_score import FatigueEngine
from modules.alarm import Alarm


def draw_status(frame, text, y, color):
    cv2.putText(
        frame,
        text,
        (20, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        color,
        2,
    )


def main():

    camera = Camera()
    detector = FaceDetector()
    eye_detector = EyeDetector()
    yawn_detector = YawnDetector()
    head_detector = HeadPoseDetector()
    phone_detector = PhoneDetector()
    fatigue_engine = FatigueEngine()
    alarm = Alarm()

    start_time = time.time()

    while True:

        frame = camera.read()

        if frame is None:
            break

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

        if fatigue_status == "DROWSY":
            alarm.play_alarm()

        # ---------------- HUD Background ----------------

        cv2.rectangle(frame, (0, 0), (360, frame.shape[0]), (35, 35, 35), -1)

        cv2.putText(
            frame,
            "DRIVEGUARD AI",
            (20, 40),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (0, 255, 255),
            2,
        )

        draw_status(frame, f"Driver        : {'DETECTED' if faces else 'NOT FOUND'}", 90, (255,255,255))
        draw_status(frame, f"Eye Status    : {eye_status}", 130, (0,255,0) if eye_status=="ALERT" else (0,0,255))
        draw_status(frame, f"EAR           : {ear:.3f}", 170, (255,255,0))
        draw_status(frame, f"Blink Count   : {blinks}", 210, (255,255,255))

        draw_status(frame, f"Yawning       : {yawn_status}", 250, (0,255,0) if yawn_status=="NO" else (0,0,255))
        draw_status(frame, f"MAR           : {mar:.3f}", 290, (255,255,0))
        draw_status(frame, f"Yawn Count    : {yawns}", 330, (255,255,255))

        draw_status(frame, f"Head Pose     : {head_direction}", 370, (255,165,0))

        draw_status(frame, f"Phone         : {'YES' if phone_detected else 'NO'}", 410,
                    (0,0,255) if phone_detected else (0,255,0))

        draw_status(frame, f"Fatigue Score : {fatigue_score}%", 450, (0,255,255))

        status_color = (0,255,0)

        if fatigue_status == "WARNING":
            status_color = (0,165,255)

        elif fatigue_status == "DROWSY":
            status_color = (0,0,255)

        draw_status(frame, f"STATUS        : {fatigue_status}", 490, status_color)

        elapsed = int(time.time() - start_time)

        minutes = elapsed // 60

        seconds = elapsed % 60

        draw_status(frame, f"Session Time  : {minutes:02}:{seconds:02}", 530, (255,255,255))

        if fatigue_status == "DROWSY":

            cv2.rectangle(
                frame,
                (360, 0),
                (frame.shape[1], 70),
                (0,0,255),
                -1,
            )

            cv2.putText(
                frame,
                "WAKE UP DRIVER!",
                (420,45),
                cv2.FONT_HERSHEY_DUPLEX,
                1.1,
                (255,255,255),
                3,
            )

        cv2.imshow("DriveGuard AI", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == ord("Q") or key == 27:
            break

    camera.release()


if __name__ == "__main__":
    main()