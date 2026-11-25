
import glob
import os
import sqlite3

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_autorefresh import st_autorefresh


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DriveGuard AI | Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Automatic dashboard refresh every 5 seconds
st_autorefresh(
    interval=5000,
    key="driveguard_auto_refresh"
)

# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "driveguard.db"
)

REPORTS_PATH = os.path.join(
    BASE_DIR,
    "reports"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

[data-testid="stSidebar"] {
    background-color: #151922;
}

.metric-card {
    background-color: #1c2330;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #303846;
}

.dashboard-title {
    font-size: 36px;
    font-weight: bold;
    color: #00d4ff;
}

.dashboard-subtitle {
    color: #aab4c3;
    font-size: 16px;
}

.section-title {
    color: #00d4ff;
    font-size: 22px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

@st.cache_data(ttl=5)
def load_sessions():

    if not os.path.exists(DATABASE_PATH):
        return pd.DataFrame()

    connection = sqlite3.connect(DATABASE_PATH)

    try:

        df = pd.read_sql_query(
            """
            SELECT *
            FROM monitoring_sessions
            ORDER BY session_id DESC
            """,
            connection
        )

    except Exception:

        df = pd.DataFrame()

    finally:

        connection.close()

    return df


@st.cache_data(ttl=5)
def load_monitoring_records(session_id=None):

    if not os.path.exists(DATABASE_PATH):
        return pd.DataFrame()

    connection = sqlite3.connect(DATABASE_PATH)

    try:

        if session_id is not None:

            df = pd.read_sql_query(
                """
                SELECT *
                FROM monitoring_records
                WHERE session_id = ?
                ORDER BY record_id ASC
                """,
                connection,
                params=(session_id,)
            )

        else:

            df = pd.read_sql_query(
                """
                SELECT *
                FROM monitoring_records
                ORDER BY record_id DESC
                """,
                connection
            )

    except Exception:

        df = pd.DataFrame()

    finally:

        connection.close()

    return df


@st.cache_data(ttl=5)
def load_latest_monitoring_record():
    if not os.path.exists(DATABASE_PATH):
        return pd.DataFrame()
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        df = pd.read_sql_query(
            """
            SELECT monitoring_records.*,
                   monitoring_sessions.start_time
            FROM monitoring_records
            LEFT JOIN monitoring_sessions
                ON monitoring_records.session_id = monitoring_sessions.session_id
            ORDER BY monitoring_records.record_id DESC
            LIMIT 1
            """,
            connection
        )
    except Exception:
        df = pd.DataFrame()
    finally:
        connection.close()
    return df


@st.cache_data(ttl=5)
def load_detection_events(session_id=None):

    if not os.path.exists(DATABASE_PATH):
        return pd.DataFrame()

    connection = sqlite3.connect(DATABASE_PATH)

    try:

        if session_id is not None:

            df = pd.read_sql_query(
                """
                SELECT *
                FROM detection_events
                WHERE session_id = ?
                ORDER BY event_id DESC
                """,
                connection,
                params=(session_id,)
            )

        else:

            df = pd.read_sql_query(
                """
                SELECT *
                FROM detection_events
                ORDER BY event_id DESC
                """,
                connection
            )

    except Exception:

        df = pd.DataFrame()

    finally:

        connection.close()

    return df


@st.cache_data(ttl=5)
def load_csv_reports():

    files = glob.glob(
        os.path.join(REPORTS_PATH, "*.csv")
    )

    reports = []

    for file in files:

        try:

            df = pd.read_csv(file)

            reports.append({
                "filename": os.path.basename(file),
                "path": file,
                "data": df
            })

        except Exception:

            continue

    reports.sort(
        key=lambda item: os.path.getctime(item["path"]),
        reverse=True
    )

    return reports


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_duration(seconds):

    if pd.isna(seconds):
        return "N/A"

    seconds = int(seconds)

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    remaining_seconds = seconds % 60

    if hours > 0:

        return f"{hours}h {minutes}m {remaining_seconds}s"

    elif minutes > 0:

        return f"{minutes}m {remaining_seconds}s"

    else:

        return f"{remaining_seconds}s"


def safe_number(value, default=0):

    try:

        if pd.isna(value):
            return default

        return float(value)

    except Exception:

        return default


def status_color(status):

    status = str(status).upper()

    if status == "SAFE":
        return "#00cc96"

    elif status == "WARNING":
        return "#ffa15a"

    elif status == "DROWSY":
        return "#ef553b"

    return "#808080"


def style_plot(fig, height=400):

    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(
            color="#FAFAFA"
        ),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    return fig


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">🚗 DriveGuard AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'AI-Based Driver Drowsiness Detection and Monitoring System'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚗 DriveGuard AI")

st.sidebar.markdown("---")

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Overview",
        "Session History",
        "Session Analytics",
        "Detection Events",
        "Raw Data"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### System Information")

st.sidebar.info(
    """
    **Computer Vision**

    • OpenCV

    **Face Detection**

    • MediaPipe

    **Object Detection**

    • YOLOv8

    **Database**

    • SQLite

    **Analytics**

    • Streamlit

    • Plotly
    """
)

if st.sidebar.button(
    "🔄 Refresh Dashboard",
    use_container_width=True
):

    st.cache_data.clear()

    st.rerun()


# ============================================================
# LOAD DATABASE
# ============================================================

sessions_df = load_sessions()

all_records_df = load_monitoring_records()

latest_record_df = load_latest_monitoring_record()

all_events_df = load_detection_events()

csv_reports = load_csv_reports()


# ============================================================
# DATABASE STATUS
# ============================================================

st.sidebar.markdown("---")

if os.path.exists(DATABASE_PATH):

    st.sidebar.success(
        "🟢 Database Connected"
    )

else:

    st.sidebar.error(
        "🔴 Database Not Found"
    )


# ============================================================
# DATABASE STATISTICS
# ============================================================

total_sessions = len(sessions_df)

total_records = len(all_records_df)

total_events = len(all_events_df)

total_alerts = 0

total_phone_events = 0

if not sessions_df.empty:

    if "total_alerts" in sessions_df.columns:

        total_alerts = int(
            sessions_df["total_alerts"]
            .fillna(0)
            .sum()
        )

    if "phone_events" in sessions_df.columns:

        total_phone_events = int(
            sessions_df["phone_events"]
            .fillna(0)
            .sum()
        )


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "Overview":

    st.subheader("📊 System Overview")

    # --------------------------------------------------------
    # LIVE MONITORING STATUS
    # --------------------------------------------------------

    st.subheader("🔴 Live Monitoring Status")

    if latest_record_df.empty:
        st.info("No monitoring data available yet. Start DriveGuard AI to see live status.")
    else:
        live = latest_record_df.iloc[0]
        live_status = str(live.get("fatigue_status", "UNKNOWN")).upper()
        live_color = status_color(live_status)
        live_fatigue = safe_number(live.get("fatigue_score", 0))
        live_session = live.get("session_id", "N/A")
        live_time = live.get("timestamp", "N/A")

        st.markdown(
            f"""
            <div style="background-color: #1c2330; border: 1px solid {live_color};
                        border-left: 8px solid {live_color}; border-radius: 12px;
                        padding: 18px 22px; margin-bottom: 12px;">
                <div style="font-size: 14px; color: #aab4c3;">LATEST DRIVER STATUS</div>
                <div style="font-size: 32px; font-weight: bold; color: {live_color};">
                    {live_status}
                </div>
                <div style="color: #aab4c3; margin-top: 4px;">
                    Session: {live_session} &nbsp; | &nbsp; Latest record: {live_time}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        live_col1, live_col2, live_col3, live_col4, live_col5 = st.columns(5)
        live_col1.metric("Fatigue Score", f"{live_fatigue:.2f}")
        live_col2.metric("Eye Status", str(live.get("eye_status", "N/A")))
        live_col3.metric("Yawning", str(live.get("yawning", "N/A")))
        live_col4.metric(
            "Phone",
            "DETECTED" if str(live.get("phone_detected", "")).upper() in ("1", "TRUE", "YES") else "NOT DETECTED"
        )
        live_col5.metric("Head Direction", str(live.get("head_direction", "N/A")))

        st.caption("This panel displays the latest record stored in SQLite and updates automatically every 5 seconds.")

    st.markdown("---")

    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Sessions",
        total_sessions
    )

    col2.metric(
        "Monitoring Records",
        total_records
    )

    col3.metric(
        "Detection Events",
        total_events
    )

    col4.metric(
        "Drowsiness Alerts",
        total_alerts
    )

    st.markdown("---")

    # --------------------------------------------------------
    # SECONDARY KPIs
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Phone Detection Events",
        total_phone_events
    )

    col2.metric(
        "Total Frames",
        total_records
    )

    if not sessions_df.empty:

        avg_fatigue = safe_number(
            sessions_df["average_fatigue"].mean()
        )

        maximum_fatigue = safe_number(
            sessions_df["maximum_fatigue"].max()
        )

    else:

        avg_fatigue = 0

        maximum_fatigue = 0

    col3.metric(
        "Average Session Fatigue",
        f"{avg_fatigue:.2f}"
    )

    col4.metric(
        "Maximum Recorded Fatigue",
        f"{maximum_fatigue:.2f}"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # SESSION ACTIVITY
    # --------------------------------------------------------

    st.subheader("📈 Monitoring Session Activity")

    if not sessions_df.empty:

        session_chart_df = sessions_df.copy()

        session_chart_df["session_id"] = (
            session_chart_df["session_id"]
            .astype(str)
        )

        fig = px.bar(
            session_chart_df,
            x="session_id",
            y="total_frames",
            color="final_status",
            title="Frames Recorded Per Session",
            labels={
                "session_id": "Session ID",
                "total_frames": "Total Frames",
                "final_status": "Final Status"
            },
            color_discrete_map={
                "SAFE": "#00cc96",
                "WARNING": "#ffa15a",
                "DROWSY": "#ef553b",
                "UNKNOWN": "#808080"
            }
        )

        style_plot(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No monitoring sessions are available yet."
        )

    # --------------------------------------------------------
    # FATIGUE DISTRIBUTION
    # --------------------------------------------------------

    if not all_records_df.empty:

        st.subheader("📊 Fatigue Score Distribution")

        fatigue_df = all_records_df.copy()

        fatigue_df["fatigue_score"] = pd.to_numeric(
            fatigue_df["fatigue_score"],
            errors="coerce"
        )

        fatigue_df = fatigue_df.dropna(
            subset=["fatigue_score"]
        )

        if not fatigue_df.empty:

            fig = px.histogram(
                fatigue_df,
                x="fatigue_score",
                nbins=20,
                title="Distribution of Fatigue Scores",
                color_discrete_sequence=["#00d4ff"]
            )

            style_plot(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # --------------------------------------------------------
    # LATEST SESSION
    # --------------------------------------------------------

    if not sessions_df.empty:

        st.subheader("🕒 Latest Monitoring Session")

        latest_session = sessions_df.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Session ID",
            latest_session["session_id"]
        )

        col2.metric(
            "Duration",
            format_duration(
                latest_session.get("duration_seconds", 0)
            )
        )

        col3.metric(
            "Average Fatigue",
            f"{safe_number(latest_session.get('average_fatigue', 0)):.2f}"
        )

        col4.metric(
            "Final Status",
            latest_session.get("final_status", "UNKNOWN")
        )


# ============================================================
# SESSION HISTORY
# ============================================================

elif page == "Session History":

    st.subheader("📚 Monitoring Session History")

    if sessions_df.empty:

        st.warning(
            "No monitoring sessions found. "
            "Run DriveGuard AI to create a session."
        )

    else:

        history_df = sessions_df.copy()

        if "start_time" in history_df.columns:

            history_df["start_time"] = pd.to_datetime(
                history_df["start_time"],
                errors="coerce"
            )

        if "end_time" in history_df.columns:

            history_df["end_time"] = pd.to_datetime(
                history_df["end_time"],
                errors="coerce"
            )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        st.subheader("📊 Session Comparison")

        if len(sessions_df) > 1:

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=sessions_df["session_id"].astype(str),
                    y=sessions_df["average_fatigue"],
                    name="Average Fatigue",
                    marker_color="#00d4ff"
                )
            )

            fig.add_trace(
                go.Bar(
                    x=sessions_df["session_id"].astype(str),
                    y=sessions_df["maximum_fatigue"],
                    name="Maximum Fatigue",
                    marker_color="#ef553b"
                )
            )

            fig.update_layout(
                barmode="group",
                title="Fatigue Comparison Across Sessions",
                xaxis_title="Session ID",
                yaxis_title="Fatigue Score"
            )

            style_plot(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # SESSION EXPORT
        # ----------------------------------------------------

        csv_data = sessions_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Session History",
            data=csv_data,
            file_name="driveguard_session_history.csv",
            mime="text/csv"
        )


# ============================================================
# SESSION ANALYTICS
# ============================================================

elif page == "Session Analytics":

    st.subheader("📈 Detailed Session Analytics")

    if sessions_df.empty:

        st.warning(
            "No sessions are available for analysis."
        )

    else:

        session_ids = sessions_df[
            "session_id"
        ].tolist()

        selected_session = st.selectbox(
            "Select Monitoring Session",
            session_ids
        )

        selected_session_data = sessions_df[
            sessions_df["session_id"] == selected_session
        ].iloc[0]

        records_df = load_monitoring_records(
            selected_session
        )

        # ----------------------------------------------------
        # SESSION KPI
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Session Duration",
            format_duration(
                selected_session_data.get(
                    "duration_seconds",
                    0
                )
            )
        )

        col2.metric(
            "Total Frames",
            selected_session_data.get(
                "total_frames",
                0
            )
        )

        col3.metric(
            "Average Fatigue",
            f"{safe_number(selected_session_data.get('average_fatigue', 0)):.2f}"
        )

        col4.metric(
            "Maximum Fatigue",
            f"{safe_number(selected_session_data.get('maximum_fatigue', 0)):.2f}"
        )

        st.markdown("---")

        # ----------------------------------------------------
        # SESSION INFORMATION
        # ----------------------------------------------------

        st.subheader("📋 Session Information")

        info_col1, info_col2 = st.columns(2)

        with info_col1:

            st.write(
                f"**Session ID:** {selected_session_data['session_id']}"
            )

            st.write(
                f"**Start Time:** {selected_session_data.get('start_time', 'N/A')}"
            )

            st.write(
                f"**End Time:** {selected_session_data.get('end_time', 'N/A')}"
            )

        with info_col2:

            st.write(
                f"**Drowsiness Alerts:** "
                f"{selected_session_data.get('total_alerts', 0)}"
            )

            st.write(
                f"**Phone Events:** "
                f"{selected_session_data.get('phone_events', 0)}"
            )

            st.write(
                f"**Final Status:** "
                f"{selected_session_data.get('final_status', 'UNKNOWN')}"
            )

        st.markdown("---")

        # ----------------------------------------------------
        # FATIGUE TIMELINE
        # ----------------------------------------------------

        st.subheader("📉 Fatigue Timeline")

        if not records_df.empty:

            records_df["fatigue_score"] = pd.to_numeric(
                records_df["fatigue_score"],
                errors="coerce"
            )

            records_df["timestamp"] = pd.to_datetime(
                records_df["timestamp"],
                errors="coerce"
            )

            records_df = records_df.dropna(
                subset=["fatigue_score"]
            )

            fig = px.line(
                records_df,
                x="timestamp",
                y="fatigue_score",
                title="Fatigue Score Over Time",
                markers=False
            )

            fig.update_traces(
                line=dict(
                    color="#00d4ff",
                    width=2
                )
            )

            style_plot(
                fig,
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # ------------------------------------------------
            # STATUS DISTRIBUTION
            # ------------------------------------------------

            st.subheader("🚦 Driver Status Distribution")

            status_counts = records_df[
                "fatigue_status"
            ].value_counts()

            status_fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                color=status_counts.index,
                color_discrete_map={
                    "SAFE": "#00cc96",
                    "WARNING": "#ffa15a",
                    "DROWSY": "#ef553b"
                },
                hole=0.4
            )

            style_plot(
                status_fig,
                height=400
            )

            st.plotly_chart(
                status_fig,
                use_container_width=True
            )

            # ------------------------------------------------
            # EYE STATUS
            # ------------------------------------------------

            if "eye_status" in records_df.columns:

                st.subheader("👁️ Eye Status Analysis")

                eye_counts = records_df[
                    "eye_status"
                ].value_counts()

                eye_fig = px.bar(
                    x=eye_counts.index,
                    y=eye_counts.values,
                    title="Eye Status Frequency",
                    color=eye_counts.index
                )

                style_plot(
                    eye_fig,
                    height=350
                )

                st.plotly_chart(
                    eye_fig,
                    use_container_width=True
                )

        else:

            st.info(
                "No monitoring records are available for this session."
            )


# ============================================================
# DETECTION EVENTS
# ============================================================

elif page == "Detection Events":

    st.subheader("🚨 Detection Events")

    if all_events_df.empty:

        st.info(
            "No detection events have been recorded yet."
        )

    else:

        # ----------------------------------------------------
        # EVENT METRICS
        # ----------------------------------------------------

        event_counts = all_events_df[
            "event_type"
        ].value_counts()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Events",
            len(all_events_df)
        )

        col2.metric(
            "Drowsiness Events",
            int(
                event_counts.get(
                    "DROWSINESS",
                    0
                )
            )
        )

        col3.metric(
            "Phone Events",
            int(
                event_counts.get(
                    "PHONE_DETECTION",
                    0
                )
            )
        )

        st.markdown("---")

        # ----------------------------------------------------
        # EVENT FILTER
        # ----------------------------------------------------

        event_types = [
            "All Events"
        ] + sorted(
            all_events_df["event_type"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_event_type = st.selectbox(
            "Filter Events",
            event_types
        )

        filtered_events = all_events_df.copy()

        if selected_event_type != "All Events":

            filtered_events = filtered_events[
                filtered_events["event_type"]
                == selected_event_type
            ]

        # ----------------------------------------------------
        # EVENT TABLE
        # ----------------------------------------------------

        st.subheader("📋 Event Records")

        st.dataframe(
            filtered_events,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # EVENT CHART
        # ----------------------------------------------------

        st.subheader("📊 Event Distribution")

        fig = px.bar(
            all_events_df,
            x="event_type",
            color="severity",
            title="Detection Events by Type",
            color_discrete_map={
                "HIGH": "#ef553b",
                "MEDIUM": "#ffa15a",
                "LOW": "#00cc96"
            }
        )

        style_plot(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # EVENT DOWNLOAD
        # ----------------------------------------------------

        event_csv = filtered_events.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Detection Events",
            data=event_csv,
            file_name="driveguard_detection_events.csv",
            mime="text/csv"
        )


# ============================================================
# RAW DATA
# ============================================================

elif page == "Raw Data":

    st.subheader("📋 Raw Monitoring Data")

    data_source = st.radio(
        "Select Data Source",
        [
            "SQLite Database",
            "CSV Reports"
        ],
        horizontal=True
    )

    # ========================================================
    # SQLITE DATABASE
    # ========================================================

    if data_source == "SQLite Database":

        if sessions_df.empty:

            st.warning(
                "No database sessions are available."
            )

        else:

            selected_session = st.selectbox(
                "Select Session",
                sessions_df["session_id"].tolist()
            )

            records_df = load_monitoring_records(
                selected_session
            )

            st.write(
                f"Session ID: **{selected_session}**"
            )

            st.dataframe(
                records_df,
                use_container_width=True,
                height=500
            )

            # ------------------------------------------------
            # DOWNLOAD
            # ------------------------------------------------

            csv_data = records_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="📥 Download Database Records",
                data=csv_data,
                file_name=f"driveguard_session_{selected_session}.csv",
                mime="text/csv"
            )

    # ========================================================
    # CSV REPORTS
    # ========================================================

    else:

        if not csv_reports:

            st.warning(
                "No CSV reports found."
            )

        else:

            report_names = [
                report["filename"]
                for report in csv_reports
            ]

            selected_report = st.selectbox(
                "Select CSV Report",
                report_names
            )

            selected_report_data = next(
                report
                for report in csv_reports
                if report["filename"] == selected_report
            )

            df = selected_report_data["data"]

            st.write(
                f"Selected Report: **{selected_report}**"
            )

            st.dataframe(
                df,
                use_container_width=True,
                height=500
            )

            csv_data = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="📥 Download CSV Report",
                data=csv_data,
                file_name=selected_report,
                mime="text/csv"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "DriveGuard AI | Intelligent Driver Monitoring System | "
    "Computer Vision, Artificial Intelligence and Data Analytics"
)
