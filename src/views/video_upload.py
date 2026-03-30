import streamlit as st
import uuid, time, random, tempfile, os, sys
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ui.theme import inject_global_css, page_header, section_divider, iq_card, idle_state
from analytics.wait_time import calculate_waiting_time
from analytics.service_status import calculate_utilization
from simulation.simulator import QueueSimulator
from shared_state import update_state

inject_global_css()

def get_service_status(u):
    return "Normal" if u < 0.7 else ("Slowing" if u <= 1.0 else "Stalled")

page_header(
    eyebrow="Version 2",
    title="CV Detection & Live Broadcast",
    subtitle="Upload counter footage. The computer vision pipeline extracts queue occupancy per frame and broadcasts live wait-time estimates to a shareable URL.",
    chips=[("Model", "YOLOv8"), ("Signal", "Real-time"), ("Output", "Shareable URL")],
)

# ── Counter ID ──────────────────────────────────────────────────────────────
if "admin_counter_id" not in st.session_state:
    st.session_state.admin_counter_id = str(uuid.uuid4())[:8]
admin_counter = st.session_state.admin_counter_id

# ── Step 1: Broadcast link ──────────────────────────────────────────────────
section_divider("Step 1 — Public broadcast link")

base = "http://localhost:8501"
share_url = f"?viewer=true&counter={admin_counter}"

st.markdown(f"""
<div class="iq-card" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px; padding: 22px 28px;">
    <div>
        <div class="iq-card-title">Customer queue status link</div>
        <div class="iq-card-body">Share this URL so customers can view estimated wait time on any device, in real time.</div>
    </div>
    <code style="white-space: nowrap;">{base}/{share_url}</code>
</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns([5, 1], gap="medium")
with col_b:
    if st.button("New Link"):
        del st.session_state["admin_counter_id"]
        st.rerun()

# ── Step 2: Upload ──────────────────────────────────────────────────────────
section_divider("Step 2 — Upload counter footage")

uploaded_video = st.file_uploader(
    "Drop an mp4, mov, or avi file here",
    type=["mp4", "mov", "avi"],
    label_visibility="collapsed"
)

if uploaded_video:
    st.success("Video received. Initialising detection pipeline.")

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_video.read())
    tfile.flush()

    try:
        import cv2
        from analytics.cv_extractor import VideoQueueAnalyzer
        analyzer = VideoQueueAnalyzer()
    except Exception as e:
        st.error(f"Failed to load CV models: {e}")
        st.stop()

    if "cv_simulator" not in st.session_state:
        st.session_state.cv_simulator = QueueSimulator(1.0, 1.0)
    simulator = st.session_state.cv_simulator

    if "cv_wait_history" not in st.session_state:
        st.session_state.cv_wait_history = []

    section_divider("Detection feed")
    video_placeholder = st.empty()

    section_divider("Live metrics")
    c1, c2, c3 = st.columns(3, gap="medium")
    pl1, pl2, pl3 = c1.empty(), c2.empty(), c3.empty()

    section_divider("Wait time trend")
    chart = st.empty()

    cap = cv2.VideoCapture(tfile.name)
    fc  = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        fc += 1
        if fc % 2 != 0:
            continue

        processed, wcount, tcount = analyzer.process_frame(frame)
        video_placeholder.image(
            cv2.cvtColor(processed, cv2.COLOR_BGR2RGB),
            channels="RGB", use_container_width=True
        )

        lam = max(0.4, (wcount / 10.0) + 0.5)
        mu  = 1.0
        simulator.arrival_rate = lam
        simulator.service_rate = mu
        simulator.step()

        wt   = calculate_waiting_time(lam, mu)
        rho  = calculate_utilization(lam, mu)
        wmin = int(max(0, (wt * 0.8) // 60))
        wmax = int(max(1, (wt * 1.2) // 60 + 1))
        status = get_service_status(rho)
        conf   = int(max(70, min(95, 95 - abs(rho - 0.5) * 20 + random.uniform(-2, 2))))
        if tcount > 0:
            conf = min(100, conf + min(15, tcount))

        update_state(admin_counter, {
            "wait_min": wmin, "wait_max": wmax,
            "status": status, "confidence": conf, "timestamp": time.time()
        })

        st.session_state.cv_wait_history.append({"Wait Time (min)": wt / 60.0})
        if len(st.session_state.cv_wait_history) > 50:
            st.session_state.cv_wait_history.pop(0)

        pl1.metric("Wait Range",    f"{wmin} – {wmax} min")
        pl2.metric("Service Status", status)
        pl3.metric("AI Confidence", f"{int(conf)}%")

        with chart:
            st.line_chart(pd.DataFrame(st.session_state.cv_wait_history), height=180)

    cap.release()
    st.success("Video processed. Broadcasting final state.")
else:
    idle_state(
        "No footage uploaded",
        "Upload a video file above to begin the computer vision detection pipeline."
    )
