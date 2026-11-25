import csv
import os
from datetime import datetime


class ReportGenerator:

    def __init__(self):

        os.makedirs("reports", exist_ok=True)

        self.filename = f"reports/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(self.filename, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Time",
                "Faces",
                "Eye Status",
                "Yawning",
                "Head",
                "Phone",
                "Fatigue",
                "Status"
            ])

    def write(
        self,
        faces,
        eye_status,
        yawn_status,
        head_direction,
        phone_detected,
        fatigue_score,
        fatigue_status
    ):

        with open(self.filename, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%H:%M:%S"),
                faces,
                eye_status,
                yawn_status,
                head_direction,
                "YES" if phone_detected else "NO",
                fatigue_score,
                fatigue_status
            ])