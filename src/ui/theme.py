import streamlit as st
from typing import Optional, List, Tuple

GLOBAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"], .stApp, .appview-container, section.main {
    font-family: 'Inter', sans-serif !important;
    background-color: #090b10 !important;
    color: #c8d3e0 !important;
}
.stApp { background-color: #090b10 !important; }
.appview-container { background-color: #090b10 !important; }
section.main { background-color: #090b10 !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #07080d !important;
    border-right: 1px solid rgba(255,255,255,0.04) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebarContent"] {
    padding: 0 !important;
}
[data-testid="stSidebarNav"] {
    padding: 1.5rem 1rem 1rem !important;
}
[data-testid="stSidebarNav"] a {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #475569 !important;
    border-radius: 7px !important;
    padding: 9px 14px !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s !important;
    text-decoration: none !important;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(99,102,241,0.08) !important;
    color: #c7d2fe !important;
}
[data-testid="stSidebarNav"] [aria-current="page"] {
    background: rgba(99,102,241,0.12) !important;
    color: #818cf8 !important;
    font-weight: 600 !important;
}
[data-testid="stSidebarNavSeparator"] {
    display: none !important;
}
[data-testid="stSidebarNavItems"] {
    gap: 2px !important;
}

/* ── Main content area ── */
.main .block-container {
    padding: 3rem 3.5rem !important;
    max-width: 1080px !important;
}

/* ── Typography ── */
h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.035em !important;
    color: #f1f5f9 !important;
    line-height: 1.1 !important;
}
h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    color: #e2e8f0 !important;
    letter-spacing: -0.025em !important;
}
h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
    letter-spacing: -0.015em !important;
}
p, li, .stMarkdown {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    line-height: 1.75 !important;
    color: #64748b !important;
}
strong { color: #e2e8f0 !important; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.05) !important; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    padding: 18px 22px !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    color: #334155 !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f1f5f9 !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,0.4) !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div {
    background: rgba(99,102,241,0.15) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #818cf8 !important;
}

/* ── Alerts ── */
[data-testid="stInfo"] {
    background: rgba(99,102,241,0.06) !important;
    border-left: 3px solid #6366f1 !important;
    border-radius: 0 8px 8px 0 !important;
    color: #c7d2fe !important;
}
[data-testid="stSuccess"] {
    background: rgba(16,185,129,0.06) !important;
    border-left: 3px solid #10b981 !important;
    border-radius: 0 8px 8px 0 !important;
    color: #a7f3d0 !important;
}
[data-testid="stWarning"] {
    background: rgba(245,158,11,0.06) !important;
    border-left: 3px solid #f59e0b !important;
    border-radius: 0 8px 8px 0 !important;
    color: #fde68a !important;
}
[data-testid="stError"] {
    background: rgba(239,68,68,0.06) !important;
    border-left: 3px solid #ef4444 !important;
    border-radius: 0 8px 8px 0 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] section {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: rgba(99,102,241,0.4) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #090b10; }
::-webkit-scrollbar-thumb { background: #1e2330; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #2d3748; }

/* ── Code ── */
code {
    font-family: 'Space Mono', monospace !important;
    background: rgba(99,102,241,0.08) !important;
    color: #a5b4fc !important;
    padding: 2px 8px !important;
    border-radius: 4px !important;
    font-size: 0.8rem !important;
}

/* ── Charts ── */
[data-testid="stArrowVegaLiteChart"] {
    background: rgba(255,255,255,0.015) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    padding: 12px !important;
}

/* ── IQ design tokens ── */
.iq-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.iq-eyebrow::before {
    content: '';
    display: inline-block;
    width: 24px; height: 1px;
    background: #6366f1;
    flex-shrink: 0;
}
.iq-page-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: #f8fafc;
    line-height: 1.05;
    margin-bottom: 16px;
}
.iq-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    color: #475569;
    line-height: 1.8;
    max-width: 560px;
    margin-bottom: 0;
}
.iq-stat-chips {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 22px;
    padding-bottom: 40px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 48px;
}
.iq-chip {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.06em;
    color: #475569;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 4px;
    padding: 5px 12px;
}
.iq-chip strong {
    color: #94a3b8 !important;
    font-weight: 600;
}
.iq-section-divider {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #1e2330;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    margin-bottom: 22px;
    margin-top: 44px;
}
.iq-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #6366f1;
    border-radius: 10px;
    padding: 24px 28px;
    margin-bottom: 14px;
    transition: background 0.25s, border-color 0.25s;
}
.iq-card:hover {
    background: rgba(255,255,255,0.04);
    border-color: rgba(255,255,255,0.1);
    border-left-color: #6366f1;
}
.iq-card-green  { border-left-color: #10b981 !important; }
.iq-card-amber  { border-left-color: #f59e0b !important; }
.iq-card-red    { border-left-color: #ef4444 !important; }
.iq-card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
    letter-spacing: -0.01em;
    margin-bottom: 8px;
}
.iq-card-body {
    font-family: 'Inter', sans-serif;
    font-size: 0.86rem;
    color: #475569;
    line-height: 1.7;
}
.iq-idle-state {
    text-align: center;
    padding: 80px 40px;
    background: rgba(255,255,255,0.01);
    border: 1px dashed rgba(255,255,255,0.05);
    border-radius: 12px;
}
.iq-idle-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #334155;
    margin-bottom: 10px;
    letter-spacing: -0.015em;
}
.iq-idle-body {
    font-size: 0.88rem;
    color: #1e2330;
    line-height: 1.7;
}
"""

SIDEBAR_HTML = """
<div style="padding: 28px 20px 16px; border-bottom: 1px solid rgba(255,255,255,0.04);">
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.9rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: #f1f5f9;">Invisible Queue</div>
    <div style="font-family: 'Inter', sans-serif; font-size: 0.72rem; color: #334155; margin-top: 3px; letter-spacing: 0.02em;">Queue Intelligence Platform</div>
    <div style="margin-top: 10px; display: inline-block; font-family: 'Space Mono', monospace; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6366f1; background: rgba(99,102,241,0.1); border-radius: 3px; padding: 3px 8px;">Beta</div>
</div>
"""


def inject_global_css():
    st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)
    st.sidebar.markdown(SIDEBAR_HTML, unsafe_allow_html=True)


def page_header(eyebrow: str, title: str, subtitle: str, chips: Optional[List[Tuple]] = None):
    chips_html = ""
    if chips:
        chip_items = "".join(
            f'<div class="iq-chip">{k}: <strong>{v}</strong></div>'
            for k, v in chips
        )
        chips_html = f'<div class="iq-stat-chips">{chip_items}</div>'
    else:
        chips_html = '<div class="iq-stat-chips"></div>'

    st.markdown(f"""
    <div style="padding: 20px 0 0;">
        <div class="iq-eyebrow">{eyebrow}</div>
        <div class="iq-page-title">{title}</div>
        <div class="iq-subtitle">{subtitle}</div>
        {chips_html}
    </div>
    """, unsafe_allow_html=True)


def section_divider(label: str):
    st.markdown(f'<div class="iq-section-divider">{label}</div>', unsafe_allow_html=True)


def iq_card(title: str, body: str, accent: str = ""):
    cls = f"iq-card iq-card-{accent}" if accent else "iq-card"
    st.markdown(f"""
    <div class="{cls}">
        <div class="iq-card-title">{title}</div>
        <div class="iq-card-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)


def idle_state(title: str, body: str):
    st.markdown(f"""
    <div class="iq-idle-state">
        <div class="iq-idle-title">{title}</div>
        <div class="iq-idle-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)
