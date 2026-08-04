import cv2
from modules.camera import Camera


def main():

    camera = Camera()

    print("===================================")
    print("     DriveGuard AI Started")
    print(" Press Q to Quit")
    print("===================================")

    while True:

        frame = camera.read()

        if frame is None:
            print("Camera Error")
            break

        cv2.putText(
            frame,
            "DriveGuard AI",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
        )

        cv2.imshow("DriveGuard AI", frame)

        key = cv2.waitKey(1)

        if key == ord("q") or key == ord("Q") or key == 27:
            print("Closing Camera...")
            break

    camera.release()


if __name__ == "__main__":
    main()