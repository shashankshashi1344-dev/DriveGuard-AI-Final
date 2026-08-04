import mediapipe as mp
import cv2
import math


class YawnDetector:

    def __init__(self):

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True
        )

        # Mouth landmarks
        self.MOUTH = [13, 14, 78, 308]

        self.YAWN_THRESHOLD = 0.055

        self.frame_counter = 0
        self.yawn_count = 0
        self.status = "NO"

    def distance(self, p1, p2):

        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb)

        mar = 0

        if results.multi_face_landmarks:

            face = results.multi_face_landmarks[0]

            top = face.landmark[self.MOUTH[0]]
            bottom = face.landmark[self.MOUTH[1]]
            left = face.landmark[self.MOUTH[2]]
            right = face.landmark[self.MOUTH[3]]

            vertical = self.distance(top, bottom)
            horizontal = self.distance(left, right)

            mar = vertical / horizontal

            if mar > self.YAWN_THRESHOLD:

                self.frame_counter += 1

                if self.frame_counter >= 15:
                    self.status = "YES"

            else:

                if self.frame_counter >= 15:
                    self.yawn_count += 1

                self.frame_counter = 0
                self.status = "NO"

        return mar, self.yawn_count, self.status