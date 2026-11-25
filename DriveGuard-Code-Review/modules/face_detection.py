import cv2
import mediapipe as mp


class FaceDetector:

    def __init__(self):

        self.mp_face = mp.solutions.face_detection

        self.detector = self.mp_face.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.6
        )

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.detector.process(rgb)

        faces = 0

        if results.detections:

            faces = len(results.detections)

            for detection in results.detections:

                bbox = detection.location_data.relative_bounding_box

                h, w, _ = frame.shape

                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)

                confidence = int(detection.score[0] * 100)

                # -------------------------------
                # Outer Glow
                # -------------------------------

                cv2.rectangle(
                    frame,
                    (x - 3, y - 3),
                    (x + width + 3, y + height + 3),
                    (0, 255, 120),
                    3,
                )

                # -------------------------------
                # Main Rectangle
                # -------------------------------

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    2,
                )

                # -------------------------------
                # Top Label Background
                # -------------------------------

                label_width = 160

                cv2.rectangle(
                    frame,
                    (x, y - 30),
                    (x + label_width, y),
                    (0, 180, 0),
                    -1,
                )

                # -------------------------------
                # Label
                # -------------------------------

                cv2.putText(
                    frame,
                    f"DRIVER {confidence}%",
                    (x + 8, y - 9),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.55,
                    (255, 255, 255),
                    1,
                )

                # -------------------------------
                # Corner Highlights
                # -------------------------------

                line = 18
                t = 3

                # Top Left
                cv2.line(frame, (x, y), (x + line, y), (0, 255, 255), t)
                cv2.line(frame, (x, y), (x, y + line), (0, 255, 255), t)

                # Top Right
                cv2.line(frame, (x + width, y), (x + width - line, y), (0, 255, 255), t)
                cv2.line(frame, (x + width, y), (x + width, y + line), (0, 255, 255), t)

                # Bottom Left
                cv2.line(frame, (x, y + height), (x + line, y + height), (0, 255, 255), t)
                cv2.line(frame, (x, y + height), (x, y + height - line), (0, 255, 255), t)

                # Bottom Right
                cv2.line(
                    frame,
                    (x + width, y + height),
                    (x + width - line, y + height),
                    (0, 255, 255),
                    t,
                )

                cv2.line(
                    frame,
                    (x + width, y + height),
                    (x + width, y + height - line),
                    (0, 255, 255),
                    t,
                )

        return frame, faces