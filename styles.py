"""
Global CSS Styling for StockSense AI
Exact match to Reference Image at 1488x835 Viewport
- Sidebar: 260px fixed width, dark emerald #003F35 with fluid bottom waves
- Active Nav: #087E69 elevated pill, 15-16px Inter font, 44px height
- Main Canvas: Warm cream #FBF8F0, Cards #FFFEFA, Borders #EAE6DE
- Typography: Inter / Plus Jakarta Sans, Headings #102238, Subtitles #087E69, Supporting #52677A
"""

MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

/* ── ANIMATIONS ──────────────────────────────────────────────────────── */
@keyframes pulse-dot {
  0%   { box-shadow: 0 0 0 0 rgba(22,163,74,0.7); transform: scale(0.95); }
  70%  { box-shadow: 0 0 0 7px rgba(22,163,74,0); transform: scale(1.05); }
  100% { box-shadow: 0 0 0 0 rgba(22,163,74,0); transform: scale(0.95); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ── RESET & BASE APPLICATION ────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background-color: #FBF8F0 !important;
    background: #FBF8F0 !important;
    font-family: 'Inter', 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: #102238 !important;
    -webkit-font-smoothing: antialiased;
}

.block-container {
    padding: 16px 28px 16px 28px !important;
    max-width: 100% !important;
    animation: fadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

[data-testid="stMain"] div[data-testid="stVerticalBlock"] {
    gap: 10px !important;
}

[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    gap: 4px !important;
}

/* Hide Streamlit default chrome completely */
#MainMenu { visibility: hidden !important; display: none !important; }
footer { visibility: hidden !important; display: none !important; }
header { visibility: hidden !important; display: none !important; height: 0 !important; }
[data-testid="stHeader"] { display: none !important; visibility: hidden !important; height: 0 !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

/* ── SIDEBAR PANEL (USER-ADJUSTABLE WIDTH & EMERALD GRADIENT WITH INTEGRATED ORGANIC WAVE) ── */
[data-testid="stSidebar"],
section[data-testid="stSidebar"] {
    background: 
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 240' fill='none'%3E%3Cpath d='M-20 180 C80 140, 160 210, 260 160 C320 130, 370 170, 420 150 L420 240 L-20 240 Z' fill='rgba(11, 166, 91, 0.08)'/%3E%3Cpath d='M-20 140 C100 190, 180 120, 280 180 C340 210, 390 170, 420 185 L420 240 L-20 240 Z' fill='rgba(20, 184, 166, 0.05)'/%3E%3Cpath d='M-20 155 C70 115, 150 185, 250 145 C320 115, 370 160, 420 135' stroke='rgba(52, 211, 153, 0.20)' stroke-width='1.8' fill='none'/%3E%3Cpath d='M-20 175 C80 135, 170 205, 270 165 C330 140, 380 180, 420 160' stroke='rgba(20, 184, 166, 0.15)' stroke-width='1.4' fill='none'/%3E%3Cpath d='M-20 195 C90 160, 190 220, 290 185 C350 165, 390 195, 420 180' stroke='rgba(52, 211, 153, 0.10)' stroke-width='1.2' fill='none'/%3E%3C/svg%3E") no-repeat bottom center / 100% 240px,
        linear-gradient(180deg, #003F35 0%, #002E28 100%) !important;
    background-color: #002E28 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    min-width: 260px !important;
    max-width: 480px !important;
    width: 320px;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15) !important;
    resize: horizontal !important;
    overflow-x: hidden !important;
}

[data-testid="stSidebar"] > div:first-child,
div[data-testid="stSidebarContent"] {
    background: transparent !important;
    padding: 1.0rem 1.25rem 1.4rem 1.25rem !important;
    overflow-x: hidden !important;
    overflow-y: auto !important;
    min-width: 260px !important;
    max-width: 480px !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}

/* Suppress all scrollbars in sidebar completely */
[data-testid="stSidebar"],
[data-testid="stSidebar"] * {
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}
[data-testid="stSidebar"]::-webkit-scrollbar,
div[data-testid="stSidebarContent"]::-webkit-scrollbar,
section[data-testid="stSidebar"]::-webkit-scrollbar {
    display: none !important;
    width: 0px !important;
    height: 0px !important;
}

/* Sidebar resize handle: borderless, transparent idle with emerald glow on hover */
[data-testid="stSidebarResizeHandle"],
div[data-testid="stSidebarUserResizeHandle"],
div[class*="resize-handle"],
div[class*="ResizeHandle"] {
    width: 6px !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    cursor: col-resize !important;
    transition: background 0.2s ease !important;
    z-index: 9999 !important;
}

[data-testid="stSidebarResizeHandle"]:hover,
div[data-testid="stSidebarUserResizeHandle"]:hover,
div[class*="resize-handle"]:hover,
div[class*="ResizeHandle"]:hover {
    background: #0BA65B !important;
    box-shadow: 0 0 10px rgba(11, 166, 91, 0.5) !important;
}

/* Make main content flexibly adapt to any sidebar width */
section[data-testid="stMain"] {
    flex: 1 1 0% !important;
    min-width: 0 !important;
    width: auto !important;
}

/* ── UNIVERSAL CARD CONTAINERS (SCOPED TO REAL CARDS ONLY) ────────────────── */
[data-testid="stMain"] div[data-testid="stLayoutWrapper"] {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    position: relative !important;
    padding: 0 !important;
}

[data-testid="stMain"] div[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"]:not([data-test-wrap="false"]) {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    gap: 2px !important;
}

/* ── UNIVERSAL CARD CONTAINERS (ALL BORDERED CONTAINERS ACROSS ALL PAGES) ── */
[data-testid="stMain"] div[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"],
[data-testid="stMain"] div[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMain"] div[data-testid="stVerticalBlock"][data-test-wrap="false"],
[data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMain"] div.st-emotion-cache-1fpp8sd {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid #EBE6DC !important;
    border-radius: 16px !important;
    padding: 16px 20px 14px 20px !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02) !important;
    position: relative !important;
    overflow: hidden !important;
    gap: 6px !important;
}

/* Ensure no double border if both layout wrapper and inner vertical block match */
[data-testid="stMain"] div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) > div[data-testid="stVerticalBlock"],
[data-testid="stMain"] div[data-testid="stLayoutWrapper"]:has(.chart-box-marker) > div[data-testid="stVerticalBlock"] {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* Sidebar navigation buttons — TRANSPARENT IDLE, WHITE TEXT, 48px HEIGHT, 18.5px FONT */
[data-testid="stSidebar"] .stButton > button,
section[data-testid="stSidebar"] .stButton > button {
    background-color: transparent !important;
    background: transparent !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 18.5px !important;
    font-weight: 650 !important;
    padding: 0 18px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    align-items: center !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: none !important;
    min-height: 48px !important;
    height: 48px !important;
    margin-bottom: 4px !important;
    width: 100% !important;
    letter-spacing: -0.01em !important;
    display: flex !important;
    flex-direction: row !important;
    gap: 16px !important;
}

/* Force strict left-alignment for Streamlit emotion cache wrappers inside buttons */
[data-testid="stSidebar"] .stButton > button > div,
[data-testid="stSidebar"] .stButton > button > div > span,
[data-testid="stSidebar"] .stButton > button span[class*="eqzt73c"] {
    display: flex !important;
    flex-direction: row !important;
    justify-content: flex-start !important;
    align-items: center !important;
    text-align: left !important;
    width: 100% !important;
    gap: 16px !important;
}

[data-testid="stSidebar"] .stButton > button div[data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] .stButton > button div[data-testid="stMarkdownContainer"] p {
    text-align: left !important;
    font-size: 18.5px !important;
    font-weight: 650 !important;
    margin: 0 !important;
    padding: 0 !important;
    color: inherit !important;
    display: flex !important;
    align-items: center !important;
}

/* Material Icons inside sidebar buttons */
[data-testid="stSidebar"] .stButton [data-testid="stIconMaterial"],
[data-testid="stSidebar"] .stButton span[translate="no"] {
    font-size: 24px !important;
    width: 26px !important;
    height: 26px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: inherit !important;
    flex-shrink: 0 !important;
}

[data-testid="stSidebar"] .stButton > button:hover,
section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
    background: rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
    transform: translateX(3px);
    box-shadow: none !important;
}

/* Active navigation pill — #087F68 matching specification */
[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #087F68 !important;
    background-color: #087F68 !important;
    color: #ffffff !important;
    font-weight: 750 !important;
    font-size: 18.5px !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(8, 127, 104, 0.45) !important;
    border-radius: 12px !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
[data-testid="stSidebar"] [data-testid="baseButton-primary"]:hover {
    background: #0B8E75 !important;
    color: #ffffff !important;
}

/* Sidebar Market & Benchmark controls */
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: rgba(0, 48, 40, 0.65) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    margin-top: 14px !important;
    overflow: hidden !important;
}

[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: #8FAFA2 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    padding: 8px 12px !important;
}

[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] .sidebar-controls-card {
    background: rgba(0, 48, 40, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 12px 14px;
    margin-top: 14px;
    margin-bottom: 12px;
}

/* Sidebar Form Controls (React-Aria & BaseWeb ComboBox Support) */
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stTextInput {
    width: 100% !important;
    margin-bottom: 8px !important;
}

/* The dropdown container box */
[data-testid="stSidebar"] .stSelectbox div[role="group"],
[data-testid="stSidebar"] .react-aria-ComboBox div[role="group"],
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: rgba(0, 48, 40, 0.95) !important;
    background: rgba(0, 48, 40, 0.95) !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    height: 42px !important;
    display: flex !important;
    align-items: center !important;
    padding: 0 6px 0 12px !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] .stSelectbox div[role="group"]:hover,
[data-testid="stSidebar"] .stSelectbox div[role="group"]:focus-within {
    border-color: #34D399 !important;
    box-shadow: 0 0 0 2px rgba(52, 211, 153, 0.2) !important;
}

/* The combobox input element — CRITICAL: flex: 1 and bright white text */
[data-testid="stSidebar"] .react-aria-ComboBox input,
[data-testid="stSidebar"] [data-testid="stSelectbox"] input,
[data-testid="stSidebar"] .stSelectbox input {
    flex: 1 1 auto !important;
    width: 100% !important;
    min-width: 0 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 650 !important;
    padding: 0 4px !important;
    height: 100% !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Dropdown arrow button */
[data-testid="stSidebar"] .react-aria-ComboBox button,
[data-testid="stSidebar"] [data-testid="stSelectbox"] button,
[data-testid="stSidebar"] .stSelectbox button {
    background: transparent !important;
    border: none !important;
    color: #A7C9BE !important;
    cursor: pointer !important;
    padding: 0 !important;
    margin: 0 !important;
    width: 28px !important;
    min-width: 28px !important;
    max-width: 28px !important;
    height: 100% !important;
    flex: 0 0 28px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] .react-aria-ComboBox button svg,
[data-testid="stSidebar"] [data-testid="stSelectbox"] button svg {
    fill: #A7C9BE !important;
    color: #A7C9BE !important;
    width: 17px !important;
    height: 17px !important;
}

/* Sidebar Custom text input */
[data-testid="stSidebar"] .stTextInput div[data-testid="stTextInputRootElement"],
[data-testid="stSidebar"] .stTextInput [data-baseweb="input"] {
    background-color: rgba(0, 48, 40, 0.95) !important;
    background: rgba(0, 48, 40, 0.95) !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    height: 42px !important;
    padding: 0 !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] .stTextInput div[data-testid="stTextInputRootElement"]:focus-within {
    border-color: #34D399 !important;
    box-shadow: 0 0 0 2px rgba(52, 211, 153, 0.2) !important;
}

[data-testid="stSidebar"] .stTextInput input {
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important; /* REMOVE MAGNIFYING GLASS FROM SIDEBAR */
    border: none !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 650 !important;
    height: 40px !important;
    padding: 0 12px !important;
    width: 100% !important;
    outline: none !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: #8FAFA2 !important;
    -webkit-text-fill-color: #8FAFA2 !important;
}

/* CRITICAL: DISABLE GREEN ARROW BUTTON ON SIDEBAR TEXT INPUT */
[data-testid="stSidebar"] [data-testid="stTextInput"]::after {
    display: none !important;
    content: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* Sidebar field labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #E1F2EC !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em !important;
    margin-bottom: 5px !important;
    text-transform: none !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── SEARCH BAR PILL IN MAIN CONTENT (52px HEIGHT WITH GREEN ARROW BUTTON) ─── */
[data-testid="stMain"] [data-testid="stTextInput"],
.block-container [data-testid="stTextInput"] {
    position: relative !important;
    max-width: 860px !important;
    width: 100% !important;
}

[data-testid="stMain"] [data-testid="stTextInput"] [data-baseweb="base-input"],
[data-testid="stMain"] [data-testid="stTextInput"] [data-baseweb="input"],
[data-testid="stMain"] [data-testid="stTextInput"] div[data-testid="stTextInputRootElement"],
[data-testid="stMain"] [data-testid="stTextInput"] > div,
[data-testid="stMain"] [data-testid="stTextInput"] > div > div {
    background-color: transparent !important;
    border: none !important;
    border-radius: 30px !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="stMain"] [data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    border: 1px solid #E8E5DC !important;
    border-radius: 14px !important;
    color: #102238 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15.5px !important;
    height: 52px !important;
    padding: 0 54px 0 46px !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02) !important;
    transition: all 0.2s ease !important;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='19' height='19' viewBox='0 0 24 24' fill='none' stroke='%2352677A' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'%3E%3C/circle%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'%3E%3C/line%3E%3C/svg%3E") !important;
    background-repeat: no-repeat !important;
    background-position: 18px center !important;
}

[data-testid="stMain"] [data-testid="stTextInput"] input:focus {
    border-color: #087F68 !important;
    box-shadow: 0 0 0 3px rgba(8, 127, 104, 0.16) !important;
    outline: none !important;
}

[data-testid="stMain"] [data-testid="stTextInput"] input::placeholder {
    color: #8FAFA2 !important;
    font-size: 15px !important;
}

[data-testid="stMain"] [data-testid="stTextInput"]::after {
    display: none !important;
    content: none !important;
}

/* ── INTERACTIVE SEARCH PILL FOCUS & HOVER STATES ───────────────────── */
.ss-search-pill:focus-within {
    border-color: #087E69 !important;
    box-shadow: 0 0 0 3px rgba(8, 126, 105, 0.16) !important;
}

[data-testid="stMain"] button.ss-search-submit-btn,
.ss-search-pill button.ss-search-submit-btn,
.ss-search-pill button {
    width: 38px !important;
    height: 38px !important;
    min-width: 38px !important;
    min-height: 38px !important;
    max-width: 38px !important;
    max-height: 38px !important;
    border-radius: 50% !important;
    background-color: #003F35 !important;
    background: #003F35 !important;
    border: none !important;
    color: #FFFFFF !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
    margin: 0 !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(0, 63, 53, 0.35) !important;
    transition: all 0.2s ease !important;
    font-size: 18px !important;
    line-height: 1 !important;
}

[data-testid="stMain"] button.ss-search-submit-btn:hover,
.ss-search-pill button.ss-search-submit-btn:hover,
.ss-search-pill button:hover {
    background-color: #087E69 !important;
    background: #087E69 !important;
    transform: scale(1.06) !important;
}

.ss-search-pill button svg {
    display: block !important;
    width: 17px !important;
    height: 17px !important;
}

/* ── PLOTLY CHART CONTAINER (NO HEAVY BORDERS OR SCROLLBARS) ─────────── */
.stPlotlyChart {
    background-color: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
    overflow: hidden !important;
}

.js-plotly-plot .plotly .main-svg { background: transparent !important; }

/* ── DEDICATED ROUNDED CARDS FOR ANALYTICS SECTION ─────────────────────── */
div[data-testid="stColumn"]:has(.analytics-map-card),
div[data-testid="stColumn"]:has(.analytics-movers-card),
div[data-testid="stVerticalBlock"]:has(> div > div > .analytics-map-card),
div[data-testid="stVerticalBlock"]:has(> div > div > .analytics-movers-card),
div[data-testid="stElementContainer"]:has(.analytics-map-card) ~ *,
div[data-testid="stElementContainer"]:has(.analytics-movers-card) ~ * {
    /* ensure smooth spacing inside analytics columns */
}

div[data-testid="stColumn"]:has(.analytics-map-card),
div[data-testid="stColumn"]:has(.analytics-movers-card) {
    background: #FFFEFA !important;
    background-color: #FFFEFA !important;
    border: 1px solid #E9E5DC !important;
    border-radius: 18px !important;
    padding: 16px 20px 12px 20px !important;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.02) !important;
    min-height: 470px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
}

/* ── STOCK EXPLORER STYLING (PILLS, BUTTONS & CARDS) ───────────────────── */
[data-testid="stMain"] .explorer-chart-marker,
[data-testid="stMain"] .stock-id-marker,
[data-testid="stMain"] .chart-box-marker {
    display: none !important;
}

/* Company ID Card Container (Scoped to stLayoutWrapper) */
div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid #EBE6DC !important;
    border-radius: 16px !important;
    padding: 12px 20px 10px 20px !important;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.02) !important;
    position: relative !important;
    overflow: hidden !important;
}

div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) > div[data-testid="stVerticalBlock"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    gap: 0 !important;
}

/* Chart Box Card Container (Housing both pills & plot) */
div[data-testid="stLayoutWrapper"]:has(.chart-box-marker) {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid #EBE6DC !important;
    border-radius: 16px !important;
    padding: 10px 16px 4px 16px !important;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.02) !important;
    position: relative !important;
}

div[data-testid="stLayoutWrapper"]:has(.chart-box-marker) > div[data-testid="stVerticalBlock"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    gap: 2px !important;
}

/* Timeframe Pills (stButtonGroup & stPills) */
[data-testid="stMain"] div[data-testid="stButtonGroup"],
[data-testid="stMain"] [data-testid="stPills"],
[data-testid="stMain"] div[data-testid="stPills"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 10px !important;
    align-items: center !important;
    margin-bottom: 4px !important;
}

[data-testid="stMain"] div[data-testid="stButtonGroup"] button,
[data-testid="stMain"] [data-testid="stPills"] button {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #475569 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 20px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 650 !important;
    padding: 6px 18px !important;
    min-height: 38px !important;
    height: 38px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stMain"] div[data-testid="stButtonGroup"] button:hover,
[data-testid="stMain"] [data-testid="stPills"] button:hover {
    background: #F1F5F9 !important;
    color: #1E293B !important;
    border-color: #CBD5E1 !important;
}

[data-testid="stMain"] div[data-testid="stButtonGroup"] button[aria-pressed="true"],
[data-testid="stMain"] div[data-testid="stButtonGroup"] button[aria-selected="true"],
[data-testid="stMain"] div[data-testid="stButtonGroup"] button[data-selected="true"],
[data-testid="stMain"] [data-testid="stPills"] button[aria-pressed="true"],
[data-testid="stMain"] [data-testid="stPills"] button[aria-selected="true"],
[data-testid="stMain"] [data-testid="stPills"] button[data-selected="true"] {
    background-color: #003F35 !important;
    background: #003F35 !important;
    color: #FFFFFF !important;
    border-color: #003F35 !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 6px rgba(0, 63, 53, 0.3) !important;
}

[data-testid="stMain"] div[data-testid="stButtonGroup"] button[aria-pressed="true"] p,
[data-testid="stMain"] [data-testid="stPills"] button[aria-pressed="true"] p {
    color: #FFFFFF !important;
}

/* Stock Explorer action buttons */
div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) button[kind="secondary"],
div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) button[data-testid="stBaseButton-secondary"] {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #1E293B !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 24px !important;
    height: 36px !important;
    min-height: 36px !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    transition: all 0.2s ease !important;
    padding: 0 18px !important;
    white-space: nowrap !important;
}

div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) button[kind="secondary"]:hover,
div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) button[data-testid="stBaseButton-secondary"]:hover {
    background: #F8FAFC !important;
    border-color: #94A3B8 !important;
    color: #0F172A !important;
}

div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) button[kind="secondary"] p {
    color: #1E293B !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
}

div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) button[kind="primary"],
div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) button[data-testid="stBaseButton-primary"] {
    background-color: #003F35 !important;
    background: #003F35 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 24px !important;
    height: 36px !important;
    min-height: 36px !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(0, 63, 53, 0.3) !important;
    transition: all 0.2s ease !important;
    padding: 0 20px !important;
    white-space: nowrap !important;
}

div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) button[kind="primary"]:hover,
div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) button[data-testid="stBaseButton-primary"]:hover {
    background-color: #087E69 !important;
    background: #087E69 !important;
    box-shadow: 0 4px 12px rgba(8, 126, 105, 0.4) !important;
    color: #FFFFFF !important;
}

div[data-testid="stLayoutWrapper"]:has(.stock-id-marker) button[kind="primary"] p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
}

.kpi-interactive-card {
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.kpi-interactive-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.06) !important;
    border-color: #DCD7CB !important;
}

.mover-row-item {
    transition: all 0.18s ease !important;
}

.mover-row-item:hover {
    background-color: rgba(0, 143, 99, 0.06) !important;
    border-radius: 8px;
    padding-left: 8px !important;
}

/* ── TABS (REACT-ARIA & BASEWEB COMPATIBLE GREEN PILL #008F63) ────────── */
div[data-testid="stTabs"] div[role="tablist"],
.stTabs [data-baseweb="tab-list"] {
    background: #F1EEE6 !important;
    border: 1px solid #E5E0D5 !important;
    border-radius: 22px !important;
    padding: 3px !important;
    gap: 4px !important;
    width: fit-content !important;
    margin-bottom: 12px !important;
}

div[data-testid="stTab"],
div[data-testid="stTabs"] div[role="tab"],
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 18px !important;
    padding: 6px 18px !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: #52677A !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stTab"][aria-selected="true"],
div[data-testid="stTabs"] div[role="tab"][aria-selected="true"],
.stTabs [aria-selected="true"] {
    background: #008F63 !important;
    background-color: #008F63 !important;
    border-radius: 18px !important;
    border: none !important;
    border-bottom: none !important;
    outline: none !important;
    box-shadow: 0 2px 6px rgba(0, 143, 99, 0.3) !important;
}

div[data-testid="stTab"][aria-selected="true"] p,
div[data-testid="stTab"][aria-selected="true"] span,
div[data-testid="stTab"][aria-selected="true"] div,
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span {
    color: #ffffff !important;
    font-weight: 700 !important;
}

div[data-testid="stTab"][aria-selected="false"] p,
div[data-testid="stTab"][aria-selected="false"] span,
div[data-testid="stTab"][aria-selected="false"] div,
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span {
    color: #52677A !important;
    font-weight: 600 !important;
}

div[data-testid="stTabs"] div[role="tabpanel"],
div[data-testid="stTabs"] [data-baseweb="tab-panel"] {
    display: block !important;
    padding: 0 !important;
    margin: 0 !important;
    visibility: visible !important;
}

div[data-testid="stTabs"] div[role="tablist"] {
    border-bottom: none !important;
}

div[data-testid="stTabs"] .react-aria-SelectionIndicator,
div[data-testid="stTabs"] [class*="SelectionIndicator"],
.react-aria-SelectionIndicator,
[class*="SelectionIndicator"],
div[data-testid="stTabs"] div[role="tablist"] > *:not([role="tab"]):not([data-testid="stTab"]) {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    pointer-events: none !important;
}

div[data-testid="stTab"]::after,
div[data-testid="stTab"]::before,
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"],
div[data-testid="stTabs"] [data-testid="stTabHighlight"],
div[data-testid="stTabs"] hr,
div[data-testid="stTab"] hr {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
    height: 0 !important;
    border: none !important;
    border-bottom: none !important;
    background: transparent !important;
}

/* ── MAIN WORKSPACE BUTTONS (PRIMARY, DOWNLOAD & ACTIONS) ───────────── */
/* Solid Emerald Primary Action Buttons (+ Add Stock etc.) matching Reference 2 */
[data-testid="stMain"] button[kind="primary"],
[data-testid="stMain"] [data-testid="stBaseButton-primary"],
[data-testid="stMain"] .stButton > button[kind="primary"] {
    background: #003F35 !important;
    background-color: #003F35 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 11px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 750 !important;
    padding: 9px 22px !important;
    min-height: 42px !important;
    height: 42px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    box-shadow: 0 2px 6px rgba(0, 63, 53, 0.3) !important;
    transition: all 0.2s ease !important;
    width: auto !important;
}

[data-testid="stMain"] button[kind="primary"]:hover,
[data-testid="stMain"] [data-testid="stBaseButton-primary"]:hover,
[data-testid="stMain"] .stButton > button[kind="primary"]:hover {
    background: #087F68 !important;
    background-color: #087F68 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(8, 127, 104, 0.4) !important;
}

/* Solid Emerald Download Buttons matching Reference Image 4 */
[data-testid="stMain"] .stDownloadButton > button,
[data-testid="stMain"] div[data-testid="stDownloadButton"] > button {
    background: #003F35 !important;
    background-color: #003F35 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    padding: 4px 14px !important;
    min-height: 32px !important;
    height: 32px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    box-shadow: 0 1px 3px rgba(0, 63, 53, 0.25) !important;
    transition: all 0.2s ease !important;
    width: auto !important;
}

[data-testid="stMain"] .stDownloadButton > button:hover,
[data-testid="stMain"] div[data-testid="stDownloadButton"] > button:hover {
    background: #087F68 !important;
    background-color: #087F68 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(8, 127, 104, 0.35) !important;
}

/* Secondary & Action Buttons in main container */
[data-testid="stMain"] button[data-testid="stBaseButton-secondary"],
[data-testid="stMain"] .stButton > button:not([kind="primary"]),
[data-testid="stMain"] [data-testid="baseButton-secondary"],
[data-testid="stMain"] button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):not(.ss-search-submit-btn),
section.main .stButton > button:not([kind="primary"]) {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #102238 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 9px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 650 !important;
    padding: 6px 14px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
}

[data-testid="stMain"] button[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stMain"] .stButton > button:not([kind="primary"]):hover,
section.main .stButton > button:not([kind="primary"]):hover {
    background-color: #F8FAFC !important;
    background: #F8FAFC !important;
    border-color: #CBD5E1 !important;
    color: #087F68 !important;
    transform: translateY(-1px);
}

/* Main workspace Form Controls & Selectboxes */
[data-testid="stMain"] .stSelectbox div[role="group"],
[data-testid="stMain"] .stSelectbox > div > div,
[data-testid="stMain"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 9px !important;
    color: #102238 !important;
    min-height: 40px !important;
}

[data-testid="stMain"] .stSelectbox input,
[data-testid="stMain"] .stSelectbox span,
[data-testid="stMain"] div[data-baseweb="select"] * {
    color: #102238 !important;
    font-weight: 550 !important;
}

[data-testid="stMain"] div[data-baseweb="select"] svg {
    fill: #64748B !important;
}

/* Watchlist Table Action Buttons — Clean Transparent Icons */
div[data-testid="column"]:last-child .stButton > button,
div[data-testid="column"]:last-child .stButton > button:hover,
button[key*="btn_alt_"],
button[key*="btn_del_"],
div[data-testid="column"]:has(button[key*="btn_alt_"]) .stButton > button,
div[data-testid="column"]:has(button[key*="btn_del_"]) .stButton > button,
div[data-testid="column"]:has(button[key*="btn_alt_"]) .stButton > button:hover,
div[data-testid="column"]:has(button[key*="btn_del_"]) .stButton > button:hover,
button:has([data-testid="stIconMaterial"]):not([kind="primary"]) {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    min-height: 36px !important;
    height: 36px !important;
    padding: 0 4px !important;
}

div[data-testid="column"]:has(button[key*="btn_alt_"]) .stButton > button:hover,
div[data-testid="column"]:has(button[key*="btn_del_"]) .stButton > button:hover {
    background: rgba(0, 0, 0, 0.05) !important;
    transform: scale(1.15) !important;
}

/* Red trash icon matching Reference Image 2 */
button[key*="btn_del_"] [data-testid="stIconMaterial"],
div[data-testid="column"]:has(button[key*="btn_del_"]) [data-testid="stIconMaterial"] {
    color: #DC2626 !important;
    fill: #DC2626 !important;
    font-size: 21px !important;
}

/* Gray bell icon matching Reference Image 2 */
button[key*="btn_alt_"] [data-testid="stIconMaterial"],
div[data-testid="column"]:has(button[key*="btn_alt_"]) [data-testid="stIconMaterial"] {
    color: #64748B !important;
    fill: #64748B !important;
    font-size: 21px !important;
}

/* ── TOP STAT CARDS ──────────────────────────────────────────────────── */
.ss-stats-row {
    display: flex;
    gap: 16px;
    margin-bottom: 20px;
    width: 100%;
}

.ss-page-h1 {
    font-size: 38px;
    font-weight: 800;
    color: #102238;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 4px;
    font-family: 'Inter', sans-serif;
}

.ss-page-sub {
    font-size: 16px;
    color: #52677A;
    margin-bottom: 0px;
    font-weight: 500;
    line-height: 1.45;
}

.ss-footer {
    font-size: 13px;
    color: #52677A;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #EAE6DE;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.pulse-dot {
    animation: pulse-dot 2.2s infinite;
    border-radius: 50%;
    display: inline-block;
}
</style>
"""
