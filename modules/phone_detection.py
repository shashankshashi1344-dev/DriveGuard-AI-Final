from ultralytics import YOLO
import cv2


class PhoneDetector:

    def __init__(self):

        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            conf=0.45,
            verbose=False
        )

        phone_detected = False

        for result in results:

            for box in result.boxes:

                cls = int(box.cls[0])

                name = self.model.names[cls]

                if name != "cell phone":
                    continue

                phone_detected = True

                confidence = float(box.conf[0]) * 100

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # -----------------------------
                # Outer Glow
                # -----------------------------
                cv2.rectangle(
                    frame,
                    (x1 - 3, y1 - 3),
                    (x2 + 3, y2 + 3),
                    (0, 0, 255),
                    4,
                )

                # -----------------------------
                # Main Rectangle
                # -----------------------------
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 80, 255),
                    2,
                )

                # -----------------------------
                # Label Background
                # -----------------------------
                cv2.rectangle(
                    frame,
                    (x1, y1 - 30),
                    (x1 + 190, y1),
                    (0, 0, 255),
                    -1,
                )

                # -----------------------------
                # Label
                # -----------------------------
                cv2.putText(
                    frame,
                    f"PHONE {confidence:.0f}%",
                    (x1 + 8, y1 - 8),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.55,
                    (255, 255, 255),
                    1,
                )

                # -----------------------------
                # Corner Highlights
                # -----------------------------
                l = 18
                t = 3
                c = (0, 255, 255)

                # Top Left
                cv2.line(frame, (x1, y1), (x1 + l, y1), c, t)
                cv2.line(frame, (x1, y1), (x1, y1 + l), c, t)

                # Top Right
                cv2.line(frame, (x2, y1), (x2 - l, y1), c, t)
                cv2.line(frame, (x2, y1), (x2, y1 + l), c, t)

                # Bottom Left
                cv2.line(frame, (x1, y2), (x1 + l, y2), c, t)
                cv2.line(frame, (x1, y2), (x1, y2 - l), c, t)

                # Bottom Right
                cv2.line(frame, (x2, y2), (x2 - l, y2), c, t)
                cv2.line(frame, (x2, y2), (x2, y2 - l), c, t)

        return frame, phone_detected