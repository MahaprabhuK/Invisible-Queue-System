# src/ui/scoreboard.py

import streamlit as st

def render_scoreboard(queue_length, waiting_time, utilization, decision):
    if utilization < 0.7:
        util_color = "#2ecc71" # Green
    elif utilization < 0.9:
        util_color = "#f1c40f" # Amber
    else:
        util_color = "#e74c3c" # Red

    st.markdown(
        f"""
        <style>
            .dark-scoreboard {{
                background-color: #0e1117;
                border: 1px solid #262730;
                border-radius: 8px;
                padding: 15px 25px;
                font-family: 'Courier New', Courier, monospace;
                display: flex;
                justify-content: space-around;
                align-items: center;
                margin: 0;
            }}
            .board-section {{
                display: flex;
                flex-direction: column;
                align-items: center;
                flex: 1;
                border-right: 1px solid #262730;
            }}
            .board-section:last-child {{
                border-right: none;
            }}
            .board-label {{
                color: #a0a0a0;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }}
            .board-value {{
                color: #ffffff;
                font-size: 2.2rem;
                font-weight: bold;
            }}
            .board-decision {{
                color: {'#2ecc71' if decision.lower() == 'worth waiting' else '#e74c3c'};
                font-size: 2.2rem;
                font-weight: bold;
            }}
        </style>

        <div class="dark-scoreboard">
            <div class="board-section">
                <div class="board-label">Expected Wait Time</div>
                <div class="board-value">{waiting_time:.1f}s</div>
            </div>
            <div class="board-section">
                <div class="board-label">Utilisation (&rho;)</div>
                <div class="board-value" style="color: {util_color};">{utilization:.2f}</div>
            </div>
            <div class="board-section">
                <div class="board-label">Decision Score</div>
                <div class="board-decision">
                    {decision.upper()}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
