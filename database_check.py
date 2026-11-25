import sqlite3

conn = sqlite3.connect("database/driveguard.db")

print("\n=== TABLES ===")
print(conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall())

print("\n=== MONITORING SESSIONS ===")
print(conn.execute("""
    SELECT session_id, start_time, duration_seconds,
           total_frames, average_fatigue, maximum_fatigue,
           total_alerts, final_status
    FROM monitoring_sessions
    ORDER BY session_id DESC
    LIMIT 5
""").fetchall())

print("\n=== RECENT DETECTION EVENTS ===")
print(conn.execute("""
    SELECT event_type, severity, fatigue_score, description
    FROM detection_events
    ORDER BY event_id DESC
    LIMIT 10
""").fetchall())

print("\n=== MONITORING RECORD COUNT ===")
print(conn.execute(
    "SELECT COUNT(*) FROM monitoring_records"
).fetchone())

conn.close()
