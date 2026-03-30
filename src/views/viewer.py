import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared_state import get_state

VIEWER_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"], .stApp, .appview-container, section.main {
    background-color: #06070b !important;
    font-family: 'Inter', sans-serif !important;
    color: #94a3b8 !important;
}
.stApp { background-color: #06070b !important; }
[data-testid="stSidebar"]       { display: none !important; }
[data-testid="collapsedControl"]{ display: none !important; }
[data-testid="stSidebarNav"]    { display: none !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; display: none !important; }
.stDeployButton, [data-testid="stDecoration"] { display: none !important; }

.main .block-container {
    max-width: 480px !important;
    margin: 0 auto !important;
    padding: 20px 20px 60px !important;
}
.stButton > button {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    background: rgba(255,255,255,0.04) !important;
    color: #475569 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.4rem !important;
    box-shadow: none !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.07) !important;
    color: #94a3b8 !important;
    transform: none !important;
}
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #06070b; }
::-webkit-scrollbar-thumb { background: #1e2330; border-radius: 3px; }

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.35; transform: scale(0.72); }
}
"""

st.markdown(f"<style>{VIEWER_CSS}</style>", unsafe_allow_html=True)

params     = st.query_params
counter_id = params.get("counter", "default")

# Brand mark
st.markdown("""
<div style="text-align:center; padding: 48px 0 8px;">
    <div style="font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.2em; text-transform:uppercase; color:#1e2330;">
        Invisible Queue System
    </div>
</div>
""", unsafe_allow_html=True)

state = get_state(counter_id)

if not state:
    st.markdown("""
    <div style="
        margin-top: 32px;
        background: rgba(255,255,255,0.015);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 52px 32px;
        text-align: center;
    ">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.1rem; font-weight:600; color:#334155; margin-bottom:10px; letter-spacing:-0.01em;">
            No active session
        </div>
        <div style="font-size:0.85rem; color:#1e2330; line-height:1.7;">
            The counter admin has not started a session yet.<br>Please check back shortly.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    wmin        = state.get("wait_min", 0)
    wmax        = state.get("wait_max", 0)
    status_text = state.get("status", "Unknown")
    conf        = state.get("confidence", 85)

    palette = {
        "Normal":  {"hex": "#10b981", "bg": "rgba(16,185,129,0.05)",   "border": "rgba(16,185,129,0.2)"},
        "Slowing": {"hex": "#f59e0b", "bg": "rgba(245,158,11,0.05)",   "border": "rgba(245,158,11,0.2)"},
        "Stalled": {"hex": "#ef4444", "bg": "rgba(239,68,68,0.05)",    "border": "rgba(239,68,68,0.2)"},
    }
    p = palette.get(status_text, palette["Normal"])

    st.markdown(f"""
    <div style="
        margin-top: 24px;
        background: {p['bg']};
        border: 1px solid {p['border']};
        border-radius: 18px;
        padding: 48px 36px 40px;
        text-align: center;
        position: relative;
    ">
        <div style="font-family:'Space Mono',monospace; font-size:0.62rem; letter-spacing:0.16em; text-transform:uppercase; color:#334155; margin-bottom:28px;">
            Estimated wait time
        </div>
        <div style="
            font-family:'Space Grotesk',sans-serif;
            font-size: 5.5rem;
            font-weight: 700;
            letter-spacing: -0.06em;
            line-height: 1;
            color: {p['hex']};
        ">
            {wmin}<span style="font-size:2.4rem; opacity:0.5; font-weight:500;">&thinsp;&ndash;&thinsp;</span>{wmax}
        </div>
        <div style="font-family:'Inter',sans-serif; font-size:1rem; color:#334155; margin-top:6px; letter-spacing:0.04em;">minutes</div>
        <div style="margin-top: 32px; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.04);">
            <div style="display:inline-flex; align-items:center; gap:8px;">
                <div style="
                    width:7px; height:7px; border-radius:50%;
                    background:{p['hex']};
                    animation: pulse-dot 2s ease-in-out infinite;
                "></div>
                <span style="font-family:'Space Grotesk',sans-serif; font-size:0.88rem; font-weight:600; color:{p['hex']};">{status_text}</span>
                <span style="color:#1e2330; font-size:0.82rem; margin-left:8px;">
                    &middot; {conf}% confidence
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.button("Refresh", use_container_width=True)

st.markdown("""
<div style="text-align:center; margin-top:48px; font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.12em; color:#131620; text-transform:uppercase;">
    Powered by Invisible Queue System
</div>
""", unsafe_allow_html=True)
