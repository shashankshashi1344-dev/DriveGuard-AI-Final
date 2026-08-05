import threading
import winsound


class Alarm:

    def __init__(self):

        self.is_playing = False

    def play_alarm(self):

        if self.is_playing:
            return

        self.is_playing = True

        def beep():

            for _ in range(5):

                winsound.Beep(2500, 400)

            self.is_playing = False

        threading.Thread(target=beep, daemon=True).start()

    def stop(self):

        self.is_playing = False