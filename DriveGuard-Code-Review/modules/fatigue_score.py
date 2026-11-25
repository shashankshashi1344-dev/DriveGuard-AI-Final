class FatigueEngine:

    def __init__(self):

        self.score = 0
        self.status = "SAFE"

        # Score smoothing
        self.max_score = 100
        self.decay = 2

    def calculate(
        self,
        eye_status,
        yawn_status,
        head_direction,
        phone_detected
    ):

        # ----------------------------
        # Natural Recovery
        # ----------------------------

        self.score = max(0, self.score - self.decay)

        # ----------------------------
        # Eyes Closed
        # ----------------------------

        if eye_status == "DROWSY":
            self.score += 6

        # ----------------------------
        # Yawning
        # ----------------------------

        if yawn_status == "YES":
            self.score += 4

        # ----------------------------
        # Looking Away
        # ----------------------------

        if head_direction != "FORWARD":
            self.score += 3

        # ----------------------------
        # Phone Usage
        # ----------------------------

        if phone_detected:
            self.score += 5

        # ----------------------------
        # Limit Score
        # ----------------------------

        self.score = min(self.score, self.max_score)

        # ----------------------------
        # Driver Status
        # ----------------------------

        if self.score >= 75:
            self.status = "DROWSY"

        elif self.score >= 40:
            self.status = "WARNING"

        else:
            self.status = "SAFE"

        return int(self.score), self.status