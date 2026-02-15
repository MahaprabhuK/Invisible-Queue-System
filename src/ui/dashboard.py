# src/ui/dashboard.py

import streamlit as st


def render_metrics(queue_length,
                   waiting_time,
                   utilization,
                   decision):

    col1, col2, col3 = st.columns(3)

    col1.metric("People in Queue", queue_length)
    col2.metric("Estimated Waiting Time", f"{waiting_time:.2f}")
    col3.metric("Utilization (ρ)", f"{utilization:.2f}")

    if decision == "Worth Waiting":
        st.success(decision)
    elif decision == "System Overloaded":
        st.error(decision)
    else:
        st.warning(decision)
