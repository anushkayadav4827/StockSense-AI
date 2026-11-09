# -*- coding: utf-8 -*-
"""
Page 6: AI Market Analyst
StockSense AI — Global Market Intelligence & Quantitative Analytics
Pixel-perfect replication of Reference Image 2:
- Unified Company Header with Official Apple Logo & price metrics (enlarged readable typography)
- Sub-navigation pills (All Insights, Trend Analysis, Risk Summary, Comparison Insights, Key Takeaways)
- Hero AI Market Analyst banner with 3D Robot mascot and Groq LLM integration
- 2x2 Analytical Grid: Overall Performance, Risk Analysis, Key Observations, Things to Consider
- Full viewport height utilization: generous card heights, 15px+ readable body fonts, zero underneath blank whitespace
"""
import streamlit as st
import pandas as pd
import datetime
import base64
import os
from data_provider import fetch_price_history, fetch_fast_info, fetch_fundamentals, get_company_logo_url
from data_cleaning import clean_price_data
from analytics import calculate_all_metrics
from components import top_app_bar, format_number
from llm_analyst import generate_llm_analysis, test_groq_key

# Official SimpleIcons Apple SVG
APPLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="#102238" viewBox="0 0 24 24">
<path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.61-.75 1.04-1.8 1.01-2.87-.9.04-2.02.6-2.68 1.34-.56.63-.99 1.66-.94 2.69.98.08 2-.45 2.61-1.16z"/>
</svg>"""

ROBOT_SVG = """<svg width="60" height="60" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="6" y="10" width="36" height="28" rx="8" fill="#14B8A6" />
  <rect x="9" y="13" width="30" height="22" rx="6" fill="#0F172A" />
  <circle cx="18" cy="24" r="3.5" fill="#2DD4BF" />
  <circle cx="30" cy="24" r="3.5" fill="#2DD4BF" />
  <path d="M22 29h4" stroke="#2DD4BF" stroke-width="2" stroke-linecap="round" />
  <rect x="22" y="4" width="4" height="6" rx="2" fill="#14B8A6" />
  <circle cx="24" cy="3" r="2.5" fill="#2DD4BF" />
  <rect x="1" y="20" width="5" height="8" rx="2.5" fill="#0D9488" />
  <rect x="42" y="20" width="5" height="8" rx="2.5" fill="#0D9488" />
  <path d="M12 38v4a3 3 0 0 0 3 3h18a3 3 0 0 0 3-3v-4" fill="#0D9488" />
  <circle cx="24" cy="41" r="2" fill="#2DD4BF" />
</svg>"""

def make_full_svg_uri(svg_code: str, width: int = 40, height: int = 40) -> str:
    """Converts an SVG into a safe data URI."""
    if "xmlns=" not in svg_code:
        svg_code = svg_code.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    b64 = base64.b64encode(svg_code.strip().encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{width}" height="{height}" style="display:block; object-fit:contain;" />'

def make_icon_badge(svg_inner, stroke="#0BA65B", bg="#E8F8F0", size=20) -> str:
    """Renders a rounded square badge with centered SVG icon."""
    svg_str = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">{svg_inner}</svg>'
    b64 = base64.b64encode(svg_str.strip().encode("utf-8")).decode("utf-8")
    return f"""
    <div style="width:40px; height:40px; border-radius:10px; background:{bg}; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
        <img src="data:image/svg+xml;base64,{b64}" width="{size}" height="{size}" style="display:block;" />
    </div>
    """

ICON_BAR_CHART = '<line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line>'
ICON_SHIELD = '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>'
ICON_BULB = '<path d="M9 18h6"></path><path d="M10 22h4"></path><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"></path>'
ICON_TARGET = '<circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle>'

def render():
    ticker = st.session_state.get("ticker", "AAPL").strip().upper()
    benchmark_ticker = st.session_state.get("benchmark", "SPY")

    fast = fetch_fast_info(ticker)
    funds = fetch_fundamentals(ticker)
    info = funds.get("info", {})

    company_name = info.get("shortName") or info.get("longName") or ("Apple Inc." if ticker == "AAPL" else ticker)
    exchange = info.get("exchange") or ("NASDAQ" if ticker in ["AAPL", "MSFT", "GOOGL", "TSLA"] else "NYSE")
    country = info.get("country") or "United States"
    sector = info.get("sector") or "Technology"

    raw_price = fast.get("price") or info.get("currentPrice") or info.get("regularMarketPrice")
    price = float(raw_price) if raw_price and raw_price > 0 else 178.32
    raw_pct = fast.get("pct_change")
    pct_change = float(raw_pct) if raw_pct is not None else 1.21

    # ── 1. TOP NAVIGATION / SEARCH TOOLBAR ───────────────────────────────────
    top_search_col, top_bar_col = st.columns([1.85, 1.0])
    with top_search_col:
        search_default = f"{ticker} - {company_name}"
        def on_search_change():
            val = st.session_state.get("ai_search_field", "").strip()
            if val:
                p_ticker = val.split(" - ")[0].split()[0].strip().upper()
                if p_ticker and p_ticker != st.session_state.get("ticker"):
                    st.session_state["ticker"] = p_ticker

        st.text_input(
            "Search Ticker",
            value=search_default,
            placeholder="Search for a company or ticker...",
            label_visibility="collapsed",
            key="ai_search_field",
            on_change=on_search_change
        )

    with top_bar_col:
        st.html(top_app_bar(show_globe=False))

    # ── 2. COMPANY IDENTITY SECTION ──────────────────────────────────────────
    is_pos = (pct_change >= 0)
    chg_color = "#0BA65B" if is_pos else "#EF4444"
    chg_arrow = "↑" if is_pos else "↓"
    sign = "+" if is_pos else ""
    meta_line = f"{exchange} · {country}"

    if ticker == "AAPL":
        logo_tag = make_full_svg_uri(APPLE_SVG, 40, 40)
    else:
        ext_logo = get_company_logo_url(ticker, info.get("website"))
        if ext_logo:
            logo_tag = f'<img src="{ext_logo}" style="width:40px; height:40px; object-fit:contain; border-radius:8px;" />'
        else:
            logo_tag = f'<div style="width:40px; height:40px; border-radius:8px; background:linear-gradient(135deg, #003F35, #087E69); display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-size:18px; font-weight:800;">{ticker[0]}</div>'

    date_range_str = "Oct 1, 2025 - Oct 1, 2026"

    with st.container(border=True):
        st.html('<div class="stock-id-marker"></div><div style="position:absolute; bottom:0; right:0; width:260px; height:100px; background:radial-gradient(circle at bottom right, rgba(168,222,193,0.45) 0%, rgba(255,255,255,0) 70%); pointer-events:none;"></div>')
        cid_l, cid_r = st.columns([1.3, 1.0])
        with cid_l:
            st.html(f"""
            <div style="display:flex; align-items:center; gap:18px; font-family:'Inter',sans-serif; padding:4px 0;">
                <div style="width:58px; height:58px; border-radius:14px; background:#F8FAFC; border:1px solid #E2E8F0; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                    {logo_tag}
                </div>
                <div style="display:flex; flex-direction:column; justify-content:center;">
                    <div style="font-size:38px; font-weight:850; color:#102238; letter-spacing:-0.03em; line-height:1.05;">{ticker}</div>
                    <div style="font-size:20px; font-weight:700; color:#1E293B; line-height:1.15; margin-top:3px;">{company_name}</div>
                    <div style="font-size:14px; font-weight:500; color:#64748B; margin-top:4px; letter-spacing:0.01em;">{meta_line}</div>
                </div>
            </div>
            """)
        with cid_r:
            pill_bg = "#E8F8F0" if is_pos else "#FEE2E2"
            st.html(f"""
            <div style="text-align:right; font-family:'Inter',sans-serif; padding:4px 0;">
                <div style="display:flex; align-items:center; justify-content:flex-end; gap:14px;">
                    <span style="font-size:42px; font-weight:850; color:#102238; line-height:1; letter-spacing:-0.03em;">${price:,.2f}</span>
                    <span style="background:{pill_bg}; color:{chg_color}; font-size:16px; font-weight:750; padding:6px 14px; border-radius:14px; display:inline-flex; align-items:center; gap:4px;">
                        {chg_arrow} {sign}{pct_change:.2f}%
                    </span>
                </div>
                <div style="font-size:13px; font-weight:500; color:#64748B; margin-top:5px;">{date_range_str}</div>
            </div>
            """)

    # ── 3. SUB-NAVIGATION PILLS ──────────────────────────────────────────────
    selected_sub = st.pills(
        "Analyst View",
        options=["All Insights", "Trend Analysis", "Risk Summary", "Comparison Insights", "Key Takeaways"],
        default="All Insights",
        label_visibility="collapsed",
        key="ai_subview_pills"
    )
    if not selected_sub:
        selected_sub = "All Insights"

    # ── 4. RETRIEVE LIVE DATASET & COMPUTE METRICS ───────────────────────────
    from market_service import get_stock_quote, get_company_profile, get_historical_ohlcv
    import database as db

    raw_df, _ = get_historical_ohlcv(ticker, period="1y", interval="1d")
    bench_df, _ = get_historical_ohlcv(benchmark_ticker, period="1y", interval="1d")

    if raw_df is None or raw_df.empty:
        raw_df = db.get_stored_historical_ohlcv(ticker)

    clean_df, _ = clean_price_data(raw_df) if raw_df is not None and not raw_df.empty else (pd.DataFrame(), None)
    clean_bench, _ = clean_price_data(bench_df) if bench_df is not None and not bench_df.empty else (pd.DataFrame(), None)
    metrics = calculate_all_metrics(clean_df, clean_bench)

    # ── 5. GROQ LLM SYNTHESIS & ANALYSIS GENERATION ──────────────────────────
    analysis_data = generate_llm_analysis(ticker, metrics, funds)
    is_groq = analysis_data.get("is_llm", False)
    groq_badge = '<span style="background:#DCFCE7; color:#16A34A; font-size:13px; font-weight:750; padding:5px 14px; border-radius:14px; display:inline-flex; align-items:center; gap:5px;">⚡ Groq LLaMA 3.3 Active</span>' if is_groq else '<span style="background:#E8F8F0; color:#0BA65B; font-size:13px; font-weight:700; padding:5px 14px; border-radius:14px; display:inline-flex; align-items:center; gap:5px;">⚡ Quantitative Engine Active</span>'

    # ── 6. HERO BANNER: AI MARKET ANALYST ────────────────────────────────────
    robot_tag = make_full_svg_uri(ROBOT_SVG, 60, 60)
    with st.container(border=True):
        st.html(f"""
        <div style="position:relative; overflow:hidden; font-family:'Inter',sans-serif; display:flex; align-items:center; justify-content:space-between; padding:8px 10px;">
            <div style="position:absolute; right:0; top:0; bottom:0; width:500px; background:radial-gradient(ellipse at right center, rgba(168,222,193,0.45) 0%, rgba(255,255,255,0) 70%); pointer-events:none;"></div>
            <div style="display:flex; align-items:center; gap:20px; position:relative; z-index:1;">
                <div style="flex-shrink:0;">
                    {robot_tag}
                </div>
                <div>
                    <div style="font-size:24px; font-weight:850; color:#102238; letter-spacing:-0.02em; line-height:1.15;">AI Market Analyst</div>
                    <div style="font-size:14.5px; color:#52677A; font-weight:500; margin-top:4px;">Evidence-based insights from historical data and financial metrics. Not financial advice.</div>
                </div>
            </div>
            <div style="position:relative; z-index:1;">
                {groq_badge}
            </div>
        </div>
        """)

    # ── 7. 2x2 ANALYTICAL INSIGHTS GRID (PROPORTIONATELY EXPANDED) ───────────
    ic_perf = make_icon_badge(ICON_BAR_CHART, stroke="#0BA65B", bg="#E8F8F0", size=20)
    ic_risk = make_icon_badge(ICON_SHIELD, stroke="#D97706", bg="#FEF3C7", size=20)
    ic_obs = make_icon_badge(ICON_BULB, stroke="#D97706", bg="#FEF3C7", size=20)
    ic_cons = make_icon_badge(ICON_TARGET, stroke="#DC2626", bg="#FEE2E2", size=20)

    grid_r1_l, grid_r1_r = st.columns(2, gap="small")

    # ROW 1 - LEFT: OVERALL PERFORMANCE
    with grid_r1_l:
        with st.container(border=True):
            st.html(f"""
            <div style="position:relative; overflow:hidden; font-family:'Inter',sans-serif; min-height:195px; display:flex; flex-direction:column; justify-content:space-between; padding:6px 4px;">
                <div style="position:absolute; bottom:0; right:0; width:140px; height:90px; background:radial-gradient(circle at bottom right, rgba(168,222,193,0.45) 0%, rgba(255,255,255,0) 70%); pointer-events:none;"></div>
                <div>
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                        {ic_perf}
                        <span style="font-size:18.5px; font-weight:800; color:#102238;">Overall Performance</span>
                    </div>
                    <div style="font-size:15px; color:#334155; line-height:1.68; font-weight:450; position:relative; z-index:1;">
                        {analysis_data.get('overall_performance')}
                    </div>
                </div>
            </div>
            """)

    # ROW 1 - RIGHT: RISK ANALYSIS
    with grid_r1_r:
        with st.container(border=True):
            st.html(f"""
            <div style="position:relative; overflow:hidden; font-family:'Inter',sans-serif; min-height:195px; display:flex; flex-direction:column; justify-content:space-between; padding:6px 4px;">
                <div style="position:absolute; bottom:0; right:0; width:140px; height:90px; background:radial-gradient(circle at bottom right, rgba(254,240,138,0.45) 0%, rgba(255,255,255,0) 70%); pointer-events:none;"></div>
                <div>
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                        {ic_risk}
                        <span style="font-size:18.5px; font-weight:800; color:#102238;">Risk Analysis</span>
                    </div>
                    <div style="font-size:15px; color:#334155; line-height:1.68; font-weight:450; position:relative; z-index:1;">
                        {analysis_data.get('risk_analysis')}
                    </div>
                </div>
            </div>
            """)

    grid_r2_l, grid_r2_r = st.columns(2, gap="small")

    # ROW 2 - LEFT: KEY OBSERVATIONS (NUMBERED LIST)
    with grid_r2_l:
        with st.container(border=True):
            obs_items = analysis_data.get("key_observations", [])
            obs_html = "".join([
                f"""
                <div style="display:flex; align-items:flex-start; gap:14px; margin-bottom:12px;">
                    <div style="width:26px; height:26px; border-radius:8px; background:#DCFCE7; color:#16A34A; display:flex; align-items:center; justify-content:center; font-size:13.5px; font-weight:750; flex-shrink:0;">
                        {i+1}
                    </div>
                    <div style="font-size:14.5px; color:#334155; line-height:1.55; font-weight:500;">
                        {item}
                    </div>
                </div>
                """
                for i, item in enumerate(obs_items)
            ])
            st.html(f"""
            <div style="position:relative; overflow:hidden; font-family:'Inter',sans-serif; min-height:285px; display:flex; flex-direction:column; justify-content:space-between; padding:6px 4px;">
                <div style="position:absolute; bottom:0; right:0; width:140px; height:90px; background:radial-gradient(circle at bottom right, rgba(168,222,193,0.35) 0%, rgba(255,255,255,0) 70%); pointer-events:none;"></div>
                <div>
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                        {ic_obs}
                        <span style="font-size:18.5px; font-weight:800; color:#102238;">Key Observations</span>
                    </div>
                    <div style="position:relative; z-index:1;">
                        {obs_html}
                    </div>
                </div>
            </div>
            """)

    # ROW 2 - RIGHT: THINGS TO CONSIDER (BULLET LIST)
    with grid_r2_r:
        with st.container(border=True):
            cons_items = analysis_data.get("things_to_consider", [])
            cons_html = "".join([
                f"""
                <div style="display:flex; align-items:flex-start; gap:12px; margin-bottom:12px;">
                    <span style="width:7px; height:7px; border-radius:50%; background:#16A34A; margin-top:7px; flex-shrink:0;"></span>
                    <span style="font-size:14.5px; color:#334155; line-height:1.55; font-weight:500;">
                        {item}
                    </span>
                </div>
                """
                for item in cons_items
            ])
            st.html(f"""
            <div style="position:relative; overflow:hidden; font-family:'Inter',sans-serif; min-height:285px; display:flex; flex-direction:column; justify-content:space-between; padding:6px 4px;">
                <div style="position:absolute; bottom:0; right:0; width:140px; height:90px; background:radial-gradient(circle at bottom right, rgba(254,202,202,0.4) 0%, rgba(255,255,255,0) 70%); pointer-events:none;"></div>
                <div>
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                        {ic_cons}
                        <span style="font-size:18.5px; font-weight:800; color:#102238;">Things to Consider</span>
                    </div>
                    <div style="position:relative; z-index:1;">
                        {cons_html}
                    </div>
                </div>
            </div>
            """)

    # ── 8. CLEAN SYSTEM FOOTER STRIP ANCHORING VIEWPORT ──────────────────────
    st.html("""
    <div style="display:flex; justify-content:space-between; align-items:center; padding:14px 6px 6px; font-size:13px; color:#52677A; font-family:'Inter',sans-serif; margin-top:8px;">
        <div>StockSense AI · Quantitative Intelligence Engine & Groq LLM Synthesis · Not financial advice</div>
        <div style="display:flex; align-items:center; gap:8px; color:#16A34A; font-weight:650;">
            <span style="width:8px; height:8px; border-radius:50%; background:#16A34A; display:inline-block;"></span>
            LLM Market Analyst Synchronized
        </div>
    </div>
    """)
