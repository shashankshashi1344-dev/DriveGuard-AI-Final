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

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    2,
                )

        return frame, faces