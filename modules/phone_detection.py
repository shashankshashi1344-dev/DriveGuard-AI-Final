from ultralytics import YOLO


class PhoneDetector:

    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            conf=0.40,
            verbose=False
        )

        phone_detected = False

        for result in results:

            for box in result.boxes:

                cls = int(box.cls[0])

                name = self.model.names[cls]

                if name == "cell phone":

                    phone_detected = True

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    import cv2

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 255),
                        2,
                    )

                    cv2.putText(
                        frame,
                        "PHONE DETECTED",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2,
                    )

        return frame, phone_detected