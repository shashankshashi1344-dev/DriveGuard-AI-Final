import mediapipe as mp
import cv2
import math
from collections import deque


class EyeDetector:

    def __init__(self):

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
        )

        self.LEFT = [33, 160, 158, 133, 153, 144]
        self.RIGHT = [362, 385, 387, 263, 373, 380]

        self.EAR_THRESHOLD = 0.21
        self.CLOSED_FRAMES = 15

        self.frame_counter = 0
        self.blink_count = 0
        self.status = "ALERT"

        # Smooth EAR using last 5 values
        self.ear_history = deque(maxlen=5)

    def distance(self, p1, p2):
        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def calculate_ear(self, eye):

        A = self.distance(eye[1], eye[5])
        B = self.distance(eye[2], eye[4])
        C = self.distance(eye[0], eye[3])

        if C == 0:
            return 0

        return (A + B) / (2 * C)

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb)

        ear = 0

        if results.multi_face_landmarks:

            face = results.multi_face_landmarks[0]

            left = [face.landmark[i] for i in self.LEFT]
            right = [face.landmark[i] for i in self.RIGHT]

            leftEAR = self.calculate_ear(left)
            rightEAR = self.calculate_ear(right)

            ear = (leftEAR + rightEAR) / 2

            # Smooth EAR
            self.ear_history.append(ear)
            ear = sum(self.ear_history) / len(self.ear_history)

            if ear < self.EAR_THRESHOLD:

                self.frame_counter += 1

                if self.frame_counter >= self.CLOSED_FRAMES:
                    self.status = "DROWSY"

            else:

                if self.frame_counter >= 2:
                    self.blink_count += 1

                self.frame_counter = 0
                self.status = "ALERT"

        else:
            self.status = "NO FACE"

        return ear, self.blink_count, self.status