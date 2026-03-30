import streamlit as st
import base64
import os
import sys

# Ensure imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ui.theme import inject_global_css

# Apply global dark theme first
inject_global_css()

# Override Streamlit's default container padding specifically for this full-bleed landing page
st.markdown("""
<style>
/* Remove max width and padding so iframe goes edge-to-edge */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
/* Ensure the body behind the iframe is dark */
.stApp, .appview-container, section.main {
    background-color: #05070a !important;
}
/* Strip iframe borders */
iframe {
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    display: block !important;
}
/* Hide the top header bar from Streamlit */
header[data-testid="stHeader"] {
    display: none !important;
}
/* Completely hide the Streamlit sidebar and its toggle button on the landing page */
section[data-testid="stSidebar"] {
    display: none !important;
}
button[data-testid="collapsedControl"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── Build base64 URIs for background images ──────────────────────────────────
def _b64(filename):
    path = os.path.join(os.path.dirname(__file__), "..", "ui", "assets", filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

try:
    HERO_BG  = f"data:image/png;base64,{_b64('zebc_hero.png')}"
except Exception:
    HERO_BG  = "none"

# ── The full scrollable single-page HTML ──────────────────────────────────────
PAGE_HTML = f"""
<style>
/* ── Reset ─────────────────────────────────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; font-size: 16px; }}
body {{
  color: #c4d0e0;
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  line-height: 1.6;
  overflow-x: hidden;
}}

/* ── Navbar ────────────────────────────────────────────────────────────── */
nav {{
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 99999;
  padding: 0 4vw;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: transparent;
  transition: background 0.3s ease, border-bottom 0.3s;
}}
nav.scrolled {{
  background: rgba(5,7,10,0.9);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255,0.06);
}}
.nav-brand {{
  font-family: 'General Sans', sans-serif;
  font-weight: 600;
  font-size: 1.15rem;
  letter-spacing: -0.02em;
  color: #f1f5f9;
}}
.nav-brand span {{ color: #10b981; font-weight: 500; }}
.nav-links {{
  display: flex;
  gap: 40px;
  list-style: none;
}}
.nav-links a {{
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  color: #8b9db3;
  text-decoration: none;
  transition: color 0.2s;
}}
.nav-links a:hover {{ color: #f1f5f9; }}
.nav-login {{
  display: flex;
  align-items: center;
  gap: 20px;
}}
.nav-login a.plain {{
  font-size: 0.85rem;
  font-weight: 500;
  color: #f1f5f9;
  text-decoration: none;
  transition: opacity 0.2s;
}}
.nav-login a.plain:hover {{
  opacity: 0.7;
}}
.nav-btn {{
  background: #f1f5f9;
  color: #05070a;
  padding: 10px 24px;
  border-radius: 40px;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s, transform 0.2s;
}}
.nav-btn:hover {{
  background: #fff;
  transform: translateY(-1px);
}}

/* ── Button Styles ─────────────────────────────────────────────────────── */
.btn-primary {{
  display: inline-block;
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  color: #05070a;
  background: #f1f5f9;
  border-radius: 40px;
  padding: 16px 36px;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s;
}}
.btn-primary:hover {{
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(255,255,255,0.1);
}}
.btn-secondary {{
  display: inline-block;
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  color: #f1f5f9;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 40px;
  padding: 16px 36px;
  text-decoration: none;
  transition: background 0.2s;
}}
.btn-secondary:hover {{
  background: rgba(255,255,255,0.08);
}}

/* ── HERO ──────────────────────────────────────────────────────────────── */
#hero {{
  min-height: 850px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: url('{HERO_BG}') center bottom / cover no-repeat;
  padding: 120px 10vw 0;
  position: relative;
}}
#hero::after {{
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 100%, transparent 0%, #05070a 90%);
  pointer-events: none;
  z-index: 1;
}}
.hero-content {{
  position: relative;
  z-index: 2;
  max-width: 900px;
  display: flex;
  flex-direction: column;
  align-items: center;
}}
.hero-eyebrow {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: rgba(16,185,129,0.1);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 30px;
  color: #34d399;
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.02em;
  margin-bottom: 32px;
}}
.hero-eyebrow span.dot {{
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #10b981;
}}
.hero-title {{
  font-family: 'General Sans', sans-serif;
  font-size: clamp(3rem, 6.5vw, 5.5rem);
  font-weight: 600;
  letter-spacing: -0.04em;
  line-height: 1.05;
  color: #f1f5f9;
  margin-bottom: 32px;
}}
.hero-title span {{
  background: linear-gradient(135deg, #10b981, #0ea5e9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.hero-body {{
  font-size: 1.15rem;
  font-weight: 400;
  color: #8b9db3;
  line-height: 1.7;
  max-width: 680px;
  margin-bottom: 48px;
}}
.hero-cta {{
  display: flex;
  gap: 20px;
  align-items: center;
}}

/* ── SECTIONS ──────────────────────────────────────────────────────────── */
.section-wrapper {{
  padding: 140px 5vw;
  position: relative;
  z-index: 2;
}}
.section-wrapper.darker {{
  background: #030406;
  border-top: 1px solid rgba(255,255,255,0.03);
  border-bottom: 1px solid rgba(255,255,255,0.03);
}}
.container {{
  max-width: 1200px;
  margin: 0 auto;
}}

/* ── Section Headers ── */
.sec-label {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #10b981;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 20px;
}}
.sec-title {{
  font-family: 'General Sans', sans-serif;
  font-size: clamp(2.2rem, 4vw, 3.2rem);
  font-weight: 600;
  letter-spacing: -0.03em;
  color: #f1f5f9;
  line-height: 1.1;
  max-width: 700px;
  margin-bottom: 24px;
}}
.sec-desc {{
  font-size: 1.1rem;
  color: #8b9db3;
  line-height: 1.7;
  max-width: 600px;
  margin-bottom: 64px;
}}

/* ── GRID LAYOUTS ──────────────────────────────────────────────────────── */
.grid-2 {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}}
.grid-3 {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}}
.grid-4 {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}}

/* ── CARDS (ZeBeyond Style) ────────────────────────────────────────────── */
.zb-card {{
  background: rgba(15,18,25,0.6);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 40px;
  transition: transform 0.3s, background 0.3s, border-color 0.3s;
  position: relative;
  overflow: hidden;
}}
.zb-card::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; width: 100%; height: 2px;
  background: linear-gradient(90deg, #10b981, transparent);
  opacity: 0;
  transition: opacity 0.3s;
}}
.zb-card:hover {{
  transform: translateY(-4px);
  background: rgba(15,18,25,0.9);
  border-color: rgba(255,255,255,0.1);
}}
.zb-card:hover::before {{ opacity: 1; }}

.card-tag {{
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 6px 12px;
  background: rgba(255,255,255,0.04);
  color: #8b9db3;
  border-radius: 4px;
  margin-bottom: 24px;
}}
.card-title {{
  font-family: 'General Sans', sans-serif;
  font-size: 1.35rem;
  font-weight: 500;
  color: #f1f5f9;
  margin-bottom: 16px;
}}
.card-text {{
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.6;
}}

/* ── CTA SECTION ───────────────────────────────────────────────────────── */
.cta-box {{
  background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(15,18,25,0.8));
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 20px;
  padding: 80px 60px;
  text-align: center;
  position: relative;
  overflow: hidden;
}}
.cta-box h2 {{
  font-family: 'General Sans', sans-serif;
  font-size: 3rem;
  color: #f1f5f9;
  font-weight: 600;
  margin-bottom: 24px;
  letter-spacing: -0.04em;
}}
.cta-box p {{
  font-size: 1.1rem;
  color: #8b9db3;
  max-width: 500px;
  margin: 0 auto 40px;
  line-height: 1.6;
}}

/* ── PRE-FOOTER / FOOTER ───────────────────────────────────────────────── */
footer {{
  border-top: 1px solid rgba(255,255,255,0.05);
  padding: 60px 5vw;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.f-brand {{
  font-family: 'General Sans', sans-serif;
  font-weight: 600;
  color: #f1f5f9;
  font-size: 1.1rem;
}}
.f-links {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #64748b;
}}

/* ── DETAILS LIST ──────────────────────────────────────────────────────── */
.details-list {{
  list-style: none;
  border-top: 1px solid rgba(255,255,255,0.06);
}}
.details-list li {{
  padding: 24px 0;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.dl-name {{
  font-family: 'General Sans', sans-serif;
  color: #f1f5f9;
  font-size: 1.1rem;
  font-weight: 500;
}}
.dl-role {{
  color: #8b9db3;
  font-size: 0.9rem;
}}

/* ── REVEALS ───────────────────────────────────────────────────────────── */
.reveal {{
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}
.reveal.visible {{
  opacity: 1;
  transform: translateY(0);
}}
.d-1 {{ transition-delay: 0.1s; }}
.d-2 {{ transition-delay: 0.2s; }}
.d-3 {{ transition-delay: 0.3s; }}
</style>

<!-- Navbar -->
<nav id="navbar">
  <div class="nav-brand">Invisible<span>Queue</span></div>
</nav>

<!-- 1. HERO -->
<section id="hero">
  <div class="hero-content">
    <h1 class="hero-title reveal d-1">
      Make every wait<br><span>transparent.</span>
    </h1>
    <p class="hero-body reveal d-2">
      An advanced operations platform helping service providers track, simulate, and broadcast real-time queue states before physical congestion occurs.
    </p>
  </div>
</section>

<!-- 2. THE PROBLEM -->
<section id="problem" class="section-wrapper darker">
  <div class="container">
    <div class="sec-label reveal">The Problem</div>
    <h2 class="sec-title reveal d-1">Uncertainty causes anxiety. Physical queues are information voids.</h2>
    <p class="sec-desc reveal d-2">
      Research consistently shows that unexplained, unmeasured waits feel significantly longer. Unpredictable arrival rates force customers back into crowded lobbies, elevating dissatisfaction. Existing solutions are hardware-dependent and provide zero pre-arrival visibility for the end user.
    </p>
    <div class="grid-3">
      <div class="zb-card reveal">
        <span class="card-tag">Symptom</span>
        <div class="card-title">Unknown Wait Times</div>
        <p class="card-text">Customers commit their time without any data, causing friction at peak capacity.</p>
      </div>
      <div class="zb-card reveal d-1">
        <span class="card-tag">Symptom</span>
        <div class="card-title">Reactive Operations</div>
        <p class="card-text">Staff cannot predict congestion surges until physical bottlenecks have already formed.</p>
      </div>
      <div class="zb-card reveal d-2">
        <span class="card-tag">Symptom</span>
        <div class="card-title">High Hardware Cost</div>
        <p class="card-text">Traditional queuing systems rely on expensive ticketing kiosks or proprietary sensors.</p>
      </div>
    </div>
  </div>
</section>

<!-- 3. THE SOLUTION -->
<section id="solution" class="section-wrapper">
  <div class="container">
    <div class="sec-label reveal">The Solution</div>
    <h2 class="sec-title reveal d-1">Connecting physical density with queuing theory.</h2>
    <p class="sec-desc reveal d-2">
      We combined classical M/M/1 mathematical models with modern computer vision. Existing security cameras become sensors, instantly feeding arrival data into our probability engine to broadcast 95% confidence intervals directly to customer smartphones.
    </p>
    <div class="grid-2">
      <div class="zb-card reveal">
        <span class="card-tag">Layer 1: Extraction</span>
        <div class="card-title">YOLOv8 Object Detection</div>
        <p class="card-text">Our pipeline processes live video feeds. It identifies and tracks queue occupants, automatically calculating dynamic arrival rates (&lambda;) without relying on manual entry.</p>
      </div>
      <div class="zb-card reveal d-1">
        <span class="card-tag">Layer 2: Calculation</span>
        <div class="card-title">M/M/1 Probability Engine</div>
        <p class="card-text">Using the extracted arrival rates, the platform models service utilization (&rho;). It then computes robust wait time estimations using validated probability operations research.</p>
      </div>
    </div>
  </div>
</section>

<!-- 4. WHERE IT CAN BE USED -->
<section id="use_cases" class="section-wrapper darker">
  <div class="container">
    <div class="sec-label reveal">Where it's used</div>
    <h2 class="sec-title reveal d-1">Engineered for high-volume environments.</h2>
    <p class="sec-desc reveal d-2">
      The Invisible Queue platform operates passively using existing camera hardware, making it immediately viable across physical storefronts and transit hubs.
    </p>
    <div class="grid-3">
      <div class="zb-card reveal">
        <span class="card-tag">Aviation</span>
        <div class="card-title">Airport Check-ins</div>
        <p class="card-text">Prevent pre-flight panic by broadcasting real-time terminal gate congestion directly to passenger booking apps.</p>
      </div>
      <div class="zb-card reveal d-1">
        <span class="card-tag">Healthcare</span>
        <div class="card-title">Clinical Triage</div>
        <p class="card-text">Reduce perceived wait anxiety in outpatient reception and pharmacy departments.</p>
      </div>
      <div class="zb-card reveal d-2">
        <span class="card-tag">Retail</span>
        <div class="card-title">Checkout Lines</div>
        <p class="card-text">Predictive modelling uncovers utilization bottlenecks so managers can proactively deploy staff.</p>
      </div>
    </div>
  </div>
</section>

<!-- 5. TOOLS / CTA (V1 and V2) -->
<section id="simulation" class="section-wrapper">
  <div class="container">
    <div class="cta-box reveal">
      <h2 style="font-size: 2rem; margin-bottom: 12px;">Experience the engine</h2>
      <p>Test the theory in our interactive simulator, or deploy the CV model on actual video footage.</p>
      <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
        <a href="/?page=simulator" target="_blank" class="btn-secondary">Simulator (Version 1)</a>
        <a href="/?page=cv_detection" target="_blank" class="btn-primary" style="background: #10b981; color: #000; box-shadow: 0 4px 20px rgba(16,185,129,0.3);">CV Pipeline (Version 2)</a>
      </div>
    </div>
  </div>
</section>

<!-- 6. ABOUT US & TOOLS USED -->
<section id="about" class="section-wrapper darker">
  <div class="container">
    <div class="grid-2">
      <!-- About Us -->
      <div>
        <div class="sec-label reveal">About Us</div>
        <h2 class="sec-title reveal d-1" style="font-size: 2rem;">The Team</h2>
        <p class="sec-desc reveal d-2" style="margin-bottom: 32px; max-width: 400px;">
          Built by a team of engineers dedicated to solving operational bottlenecks through the application of modern AI on classical operations research.
        </p>
        <ul class="details-list reveal d-3" style="max-width: 400px;">
          <li>
            <span class="dl-name">Mahaprabhu K</span>
            <span class="dl-role">Pipeline Engineering</span>
          </li>
          <li>
            <span class="dl-name">Pavithran P</span>
            <span class="dl-role">Model Architecture</span>
          </li>
          <li>
            <span class="dl-name">Varanasi Teja</span>
            <span class="dl-role">Frontend Design</span>
          </li>
        </ul>
      </div>
      
      <!-- Tools Used -->
      <div>
        <div class="sec-label reveal">Tech Stack</div>
        <h2 class="sec-title reveal d-1" style="font-size: 2rem;">Tools Used</h2>
        <div class="grid-2 reveal d-2" style="margin-top: 32px;">
          <div class="zb-card" style="padding: 24px;">
            <div class="card-title" style="font-size: 1.1rem;">Python</div>
            <p class="card-text" style="font-size: 0.8rem;">Core backend logic and mathematical routing.</p>
          </div>
          <div class="zb-card" style="padding: 24px;">
            <div class="card-title" style="font-size: 1.1rem;">YOLOv8</div>
            <p class="card-text" style="font-size: 0.8rem;">Ultralytics state-of-the-art object detection.</p>
          </div>
          <div class="zb-card" style="padding: 24px;">
            <div class="card-title" style="font-size: 1.1rem;">Streamlit</div>
            <p class="card-text" style="font-size: 0.8rem;">Rapid frontend state management and deploy.</p>
          </div>
          <div class="zb-card" style="padding: 24px;">
            <div class="card-title" style="font-size: 1.1rem;">OpenCV</div>
            <p class="card-text" style="font-size: 0.8rem;">Video frame extraction and tensor formatting.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="f-brand">Invisible Queue</div>
  <div class="f-links">Powered by Python & Streamlit</div>
</footer>

<script>
// ── Navbar scroll state ───────────────────────────────────────────────────
const navbar = window.parent.document.getElementById('navbar') || document.getElementById('navbar');
if(navbar) {{
    window.addEventListener('scroll', () => {{
      if (window.scrollY > 60) {{
        navbar.classList.add('scrolled');
      }} else {{
        navbar.classList.remove('scrolled');
      }}
    }}, {{ passive: true }});
}}

// ── Reveal on scroll ──────────────────────────────────────────────────────
const reveals = document.querySelectorAll('.reveal');
const io = new IntersectionObserver((entries) => {{
  entries.forEach(entry => {{
    if (entry.isIntersecting) {{
      entry.target.classList.add('visible');
      io.unobserve(entry.target);
    }}
  }});
}}, {{ threshold: 0.1 }});
reveals.forEach(el => io.observe(el));

// Trigger hero reveals immediately
document.querySelectorAll('#hero .reveal').forEach(el => {{
  setTimeout(() => el.classList.add('visible'), 150);
}});
</script>
"""

# ── Render fullscreen ──────────────────────────────────────────────────────────
import streamlit.components.v1 as components
components.html(PAGE_HTML, height=5200, scrolling=False)

