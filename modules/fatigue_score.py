class FatigueEngine:

    def __init__(self):
        self.score = 0
        self.status = "SAFE"

    def calculate(self,
                  eye_status,
                  yawn_status,
                  head_direction,
                  phone_detected):

        score = 0

        # Eyes Closed
        if eye_status == "DROWSY":
            score += 35

        # Yawning
        if yawn_status == "YES":
            score += 25

        # Looking Away
        if head_direction != "FORWARD":
            score += 20

        # Phone Usage
        if phone_detected:
            score += 20

        self.score = score

        if score >= 70:
            self.status = "DROWSY"

        elif score >= 40:
            self.status = "WARNING"

        else:
            self.status = "SAFE"

        return self.score, self.status