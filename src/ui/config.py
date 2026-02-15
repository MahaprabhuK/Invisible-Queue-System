# src/ui/config.py

import streamlit as st


def render_sidebar():
    arrival_rate = st.sidebar.slider("Arrival Rate (λ)", 0.1, 1.5, 0.6)
    service_rate = st.sidebar.slider("Service Rate (μ)", 0.1, 1.5, 0.8)
    threshold_time = st.sidebar.slider("Max Acceptable Wait Time", 1.0, 30.0, 10.0)

    start = st.sidebar.button("Start Simulation")

    return arrival_rate, service_rate, threshold_time, start
