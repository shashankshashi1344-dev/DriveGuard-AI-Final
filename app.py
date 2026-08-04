import cv2

from modules.camera import Camera
from modules.face_detection import FaceDetector
from modules.eye_detection import EyeDetector
from modules.yawn_detection import YawnDetector


def main():

    camera = Camera()
    detector = FaceDetector()
    eye_detector = EyeDetector()
    yawn_detector = YawnDetector()

    print("===================================")
    print("      DriveGuard AI Started")
    print("      Press Q to Exit")
    print("===================================")

    while True:

        frame = camera.read()

        if frame is None:
            break

        frame, faces = detector.detect(frame)

        ear, blinks, eye_status = eye_detector.detect(frame)

        mar, yawns, yawn_status = yawn_detector.detect(frame)

        cv2.putText(frame, "DriveGuard AI", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

        cv2.putText(frame,f"Faces : {faces}",(20,80),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

        cv2.putText(frame,f"EAR : {ear:.3f}",(20,120),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),2)

        cv2.putText(frame,f"Blinks : {blinks}",(20,160),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)

        cv2.putText(frame,f"Eye Status : {eye_status}",(20,200),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,
                    (0,255,0) if eye_status=="ALERT" else (0,0,255),2)

        cv2.putText(frame,f"MAR : {mar:.3f}",(20,240),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)

        cv2.putText(frame,f"Yawns : {yawns}",(20,280),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

        cv2.putText(frame,f"Yawning : {yawn_status}",(20,320),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,
                    (0,255,0) if yawn_status=="NO" else (0,0,255),2)

        cv2.imshow("DriveGuard AI", frame)

        key=cv2.waitKey(1)&0xFF

        if key==ord("q") or key==27:
            break

    camera.release()


if __name__=="__main__":
    main()