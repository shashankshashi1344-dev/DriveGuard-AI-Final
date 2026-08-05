import cv2

from modules.camera import Camera
from modules.face_detection import FaceDetector
from modules.eye_detection import EyeDetector
from modules.yawn_detection import YawnDetector
from modules.head_pose import HeadPoseDetector
from modules.phone_detection import PhoneDetector
from modules.fatigue_score import FatigueEngine


def main():

    camera = Camera()
    detector = FaceDetector()
    eye_detector = EyeDetector()
    yawn_detector = YawnDetector()
    head_detector = HeadPoseDetector()
    phone_detector = PhoneDetector()
    fatigue_engine = FatigueEngine()

    print("===================================")
    print("       DriveGuard AI Started")
    print("        Press Q to Exit")
    print("===================================")

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
            phone_detected
        )

        cv2.putText(frame, "DriveGuard AI",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,255),
                    2)

        info = [
            f"Faces : {faces}",
            f"EAR : {ear:.3f}",
            f"Blinks : {blinks}",
            f"Eye : {eye_status}",
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

            color = (255,255,255)

            if "DROWSY" in text:
                color = (0,0,255)

            elif "WARNING" in text:
                color = (0,165,255)

            elif "SAFE" in text:
                color = (0,255,0)

            cv2.putText(
                frame,
                text,
                (20,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                color,
                2,
            )

            y += 35

        cv2.imshow("DriveGuard AI", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == ord("Q") or key == 27:
            break

    camera.release()


if __name__ == "__main__":
    main()