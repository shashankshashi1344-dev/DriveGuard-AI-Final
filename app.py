import cv2

from modules.camera import Camera
from modules.face_detection import FaceDetector
from modules.eye_detection import EyeDetector


def main():

    camera = Camera()

    detector = FaceDetector()

    eye_detector = EyeDetector()

    print("===================================")
    print("      DriveGuard AI Started")
    print("      Press Q to Exit")
    print("===================================")

    while True:

        frame = camera.read()

        if frame is None:
            break

        # Face Detection
        frame, faces = detector.detect(frame)

        # Eye Detection
        ear = eye_detector.detect(frame)

        # Title
        cv2.putText(
            frame,
            "DriveGuard AI",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
        )

        # Face Count
        cv2.putText(
            frame,
            f"Faces : {faces}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        # Driver Detection
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

        # EAR Value
        cv2.putText(
            frame,
            f"EAR : {ear:.3f}",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
        )

        cv2.imshow("DriveGuard AI", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == ord("Q") or key == 27:
            break

    camera.release()


if __name__ == "__main__":
    main()