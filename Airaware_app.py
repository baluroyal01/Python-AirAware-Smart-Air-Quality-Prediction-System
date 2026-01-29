%%writefile app.py
import streamlit as st
import plotly.graph_objects as go
import time
import pandas as pd
import numpy as np


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Smart Air Quality Dashboard", layout="wide")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
for key, value in {
    "loaded": False,
    "df": None,
    "aqi": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# YOUR EARTH LOADER (UNCHANGED)
# --------------------------------------------------
def show_earth_loader(seconds=2, text="Connecting…"):
    loader = st.empty()
    loader.markdown(f"""
    <style>
    .loader-wrapper {{
      position: fixed; inset: 0; z-index: 9999;
      display: flex; justify-content: center; align-items: center;
      background: radial-gradient(circle at top,#0f172a,#020617);
    }}
    .earth {{ display: flex; flex-direction: column; align-items: center; gap: 1rem; }}
    .earth p {{ color: white; font-size: 1.1rem; letter-spacing: 1px; }}
    .earth-loader {{
      --watercolor:#3f51d9; --landcolor:#9be24f;
      width:8em; height:8em; position:relative; overflow:hidden;
      border-radius:50%; border:2px solid rgba(255,255,255,0.9);
      background: radial-gradient(circle at 30% 30%,#6a78ff,var(--watercolor));
      box-shadow: inset 0.45em 0.45em rgba(255,255,255,.22),
                  inset -0.6em -0.6em rgba(0,0,0,.42),
                  0 0 22px rgba(79,112,255,.4);
    }}
    .earth-loader svg {{ position:absolute; width:8.2em; opacity:.9; }}
    .earth-loader svg:nth-child(1) {{ top:-2.6em; animation:round1 4s infinite linear; }}
    .earth-loader svg:nth-child(2) {{ bottom:-2.8em; animation:round2 4s infinite linear .9s; }}
    .earth-loader svg:nth-child(3) {{ top:-1.8em; animation:round1 4s infinite linear 1.8s; }}

    @keyframes round1 {{
      0% {{ left:-3.5em; opacity:1; }}
      50% {{ left:-8em; opacity:0; }}
      100% {{ left:-3.5em; opacity:1; }}
    }}
    @keyframes round2 {{
      0% {{ left:5.5em; opacity:1; }}
      50% {{ left:-9em; opacity:0; }}
      100% {{ left:5.5em; opacity:1; }}
    }}
    </style>

    <div class="loader-wrapper">
      <div class="earth">
        <div class="earth-loader">
          <svg viewBox="0 0 200 200"><path fill="var(--landcolor)"
            d="M100 35 C138 38,162 68,158 105 C154 142,120 160,100 156
               C62 152,38 125,42 100 C46 70,70 40,100 35Z"/></svg>
          <svg viewBox="0 0 200 200"><path fill="var(--landcolor)"
            d="M100 45 C132 48,152 78,148 108 C144 138,118 148,100 145
               C68 142,48 120,52 100 C56 78,72 50,100 45Z"/></svg>
          <svg viewBox="0 0 200 200"><path fill="var(--landcolor)"
            d="M100 40 C130 44,150 72,146 104 C142 136,118 148,100 144
               C70 140,50 118,54 100 C58 74,74 46,100 40Z"/></svg>
        </div>
        <p>{text}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(seconds)
    loader.empty()

# --------------------------------------------------
# STARTUP
# --------------------------------------------------
if not st.session_state.loaded:
    show_earth_loader(2, "Initializing Air Quality System…")
    st.session_state.loaded = True



# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.header("🎛 Controls")
st.sidebar.selectbox("Monitoring Station", ["Downtown","Suburb","Industrial Area"])
time_range = st.sidebar.selectbox(
    "Time Range",
    ["Last 24 Hours", "Last 7 Days"]
)
admin_mode = st.sidebar.toggle("Admin Mode")

# --------------------------------------------------
# ADMIN MODE
# --------------------------------------------------
if admin_mode:
    uploaded = st.sidebar.file_uploader("Upload AQI Dataset", type=["csv"])

    if uploaded:
        show_earth_loader(1.5, "Processing Dataset…")
        df = pd.read_csv(uploaded)
        df.columns = df.columns.str.strip()

        # Date handling
        if "Datetime" in df.columns:
            df["Date"] = pd.to_datetime(df["Datetime"])
        elif "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
        else:
            st.error("Dataset must contain Date or Datetime column")
            st.stop()

        # Ensure PM2.5 exists
        if "PM2.5" not in df.columns:
            st.error("PM2.5 column is required")
            st.stop()

        # AQI calculation
        if "AQI" not in df.columns:
            df["AQI"] = df["PM2.5"] * 1.2

        # Save to session
        st.session_state.df = df.sort_values("Date")
        st.session_state.aqi = int(df["AQI"].mean())

        st.sidebar.success("Dataset Loaded — Dashboard Updated")


# --------------------------------------------------
# DATA FILTERING
# --------------------------------------------------


df = st.session_state.df

if df is not None:
    if time_range == "Last 24 Hours":
        df = df.tail(24)
    else:
        df = df.tail(7)


# --------------------------------------------------
# TOP ROW – AQI & PM2.5
# --------------------------------------------------
aqi = st.session_state.aqi
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("Current Air Quality")
    fig = go.Figure(go.Pie(
        values=[aqi, max(0, 300 - aqi)],
        hole=0.75,
        marker=dict(colors=["#22c55e", "#e5e7eb"]),
        textinfo="none"
    ))
    fig.add_annotation(
        text=f"<b>{aqi}</b><br>AQI",
        x=0.5, y=0.5, showarrow=False, font=dict(size=22)
    )
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("PM2.5 Trend")
    fig = go.Figure()
    if df is not None:
        fig.add_trace(go.Scatter(
            x=df["Date"], y=df["PM2.5"],
            mode="lines", name="PM2.5"
        ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# POLLUTANT TRENDS (✔ ADDED & COMPLETE)
# --------------------------------------------------
st.subheader("📊 Pollutant Trends")

if df is not None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["PM2.5"], name="PM2.5"))

    if "NO2" in df.columns:
        fig.add_trace(go.Scatter(x=df["Date"], y=df["NO2"], name="NO2"))
    if "O3" in df.columns:
        fig.add_trace(go.Scatter(x=df["Date"], y=df["O3"], name="O3"))

    fig.update_layout(height=320)
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# DAILY ALERTS
# --------------------------------------------------
st.subheader("📅 Daily Air Quality Alerts")

aqi = st.session_state.aqi
c1, c2, c3 = st.columns(3)

if aqi <= 50:
    c1.success("🌅 Good AQI\nSafe for all activities")
elif aqi <= 100:
    c2.warning("🌤 Moderate AQI\nSensitive groups should limit exposure")
elif aqi <= 200:
    c3.error("🌙 Poor AQI\nAvoid prolonged outdoor activity")
else:
    c3.error("🚨 Severe AQI\nHealth emergency conditions")
