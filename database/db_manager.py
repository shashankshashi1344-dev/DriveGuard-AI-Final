
import sqlite3
import os
from datetime import datetime


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_FOLDER = "database"

DATABASE_PATH = os.path.join(
    DATABASE_FOLDER,
    "driveguard.db"
)


# ============================================================
# DATABASE MANAGER
# ============================================================

class DatabaseManager:

    def __init__(self):

        os.makedirs(DATABASE_FOLDER, exist_ok=True)

        self.initialize_database()


    # --------------------------------------------------------
    # DATABASE CONNECTION
    # --------------------------------------------------------

    def get_connection(self):

        return sqlite3.connect(DATABASE_PATH)


    # --------------------------------------------------------
    # INITIALIZE DATABASE
    # --------------------------------------------------------

    def initialize_database(self):

        connection = self.get_connection()

        cursor = connection.cursor()


        # MONITORING SESSIONS TABLE

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monitoring_sessions (

                session_id INTEGER PRIMARY KEY AUTOINCREMENT,

                start_time TEXT NOT NULL,

                end_time TEXT,

                duration_seconds REAL DEFAULT 0,

                total_frames INTEGER DEFAULT 0,

                average_fatigue REAL DEFAULT 0,

                maximum_fatigue REAL DEFAULT 0,

                total_alerts INTEGER DEFAULT 0,

                phone_events INTEGER DEFAULT 0,

                final_status TEXT DEFAULT 'UNKNOWN'

            )
        """)


        # MONITORING RECORDS TABLE

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monitoring_records (

                record_id INTEGER PRIMARY KEY AUTOINCREMENT,

                session_id INTEGER NOT NULL,

                timestamp TEXT NOT NULL,

                faces INTEGER,

                eye_status TEXT,

                yawning TEXT,

                head_direction TEXT,

                phone_detected INTEGER,

                fatigue_score REAL,

                fatigue_status TEXT,

                FOREIGN KEY (session_id)
                REFERENCES monitoring_sessions(session_id)

            )
        """)


        # DETECTION EVENTS TABLE

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detection_events (

                event_id INTEGER PRIMARY KEY AUTOINCREMENT,

                session_id INTEGER NOT NULL,

                timestamp TEXT NOT NULL,

                event_type TEXT NOT NULL,

                severity TEXT,

                fatigue_score REAL,

                description TEXT,

                FOREIGN KEY (session_id)
                REFERENCES monitoring_sessions(session_id)

            )
        """)


        connection.commit()

        connection.close()


    # --------------------------------------------------------
    # CREATE MONITORING SESSION
    # --------------------------------------------------------

    def create_session(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        start_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        cursor.execute("""
            INSERT INTO monitoring_sessions (
                start_time
            )
            VALUES (?)
        """, (start_time,))


        session_id = cursor.lastrowid

        connection.commit()

        connection.close()


        return session_id


    # --------------------------------------------------------
    # SAVE MONITORING RECORD
    # --------------------------------------------------------

    def record_frame(
        self,
        session_id,
        faces,
        eye_status,
        yawn_status,
        head_direction,
        phone_detected,
        fatigue_score,
        fatigue_status
    ):

        connection = self.get_connection()

        cursor = connection.cursor()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        cursor.execute("""
            INSERT INTO monitoring_records (

                session_id,
                timestamp,
                faces,
                eye_status,
                yawning,
                head_direction,
                phone_detected,
                fatigue_score,
                fatigue_status

            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            session_id,
            timestamp,
            faces,
            eye_status,
            yawn_status,
            head_direction,
            int(phone_detected),
            fatigue_score,
            fatigue_status

        ))


        connection.commit()

        connection.close()


    # --------------------------------------------------------
    # RECORD DETECTION EVENT
    # --------------------------------------------------------

    def record_event(
        self,
        session_id,
        event_type,
        severity,
        fatigue_score,
        description=""
    ):

        connection = self.get_connection()

        cursor = connection.cursor()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        cursor.execute("""
            INSERT INTO detection_events (

                session_id,
                timestamp,
                event_type,
                severity,
                fatigue_score,
                description

            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (

            session_id,
            timestamp,
            event_type,
            severity,
            fatigue_score,
            description

        ))


        connection.commit()

        connection.close()


    # --------------------------------------------------------
    # END MONITORING SESSION
    # --------------------------------------------------------

    def end_session(
        self,
        session_id,
        duration_seconds,
        total_frames,
        average_fatigue,
        maximum_fatigue,
        total_alerts,
        phone_events,
        final_status
    ):

        connection = self.get_connection()

        cursor = connection.cursor()

        end_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        cursor.execute("""
            UPDATE monitoring_sessions

            SET
                end_time = ?,
                duration_seconds = ?,
                total_frames = ?,
                average_fatigue = ?,
                maximum_fatigue = ?,
                total_alerts = ?,
                phone_events = ?,
                final_status = ?

            WHERE session_id = ?
        """, (

            end_time,
            duration_seconds,
            total_frames,
            average_fatigue,
            maximum_fatigue,
            total_alerts,
            phone_events,
            final_status,
            session_id

        ))


        connection.commit()

        connection.close()


    # --------------------------------------------------------
    # GET ALL SESSIONS
    # --------------------------------------------------------

    def get_sessions(self):

        connection = self.get_connection()

        cursor = connection.cursor()


        cursor.execute("""
            SELECT *
            FROM monitoring_sessions
            ORDER BY session_id DESC
        """)


        results = cursor.fetchall()

        connection.close()


        return results


    # --------------------------------------------------------
    # GET SESSION RECORDS
    # --------------------------------------------------------

    def get_session_records(self, session_id):

        connection = self.get_connection()

        cursor = connection.cursor()


        cursor.execute("""
            SELECT *
            FROM monitoring_records
            WHERE session_id = ?
            ORDER BY record_id ASC
        """, (session_id,))


        results = cursor.fetchall()

        connection.close()


        return results


    # --------------------------------------------------------
    # GET DETECTION EVENTS
    # --------------------------------------------------------

    def get_detection_events(self, session_id=None):

        connection = self.get_connection()

        cursor = connection.cursor()


        if session_id is None:

            cursor.execute("""
                SELECT *
                FROM detection_events
                ORDER BY event_id DESC
            """)

        else:

            cursor.execute("""
                SELECT *
                FROM detection_events
                WHERE session_id = ?
                ORDER BY event_id DESC
            """, (session_id,))


        results = cursor.fetchall()

        connection.close()


        return results
