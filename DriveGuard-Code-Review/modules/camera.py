import cv2


class Camera:
    def __init__(self, camera_index=0):

        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise Exception("Unable to open webcam.")

        # HD Resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Better FPS
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        # Reduce camera delay
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def read(self):

        success, frame = self.cap.read()

        if not success:
            return None

        # Slight brightness improvement
        frame = cv2.convertScaleAbs(frame, alpha=1.15, beta=15)

        return frame

    def release(self):

        self.cap.release()
        cv2.destroyAllWindows()