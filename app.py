import cv2

from modules.camera import Camera
from modules.face_detection import FaceDetector
from modules.eye_detection import EyeDetector
from modules.yawn_detection import YawnDetector
from modules.head_pose import HeadPoseDetector
from modules.phone_detection import PhoneDetector
from modules.fatigue_score import FatigueEngine
from modules.alarm import Alarm


def main():

    camera = Camera()
    detector = FaceDetector()
    eye_detector = EyeDetector()
    yawn_detector = YawnDetector()
    head_detector = HeadPoseDetector()
    phone_detector = PhoneDetector()
    fatigue_engine = FatigueEngine()
    alarm = Alarm()

    print("===================================")
    print("       DriveGuard AI Started")
    print("        Press Q to Exit")
    print("===================================")

    while True:

        frame = camera.read()

        if frame is None:
            break

        # ---------------- Face ----------------

        frame, faces = detector.detect(frame)

        # ---------------- Eyes ----------------

        ear, blinks, eye_status = eye_detector.detect(frame)

        # ---------------- Yawn ----------------

        mar, yawns, yawn_status = yawn_detector.detect(frame)

        # ---------------- Head ----------------

        head_direction = head_detector.detect(frame)

        # ---------------- Phone ----------------

        frame, phone_detected = phone_detector.detect(frame)

        # ---------------- Fatigue ----------------

        fatigue_score, fatigue_status = fatigue_engine.calculate(
            eye_status,
            yawn_status,
            head_direction,
            phone_detected
        )

        # ---------------- Alarm ----------------

        if fatigue_status == "DROWSY":
            alarm.play_alarm()

        # ---------------- HUD ----------------

        cv2.putText(
            frame,
            "DriveGuard AI",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
        )

        info = [

            f"Faces : {faces}",

            f"EAR : {ear:.3f}",

            f"Blinks : {blinks}",

            f"Eye Status : {eye_status}",

            f"MAR : {mar:.3f}",

            f"Yawns : {yawns}",

            f"Yawning : {yawn_status}",

            f"Head : {head_direction}",

            f"Phone : {'YES' if phone_detected else 'NO'}",

            f"Fatigue : {fatigue_score}%",

            f"Status : {fatigue_status}"

        ]

        y = 80

        for text in info:

            color = (255, 255, 255)

            if "SAFE" in text:
                color = (0, 255, 0)

            elif "WARNING" in text:
                color = (0, 165, 255)

            elif "DROWSY" in text:
                color = (0, 0, 255)

            cv2.putText(
                frame,
                text,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                color,
                2,
            )

            y += 35

        # ---------------- Emergency Warning ----------------

        if fatigue_status == "DROWSY":

            cv2.rectangle(
                frame,
                (0, 0),
                (frame.shape[1], 70),
                (0, 0, 255),
                -1,
            )

            cv2.putText(
                frame,
                "WAKE UP DRIVER!",
                (180, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (255, 255, 255),
                3,
            )

        cv2.imshow("DriveGuard AI", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == ord("Q") or key == 27:
            break

    camera.release()


if __name__ == "__main__":
    main()