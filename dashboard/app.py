import glob
import os

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DriveGuard AI Dashboard",
    layout="wide"
)

st.title("🚗 DriveGuard AI Dashboard")

files = glob.glob("reports/*.csv")

if len(files) == 0:

    st.warning("No report found.")

    st.stop()

latest = max(files, key=os.path.getctime)

df = pd.read_csv(latest)

st.subheader("Latest Session")

st.dataframe(df)

col1, col2, col3 = st.columns(3)

col1.metric("Frames Logged", len(df))

col2.metric(
    "Max Fatigue",
    df["Fatigue"].max()
)

col3.metric(
    "Phone Events",
    (df["Phone"] == "YES").sum()
)

fig = px.line(
    df,
    y="Fatigue",
    title="Fatigue Score Over Time",
)

st.plotly_chart(fig, use_container_width=True)

fig2 = px.histogram(
    df,
    x="Status",
    title="Driver Status Distribution"
)

st.plotly_chart(fig2, use_container_width=True)