"""
StockSense AI - Global Market Intelligence & Risk Analytics Dashboard
Main application entry point and sidebar router
Exact match to Reference Image:
- 260px fixed width sidebar, dark emerald gradient with fluid bottom waves
- Inactive Nav: Transparent background, white outline SVGs, crisp mint text
- Active Nav: Elevated teal-green rounded pill with drop shadow
- Market selection controls neatly organized inside a collapsible panel to reduce visual clutter
"""
import streamlit as st
import datetime
import os
import textwrap

# Configured page metadata and master light theme for 1488x835 viewport
st.set_page_config(
    page_title="StockSense AI — Global Market Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

from styles import MAIN_CSS
from config import (
    APP_NAME, APP_SUBTITLE, DEFAULT_TICKER, DEFAULT_MARKET,
    DEFAULT_BENCHMARK, MARKETS, BENCHMARKS, DATA_PROVIDER_NAME
)
from components import NAV_ICONS, get_logo_b64, get_wave_b64

# Inject master design system CSS
st.html(MAIN_CSS)

# Import individual pages
from views import (
    global_overview,
    stock_explorer,
    risk_analytics,
    stock_comparison,
    company_fundamentals,
    ai_analyst,
    watchlist,
    data_quality,
    datasets,
    settings
)

# Initialize Session State & URL Routing
if "page" in st.query_params:
    st.session_state["page"] = st.query_params["page"]
elif "page" not in st.session_state:
    st.session_state["page"] = "Global Overview"

if "ticker" in st.query_params:
    st.session_state["ticker"] = st.query_params["ticker"]
elif "ticker" not in st.session_state:
    st.session_state["ticker"] = DEFAULT_TICKER

if "market" not in st.session_state:
    st.session_state["market"] = DEFAULT_MARKET

if "benchmark" not in st.session_state:
    st.session_state["benchmark"] = DEFAULT_BENCHMARK

if "compare_list" not in st.session_state:
    st.session_state["compare_list"] = ["AAPL", "MSFT", "GOOGL", "TSLA"]

if "watchlist" not in st.session_state:
    st.session_state["watchlist"] = ["AAPL", "MSFT", "GOOGL", "TSLA", "RELIANCE.NS", "TCS.NS"]

# Asset HTML tags
logo_b64 = get_logo_b64()
if logo_b64:
    _LOGO_IMG_HTML = f'<img src="data:image/png;base64,{logo_b64}" style="width:36px; height:36px; object-fit:contain; border-radius:8px;" />'
else:
    _LOGO_IMG_HTML = """
    <div style="width:36px; height:36px; border-radius:8px; background:linear-gradient(135deg, #34D399, #059669); display:flex; align-items:center; justify-content:center; box-shadow:0 3px 8px rgba(0,0,0,0.3); flex-shrink:0;">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 2L4 9L12 22L20 9L12 2Z" fill="#13332a"/><path d="M12 2L12 22L20 9L12 2Z" fill="#0d261f" opacity="0.4"/></svg>
    </div>
    """


def render_sidebar():
    with st.sidebar:
        # ── 1. LOGO BLOCK (PROMINENT HIERARCHY) ──────────────────────
        logo_html = textwrap.dedent(f"""
        <div style="padding: 8px 2px 16px; margin-bottom: 6px; position:relative; z-index:2;">
            <div style="display:flex; align-items:center; gap:14px;">
                {_LOGO_IMG_HTML}
                <div>
                    <div style="font-size:1.52rem; font-weight:800; color:#FFFFFF; font-family:'Plus Jakarta Sans',sans-serif; letter-spacing:-0.02em; line-height:1.18;">
                        StockSense AI
                    </div>
                    <div style="font-size:0.92rem; color:#A7C9BE; font-family:'Plus Jakarta Sans',sans-serif; font-weight:600; letter-spacing:0.02em; margin-top:2px;">
                        Global Market Intelligence
                    </div>
                </div>
            </div>
        </div>
        """).strip()
        st.html(logo_html)
        
        # ── 2. COMPACT NAVIGATION ITEMS (48px height, 18.5px text) ────
        nav_routes = [
            ("Global Overview", "Global Overview", ":material/home:"),
            ("Stock Explorer", "Stock Explorer", ":material/search:"),
            ("Risk Analytics", "Risk Analytics", ":material/notifications:"),
            ("Stock Comparison", "Stock Comparison", ":material/bar_chart:"),
            ("Company Fundamentals", "Company Fundamentals", ":material/corporate_fare:"),
            ("AI Market Analyst", "AI Market Analyst", ":material/smart_toy:"),
            ("Watchlist", "Watchlist", ":material/bookmark:"),
            ("Datasets", "Datasets", ":material/database:"),
            ("Data Quality", "Data Quality", ":material/verified_user:"),
            ("Settings", "Settings", ":material/settings:"),
        ]
        
        current = st.session_state.get("page", "Global Overview")
        
        for label, name, icon_name in nav_routes:
            is_active = (current == name)
            
            # Button styled via CSS with clean uniform layout
            if st.button(
                f"{label}",
                key=f"nav_{name}",
                use_container_width=True,
                icon=icon_name,
                type="primary" if is_active else "secondary"
            ):
                st.session_state["page"] = name
                st.query_params["page"] = name
                st.rerun()

        # ── 3. DIRECT SLEEK MARKET & BENCHMARK CONTROLS ──
        st.html('<div style="font-size:13.5px; text-transform:uppercase; color:#85BDB0; font-weight:800; letter-spacing:0.08em; margin-top:18px; margin-bottom:8px; font-family:\'Inter\',sans-serif;">MARKET & BENCHMARK CONTROLS</div>')
        
        st.html('<div style="font-size:15px; color:#E1F2EC; font-weight:700; margin-bottom:4px; font-family:\'Inter\',sans-serif;">Market Region</div>')
        markets = ["United States","India","United Kingdom","Germany","Japan","Australia","Canada","Brazil","China","France"]
        market = st.selectbox("Market", markets, index=markets.index(st.session_state.get("market","United States")), label_visibility="collapsed", key="market_select")
        st.session_state["market"] = market
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.html('<div style="font-size:15px; color:#E1F2EC; font-weight:700; margin-bottom:4px; font-family:\'Inter\',sans-serif;">Quick Select</div>')
            quick_tickers = {
                "United States": ["AAPL","MSFT","GOOGL","AMZN","NVDA","TSLA","META","JPM"],
                "India": ["TCS.NS","RELIANCE.NS","INFY.NS","HDFCBANK.NS"],
                "United Kingdom": ["HSBA.L","BP.L","GSK.L"],
                "Germany": ["SAP.DE","BMW.DE"],
                "Japan": ["9984.T","7203.T"],
                "Australia": ["BHP.AX","CBA.AX"],
                "Canada": ["SHOP.TO","RY.TO"],
                "Brazil": ["VALE3.SA","PETR4.SA"],
                "China": ["BABA","JD","BIDU"],
                "France": ["MC.PA","TTE.PA"],
            }.get(market, ["AAPL"])
            t_idx = quick_tickers.index(st.session_state.get("ticker")) if st.session_state.get("ticker") in quick_tickers else 0
            ticker_qs = st.selectbox("Quick", quick_tickers, index=t_idx, label_visibility="collapsed", key="quick_select")
        with col_b:
            st.html('<div style="font-size:15px; color:#E1F2EC; font-weight:700; margin-bottom:4px; font-family:\'Inter\',sans-serif;">Custom</div>')
            custom_t = st.text_input("Custom", placeholder="TSLA", label_visibility="collapsed", key="custom_ticker")
        
        active_ticker = custom_t.upper().strip() if custom_t.strip() else ticker_qs
        if active_ticker != st.session_state.get("ticker"):
            st.session_state["ticker"] = active_ticker
        
        st.html('<div style="font-size:15px; color:#E1F2EC; font-weight:700; margin-top:8px; margin-bottom:4px; font-family:\'Inter\',sans-serif;">Benchmark Reference</div>')
        benchmarks = {"SPY (S&P 500 ETF)": "SPY", "QQQ (NASDAQ 100)": "QQQ", "IWM (Russell 2000)": "IWM", "EFA (Intl Developed)": "EFA"}
        cur_bm = st.session_state.get("benchmark", "SPY")
        bm_idx = list(benchmarks.values()).index(cur_bm) if cur_bm in benchmarks.values() else 0
        bm_label = st.selectbox("Benchmark", list(benchmarks.keys()), index=bm_idx, label_visibility="collapsed", key="benchmark_select")
        st.session_state["benchmark"] = benchmarks[bm_label]
        
        # Live provider status inside panel
        import datetime as _dt
        last_sync = _dt.datetime.now().strftime("%H:%M:%S")
        st.session_state["last_sync"] = last_sync
        status_html = textwrap.dedent(f"""
        <div style="margin-top:12px; padding:10px 14px; border-radius:12px; background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.12); font-family:'Inter',sans-serif;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span class="pulse-dot" style="width:8px; height:8px; background:#16a34a; border-radius:50%; display:inline-block;"></span>
                    <span style="font-size:0.95rem; color:#FFFFFF; font-weight:750;">yfinance</span>
                </div>
                <span style="background:rgba(22,163,74,0.22); color:#34D399; font-size:0.78rem; font-weight:750; padding:2px 9px; border-radius:6px; border:1px solid rgba(52,211,153,0.4);">
                    LIVE
                </span>
            </div>
            <div style="font-size:0.74rem; color:#A7C9BE; margin-top:4px; font-weight:500;">
                Last sync: {last_sync}
            </div>
        </div>
        """).strip()
        st.html(status_html)

render_sidebar()


# Main View Router
current_page = st.session_state.get("page", "Global Overview")

if current_page == "Global Overview":
    global_overview.render()
elif current_page == "Stock Explorer":
    stock_explorer.render()
elif current_page == "Risk Analytics":
    risk_analytics.render()
elif current_page == "Stock Comparison":
    stock_comparison.render()
elif current_page == "Company Fundamentals":
    company_fundamentals.render()
elif current_page == "AI Market Analyst":
    ai_analyst.render()
elif current_page == "Watchlist":
    watchlist.render()
elif current_page == "Data Quality":
    data_quality.render()
elif current_page == "Datasets":
    datasets.render()
elif current_page == "Settings":
    settings.render()
else:
    global_overview.render()
