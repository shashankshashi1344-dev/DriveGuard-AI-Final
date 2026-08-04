import mediapipe as mp
import cv2
import math


class EyeDetector:

    def __init__(self):

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
        )

        self.LEFT = [33,160,158,133,153,144]
        self.RIGHT = [362,385,387,263,373,380]

    def distance(self,p1,p2):

        return math.sqrt(
            (p1.x-p2.x)**2 +
            (p1.y-p2.y)**2
        )

    def ear(self,eye):

        A=self.distance(eye[1],eye[5])
        B=self.distance(eye[2],eye[4])
        C=self.distance(eye[0],eye[3])

        return (A+B)/(2*C)

    def detect(self,frame):

        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        results=self.face_mesh.process(rgb)

        ear=0

        if results.multi_face_landmarks:

            face=results.multi_face_landmarks[0]

            left=[face.landmark[i] for i in self.LEFT]

            right=[face.landmark[i] for i in self.RIGHT]

            leftEAR=self.ear(left)

            rightEAR=self.ear(right)

            ear=(leftEAR+rightEAR)/2

        return ear