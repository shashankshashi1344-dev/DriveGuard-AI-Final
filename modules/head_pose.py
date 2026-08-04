import cv2
import mediapipe as mp


class HeadPoseDetector:

    def __init__(self):

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True
        )

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb)

        direction = "FORWARD"

        if results.multi_face_landmarks:

            face = results.multi_face_landmarks[0]

            nose = face.landmark[1]

            if nose.x < 0.42:
                direction = "LEFT"

            elif nose.x > 0.58:
                direction = "RIGHT"

            elif nose.y < 0.38:
                direction = "UP"

            elif nose.y > 0.62:
                direction = "DOWN"

        return direction