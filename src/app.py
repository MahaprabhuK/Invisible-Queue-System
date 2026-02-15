import streamlit as st
import time

from simulation.simulator import QueueSimulator
from analytics.wait_time import calculate_waiting_time
from analytics.service_status import calculate_utilization
from analytics.confidence import compute_decision_score, evaluate_decision

from ui.config import render_sidebar
from ui.dashboard import render_metrics
from ui.animation import render_animation

st.set_page_config(page_title="Invisible Queue System", layout="wide")
st.title("Invisible Queue System")

arrival_rate, service_rate, threshold_time, start = render_sidebar()

if "simulator" not in st.session_state:
    st.session_state.simulator = QueueSimulator(arrival_rate, service_rate)

simulator = st.session_state.simulator

if start:
    for _ in range(200):

        queue_length = simulator.step()

        waiting_time = calculate_waiting_time(arrival_rate, service_rate)
        utilization = calculate_utilization(arrival_rate, service_rate)

        score = compute_decision_score(waiting_time, threshold_time)
        decision = evaluate_decision(score)

        render_metrics(queue_length, waiting_time, utilization, decision)
        render_animation(queue_length)

        time.sleep(1)
