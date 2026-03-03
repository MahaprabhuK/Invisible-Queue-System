import streamlit as st
import time

from simulation.simulator import QueueSimulator
from analytics.wait_time import calculate_waiting_time
from analytics.service_status import calculate_utilization
from analytics.confidence import compute_decision_score, evaluate_decision

from ui.config import render_sidebar
from ui.scoreboard import render_scoreboard
from ui.tycoon_animation import render_tycoon_animation

st.set_page_config(page_title="Invisible Queue System", layout="wide")
st.title("Invisible Queue System")

arrival_rate, service_rate, threshold_time, start = render_sidebar()

if "simulator" not in st.session_state:
    st.session_state.simulator = QueueSimulator(arrival_rate, service_rate)

simulator = st.session_state.simulator

if start:
    # Create placeholders for live updates
    simulation_container = st.empty()
    metrics_container = st.empty()

    for _ in range(200):

        queue_length = simulator.step()

        waiting_time = calculate_waiting_time(arrival_rate, service_rate)
        utilization = calculate_utilization(arrival_rate, service_rate)

        score = compute_decision_score(waiting_time, threshold_time)
        decision = evaluate_decision(score)

        with simulation_container.container(height=500, border=False):
            render_tycoon_animation(queue_length, utilization)

        with metrics_container.container():
            render_scoreboard(queue_length, waiting_time, utilization, decision)

        time.sleep(1)
