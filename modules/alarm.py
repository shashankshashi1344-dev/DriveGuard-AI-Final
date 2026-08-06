import threading
import winsound
import time


class Alarm:

    def __init__(self):

        self.is_playing = False

    def play_alarm(self):

        if self.is_playing:
            return

        self.is_playing = True

        def alarm():

            while self.is_playing:

                winsound.Beep(2500, 350)
                time.sleep(0.15)

        threading.Thread(
            target=alarm,
            daemon=True
        ).start()

    def stop(self):

        self.is_playing = False