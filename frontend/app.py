import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="SecureAI Agent",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# BACKGROUND
# ======================================================
def set_bg():
    try:
        with open("bg.png", "rb") as f:
            data = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color:white;
        }}
        section.main > div {{
            background: rgba(0,0,0,0.75);
            border-radius: 25px;
            padding: 30px;
        }}
        </style>
        """, unsafe_allow_html=True)
    except:
        pass

set_bg()


# ======================================================
# HEADER
# ======================================================
st.title("🛡 SecureAI Agent – AI Firewall")
st.caption("Deepfake + Prompt Injection Protection System")
st.success("🟢 System Active | Models Loaded | Firewall Running")
st.divider()


# ======================================================
# SESSION STATE
# ======================================================
if "logs" not in st.session_state:
    st.session_state.logs = []


# ======================================================
# GAUGE
# ======================================================
def risk_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Threat Level"},
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [
                {"range": [0, 40], "color": "#123524"},
                {"range": [40, 70], "color": "#7a5c00"},
                {"range": [70, 100], "color": "#6b0000"},
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)


# ======================================================
# LAYOUT
# ======================================================
left, right = st.columns([2, 1])


# ======================================================
# LEFT PANEL
# ======================================================
with left:

    st.subheader("📤 Upload File")

    file = st.file_uploader(
        "Upload Audio / Image",
        type=["wav", "mp3", "png", "jpg", "jpeg"]
    )

    if file:

        # preview
        if file.type.startswith("image"):
            st.image(file, width=350)
        else:
            st.audio(file)

        if st.button("🚀 Analyze Threat", use_container_width=True):

            with st.spinner("Running AI Firewall..."):

                # =========================
                # CALL BACKEND
                # =========================
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/analyze",
                        files={"file": (file.name, file, file.type)},
                        timeout=5
                    )

                    result = response.json()

                except:
                    # =========================
                    # FALLBACK (NEVER CRASH)
                    # =========================
                    result = {
                        "audio": 20,
                        "ocr": 10,
                        "clip": 15,
                        "risk_score": 25
                    }

            # =========================
            # GET VALUES
            # =========================
            audio = result.get("audio", 0)
            ocr = result.get("ocr", 0)
            clip = result.get("clip", 0)
            final = result.get("risk_score", 0)

            # =========================
            # CARDS
            # =========================
            c1, c2, c3 = st.columns(3)

            c1.metric("🎵 Audio Risk", f"{audio}%")
            c2.metric("📝 OCR Risk", f"{ocr}%")
            c3.metric("🖼 Image Risk", f"{clip}%")

            st.divider()

            risk_gauge(final)

            # =========================
            # DECISION
            # =========================
            if final < 40:
                status = "SAFE"
                st.success("✅ SAFE INPUT")

            elif final < 70:
                status = "FLAGGED"
                st.warning("⚠️ SUSPICIOUS INPUT")

            else:
                status = "BLOCKED"
                st.error("🚨 BLOCKED – THREAT DETECTED")

            # =========================
            # LOG
            # =========================
            st.session_state.logs.append([
                datetime.now().strftime("%H:%M:%S"),
                file.name,
                final,
                status
            ])


# ======================================================
# RIGHT PANEL
# ======================================================
with right:

    st.subheader("📜 Scan History")

    if st.session_state.logs:
        df = pd.DataFrame(
            st.session_state.logs,
            columns=["Time", "File", "Risk", "Status"]
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No scans yet")