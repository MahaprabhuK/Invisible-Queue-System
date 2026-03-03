import streamlit as st
import streamlit.components.v1 as components

def render_tycoon_animation(queue_length, utilization=0.0):
    """
    Renders pure HTML + SVG spatial Tycoon-style animation.
    Requirements: single <svg> element, fixed 500px height, no JS.
    """
    
    # Track previous queue length in session state to compute deltas for animations
    if "prev_queue_length" not in st.session_state:
        st.session_state.prev_queue_length = queue_length
        
    prev_q = st.session_state.prev_queue_length
    st.session_state.prev_queue_length = queue_length
    
    # Determine visual congestion modes based on Utilization
    if utilization < 0.7:
        bg_color = "#0e1117"       # Normal dark theme
        overlay_color = "rgba(0, 0, 0, 0)"
        banner_text = ""
        banner_color = "transparent"
        banner_display = "none"
        banner_stroke = "none"
    elif utilization < 0.9:
        bg_color = "#0e1117"       
        overlay_color = "rgba(241, 196, 15, 0.15)" # Subtle amber warning overlay
        banner_text = "HIGH TRAFFIC"
        banner_color = "#f1c40f"
        banner_display = "inline"
        banner_stroke = "#f1c40f"
    else:
        bg_color = "#0e1117"       
        overlay_color = "rgba(231, 76, 60, 0.2)" # Subtle red congestion overlay
        banner_text = "CONGESTED"
        banner_color = "#e74c3c"
        banner_display = "inline"
        banner_stroke = "#e74c3c"
        
    # Predefined array of fixed X coordinates spaced evenly
    # Slot 0 is closest to the counter, growing towards the left
    fixed_slots = [800 - (i * 40) for i in range(150)]
    
    agents_svg = ""
    colors = ["#ffb703", "#8ECAE6", "#219EBC", "#023047", "#fb8500"]
    
    # Render queue agents efficiently using fixed slots
    for i in range(queue_length):
        if i >= len(fixed_slots):
            break
            
        cx = fixed_slots[i]
        
        # Performance optimization: do not render SVG nodes that are way off the left screen
        if cx < -100:
            continue
            
        anim_class = ""
        cx_prev = cx
        # Slide in new agents from the left
        if queue_length > prev_q and i >= prev_q:
            anim_class = "agent-enter"
        # Shift remaining agents forward safely when someone is serviced
        elif queue_length < prev_q:
            anim_class = "agent-shift"
            idx_prev = i + (prev_q - queue_length)
            cx_prev = fixed_slots[idx_prev] if idx_prev < len(fixed_slots) else fixed_slots[-1]
            
        color = colors[i % len(colors)]
        
        agents_svg += f'''
        <g class="agent-pos {anim_class}" style="--start-x: {cx - 50}px; --prev-x: {cx_prev}px; --end-x: {cx}px; --exit-x: {cx + 60}px; --ty: 230px; transform: translate({cx}px, 230px);">
            <g class="agent-bob type-{i % 3}">
                <!-- Passenger Silhouette centered around 0,0 -->
                <circle cx="0" cy="-25" r="12" fill="#ffdbac" /> <!-- Head -->
                <rect x="-14" y="-8" width="28" height="30" rx="5" fill="{color}" /> <!-- Torso -->
                <!-- Simple Legs -->
                <rect x="-10" y="22" width="6" height="18" rx="3" fill="#34495e" />
                <rect x="4" y="22" width="6" height="18" rx="3" fill="#34495e" />
            </g>
        </g>
        '''
        
    # Exiting ghost sliding into the service desk boundary
    if queue_length < prev_q:
        cx_exit = fixed_slots[0]
        agents_svg += f'''
        <g class="agent-pos agent-exit" style="--end-x: {cx_exit}px; --exit-x: {cx_exit + 60}px; --ty: 230px; transform: translate({cx_exit}px, 230px);">
            <!-- Passenger Silhouette centered around 0,0 -->
            <circle cx="0" cy="-25" r="12" fill="#ffdbac" /> <!-- Head -->
            <rect x="-14" y="-8" width="28" height="30" rx="5" fill="{colors[0]}" /> <!-- Torso -->
            <!-- Simple Legs -->
            <rect x="-10" y="22" width="6" height="18" rx="3" fill="#34495e" />
            <rect x="4" y="22" width="6" height="18" rx="3" fill="#34495e" />
        </g>
        '''

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: {bg_color};
                height: 500px;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Courier New', Courier, monospace;
            }}
            
            svg {{
                width: 100%;
                height: 100%;
                display: block;
            }}
            
            /* Bobbing animation */
            .agent-bob {{
                animation: bob 0.8s infinite alternate ease-in-out;
            }}
            .agent-bob.type-0 {{ animation-delay: 0s; }}
            .agent-bob.type-1 {{ animation-delay: 0.2s; }}
            .agent-bob.type-2 {{ animation-delay: 0.4s; }}
            
            @keyframes bob {{
                0% {{ transform: translateY(-4px); }}
                100% {{ transform: translateY(4px); }}
            }}
            
            /* Entrance Animation (Slides in nicely without flicker) */
            .agent-enter {{
                opacity: 0;
                animation: enter-slide 0.8s ease-out forwards;
                transition: transform 0.8s ease-out, opacity 0.8s ease-out;
            }}
            @keyframes enter-slide {{
                0% {{ opacity: 0; transform: translate(var(--start-x), var(--ty)); }}
                100% {{ opacity: 1; transform: translate(var(--end-x), var(--ty)); }}
            }}
            
            /* Exit Animation (Slides right into the desk and fades out) */
            .agent-exit {{
                opacity: 1;
                animation: exit-slide 0.8s ease-in forwards !important;
                transition: transform 0.8s ease-in, opacity 0.8s ease-in;
            }}
            @keyframes exit-slide {{
                0% {{ opacity: 1; transform: translate(var(--end-x), var(--ty)); }}
                100% {{ opacity: 0; transform: translate(var(--exit-x), var(--ty)); }}
            }}
            
            /* Shift forward animation for remaining queue */
            .agent-shift {{
                animation: shift-forward 0.8s ease-in-out forwards;
            }}
            @keyframes shift-forward {{
                0% {{ transform: translate(var(--prev-x), var(--ty)); }}
                100% {{ transform: translate(var(--end-x), var(--ty)); }}
            }}
            
            .congestion-banner {{
                animation: pulse 2s infinite;
                transform-origin: 840px 406px;
            }}
            @keyframes pulse {{
                0% {{ opacity: 0.8; transform: scale(1); }}
                50% {{ opacity: 1; transform: scale(1.05); }}
                100% {{ opacity: 0.8; transform: scale(1); }}
            }}
            
            /* Full Scene Tint Overlay */
            .congestion-overlay {{
                transition: fill 1s ease-in-out;
                pointer-events: none;
            }}
        </style>
    </head>
    <body>
        <svg viewBox="0 0 1000 500" preserveAspectRatio="xMidYMid slice">
            
            <!-- BACKGROUND SCENE -->
            <!-- Base Wall -->
            <rect x="0" y="0" width="1000" height="500" fill="transparent" />
            
            <!-- Large Back Window -->
            <rect x="50" y="50" width="900" height="250" rx="15" fill="#87CEEB" stroke="#2c3e50" stroke-width="8" />
            
            <!-- Window Panes (Mullions) -->
            <line x1="350" y1="50" x2="350" y2="300" stroke="#2c3e50" stroke-width="6" />
            <line x1="650" y1="50" x2="650" y2="300" stroke="#2c3e50" stroke-width="6" />
            <line x1="50" y1="175" x2="950" y2="175" stroke="#2c3e50" stroke-width="6" />
            
            <!-- SVG Clouds outside window -->
            <g fill="#ffffff" opacity="0.8">
                <!-- Cloud 1 -->
                <circle cx="150" cy="120" r="30" />
                <circle cx="190" cy="110" r="40" />
                <circle cx="230" cy="120" r="30" />
                <rect x="150" y="120" width="80" height="30" />
                
                <!-- Cloud 2 -->
                <circle cx="750" cy="180" r="25" />
                <circle cx="785" cy="170" r="35" />
                <circle cx="820" cy="180" r="25" />
                <rect x="750" y="180" width="70" height="25" />
            </g>
            
            <!-- Floor Layer -->
            <rect x="0" y="320" width="1000" height="180" fill="#2c3e50" opacity="0.4" />
            
            <!-- Floor Stripe/Guide -->
            <line x1="0" y1="350" x2="800" y2="350" stroke="#f1c40f" stroke-width="4" stroke-dasharray="20,10" />
            
            <!-- Airport Departure Board (Top Right) -->
            <g transform="translate(730, 20)">
                <rect x="0" y="0" width="220" height="46" rx="6" fill="#1f2833" stroke="#45a29e" stroke-width="2" />
                <text x="110" y="28" fill="#66fcf1" font-size="18" font-weight="bold" text-anchor="middle">In Queue: {queue_length}</text>
            </g>

            <!-- Check-in Desk Base (Right Side) -->
            <path d="M 830,220 L 980,220 L 980,480 L 830,480 Z" fill="#34495e" stroke="#2c3e50" stroke-width="4" />
            <rect x="820" y="200" width="170" height="25" rx="5" fill="#ecf0f1" stroke="#bdc3c7" stroke-width="2" />
            <rect x="840" y="225" width="140" height="10" fill="#2c3e50" />
            
            <!-- Computed SVG Agents -->
            {agents_svg}
            
            <!-- Utilization Scene Overlay (tints environment and agents but not UI) -->
            <rect class="congestion-overlay" x="0" y="0" width="1000" height="500" fill="{overlay_color}" />
            
            <!-- Dynamic Congestion Banner -->
            <g class="congestion-banner" style="display: {banner_display};">
                <rect x="750" y="380" width="180" height="40" rx="5" fill="rgba(0,0,0,0.6)" stroke="{banner_stroke}" stroke-width="2"/>
                <text x="840" y="406" fill="{banner_color}" font-size="16" font-weight="bold" text-anchor="middle">{banner_text}</text>
            </g>
        </svg>
    </body>
    </html>
    """
    
    components.html(html_code, height=500, scrolling=False)
