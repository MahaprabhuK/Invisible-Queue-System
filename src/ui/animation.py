# src/ui/animation.py

import streamlit as st


def render_animation(queue_length: int):
    st.subheader("Live Queue Visual")

    visual = "🧍 " * min(queue_length, 20)
    st.write(visual if visual else "No customers in queue.")
