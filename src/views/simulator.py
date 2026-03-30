import streamlit as st
import time
import random
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from simulation.simulator import QueueSimulator
from analytics.wait_time import calculate_waiting_time
from analytics.service_status import calculate_utilization
from analytics.confidence import compute_decision_score, evaluate_decision
from ui.config import render_sidebar
from ui.scoreboard import render_scoreboard
from ui.tycoon_animation import render_tycoon_animation
from ui.theme import inject_global_css, page_header, section_divider, idle_state
from shared_state import update_state

inject_global_css()

def get_service_status(u):
    return "Normal" if u < 0.7 else ("Slowing" if u <= 1.0 else "Stalled")

page_header(
    eyebrow="Version 1",
    title="Queue Simulator",
    subtitle="Interactive M/M/1 queueing model. Configure parameters in the sidebar and observe how congestion, utilisation, and wait time evolve in real time.",
    chips=[("Model", "M/M/1"), ("Update rate", "1 Hz"), ("Iterations", "200")],
)

arrival_rate, service_rate, threshold_time, start = render_sidebar()

if "sim_simulator" not in st.session_state:
    st.session_state.sim_simulator = QueueSimulator(arrival_rate, service_rate)
st.session_state.sim_simulator.arrival_rate = arrival_rate
st.session_state.sim_simulator.service_rate = service_rate
simulator = st.session_state.sim_simulator

if "sim_wait_history" not in st.session_state:
    st.session_state.sim_wait_history = []

if start:
    section_divider("Live Metrics")
    c1, c2, c3 = st.columns(3, gap="medium")
    pl1, pl2, pl3 = c1.empty(), c2.empty(), c3.empty()

    section_divider("Wait Time Trend")
    chart = st.empty()

    simulation_container = st.empty()
    metrics_container    = st.empty()

    for _ in range(200):
        q   = simulator.step()
        wt  = calculate_waiting_time(arrival_rate, service_rate)
        rho = calculate_utilization(arrival_rate, service_rate)
        score    = compute_decision_score(wt, threshold_time)
        decision = evaluate_decision(score)

        wmin = int(max(0, (wt * 0.8) // 60))
        wmax = int(max(1, (wt * 1.2) // 60 + 1))
        status = get_service_status(rho)
        conf   = int(max(0, min(100, 95 - abs(rho - 0.5) * 20 + random.uniform(-2, 2))))

        update_state("sim_default", {
            "wait_min": wmin, "wait_max": wmax,
            "status": status, "confidence": conf, "timestamp": time.time()
        })

        st.session_state.sim_wait_history.append({"Wait Time (min)": wt / 60.0})
        if len(st.session_state.sim_wait_history) > 50:
            st.session_state.sim_wait_history.pop(0)

        pl1.metric("Wait Range",     f"{wmin} – {wmax} min")
        pl2.metric("Service Status", status)
        pl3.metric("Confidence",     f"{conf}%")

        with chart:
            st.line_chart(pd.DataFrame(st.session_state.sim_wait_history), height=180)

        with simulation_container.container(height=500, border=False):
            render_tycoon_animation(q, rho)

        with metrics_container.container():
            render_scoreboard(q, wt, rho, decision)

        time.sleep(1)
else:
    idle_state(
        "Simulation paused",
        "Set arrival rate (\u03bb) and service rate (\u03bc) in the sidebar, then press Start Simulation."
    )
