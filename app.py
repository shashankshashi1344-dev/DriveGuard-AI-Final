import cv2

from modules.camera import Camera
from modules.face_detection import FaceDetector
from modules.eye_detection import EyeDetector
from modules.yawn_detection import YawnDetector
from modules.head_pose import HeadPoseDetector
from modules.phone_detection import PhoneDetector


def main():

    camera = Camera()
    detector = FaceDetector()
    eye_detector = EyeDetector()
    yawn_detector = YawnDetector()
    head_detector = HeadPoseDetector()
    phone_detector = PhoneDetector()

    print("===================================")
    print("       DriveGuard AI Started")
    print("        Press Q to Exit")
    print("===================================")

    while True:

        frame = camera.read()

        if frame is None:
            break

        # Face Detection
        frame, faces = detector.detect(frame)

        # Eye Detection
        ear, blinks, eye_status = eye_detector.detect(frame)

        # Yawn Detection
        mar, yawns, yawn_status = yawn_detector.detect(frame)

        # Head Pose
        head_direction = head_detector.detect(frame)

        # Phone Detection
        frame, phone_detected = phone_detector.detect(frame)

        # ---------------- HUD ---------------- #

        cv2.putText(
            frame,
            "DriveGuard AI",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Faces : {faces}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        if faces > 0:
            cv2.putText(
                frame,
                "Driver Detected",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

        cv2.putText(
            frame,
            f"EAR : {ear:.3f}",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Blinks : {blinks}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2,
        )

        eye_color = (0, 255, 0) if eye_status == "ALERT" else (0, 0, 255)

        cv2.putText(
            frame,
            f"Eye Status : {eye_status}",
            (20, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            eye_color,
            2,
        )

        cv2.putText(
            frame,
            f"MAR : {mar:.3f}",
            (20, 280),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            f"Yawns : {yawns}",
            (20, 320),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        yawn_color = (0, 255, 0) if yawn_status == "NO" else (0, 0, 255)

        cv2.putText(
            frame,
            f"Yawning : {yawn_status}",
            (20, 360),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            yawn_color,
            2,
        )

        cv2.putText(
            frame,
            f"Head : {head_direction}",
            (20, 400),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 165, 0),
            2,
        )

        phone_text = "DETECTED" if phone_detected else "NOT DETECTED"
        phone_color = (0, 0, 255) if phone_detected else (0, 255, 0)

        cv2.putText(
            frame,
            f"Phone : {phone_text}",
            (20, 440),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            phone_color,
            2,
        )

        cv2.imshow("DriveGuard AI", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == ord("Q") or key == 27:
            break

    camera.release()


if __name__ == "__main__":
    main()