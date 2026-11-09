# -*- coding: utf-8 -*-
"""
Page 1: Global Overview
StockSense AI — Global Market Intelligence & Risk Analytics
Exact match to Reference 1 Image (media_1794067276908_31195af1.jpg):
- Top App Bar with real-time clock pill, notification bell, user avatar
- Global header with 3D decorative globe in upper right
- Search input bar with green submit button (52px height)
- 4 Equal KPI stat cards dynamically calculated from market coverage
- Main analytics section:
    - Left (65%): Global Market Performance interactive map with pan, zoom,
      country flags, live index movements, and activity legend
    - Right (35%): Market Movers with Top Gainers & Top Losers pills,
      live prices, dynamic return badges, and 'View more →' link
- System operational footer with zero underneath blank whitespace
"""
import streamlit as st
import pandas as pd
import re
from market_service import (
    get_market_coverage_stats,
    get_world_market_indices,
    get_market_movers
)
from visualizations import create_world_map
from components import top_app_bar, get_globe_b64, render_kpi_card, clean_html, svg_to_data_uri

def render():
    # ── 1. TOP APP BAR (DATE BADGE + NOTIFICATION BELL + USER AVATAR) ──
    st.html(top_app_bar(show_globe=False))

    # ── 2. GLOBAL HEADER + 3D DECORATIVE GLOBE LAYERED UNDER TOP-RIGHT ────
    globe_b64 = get_globe_b64()
    globe_html = ""
    if globe_b64:
        globe_html = f"""
        <div style="position:absolute; top:-25px; right:-15px; width:310px; height:310px; pointer-events:none; z-index:1; overflow:visible;">
            <div style="position:absolute; width:330px; height:330px; top:-10px; right:-10px; border-radius:50%; background:radial-gradient(circle, rgba(16,185,129,0.32) 0%, rgba(16,185,129,0.10) 50%, rgba(255,255,255,0) 75%); filter:blur(16px); pointer-events:none;"></div>
            <img src="data:image/png;base64,{globe_b64}" style="width:100%; height:auto; display:block; position:relative; z-index:2; filter:drop-shadow(0 6px 20px rgba(0,63,53,0.12));" />
        </div>
        """

    header_raw = f"""
    <div style="position:relative; margin-bottom:6px; font-family:'Inter',sans-serif; overflow:visible;">
        {globe_html}
        <div style="max-width:68%; position:relative; z-index:2;">
            <div class="ss-page-h1" style="font-size:38px; font-weight:800; color:#102238; letter-spacing:-0.03em; margin-bottom:3px; line-height:1.15;">StockSense AI</div>
            <div style="color:#087E69; font-size:19.5px; font-weight:700; margin-bottom:4px; letter-spacing:-0.01em;">Global Market Intelligence & Risk Analytics</div>
            <div class="ss-page-sub" style="font-size:15px; color:#52677A; margin-bottom:0; font-weight:500;">Explore global markets, analyze performance, compare stocks and get AI-powered insights.</div>
        </div>
    </div>
    """
    st.html(clean_html(header_raw))

    # ── 3. SEARCH BAR PILL (EXACT MATCH TO REFERENCE IMAGE 2, ZERO CONTINUATION, FULLY RESPONSIVE) ──
    search_html = f"""
    <div class="ss-global-search-container" style="max-width:760px; width:68%; margin-bottom:14px; position:relative; z-index:5; font-family:'Inter',sans-serif;">
        <form method="GET" action="/" style="margin:0; padding:0; display:block;">
            <input type="hidden" name="page" value="Stock Explorer" />
            <div class="ss-search-pill" style="display:flex; align-items:center; background:#FFFFFF; border:1.5px solid #D5D0C5; border-radius:9999px; height:52px; padding:0 8px 0 20px; box-shadow:0 2px 10px rgba(0,0,0,0.025); transition:all 0.2s ease;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#102238" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0; margin-right:12px;">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <input 
                    name="ticker"
                    type="text" 
                    placeholder="Search for a company or ticker (e.g., AAPL, RELIANCE, TSLA, TCS ...)" 
                    autocomplete="off"
                    style="flex:1; border:none; outline:none; background:transparent; font-family:'Inter',sans-serif; font-size:15px; color:#102238; font-weight:500; min-width:0;"
                />
                <button 
                    type="submit" 
                    class="ss-search-submit-btn"
                    title="Search"
                    style="width:38px; height:38px; min-width:38px; min-height:38px; border-radius:50%; background-color:#003F35; background:#003F35; border:none; color:#FFFFFF; display:flex; align-items:center; justify-content:center; cursor:pointer; flex-shrink:0; padding:0; margin:0; box-shadow:0 2px 8px rgba(0,63,53,0.35); font-size:18px; line-height:1; font-weight:700;"
                >&rarr;</button>
            </div>
        </form>
    </div>
    """
    st.html(clean_html(search_html))

    # ── 4. 4 EQUAL KPI STAT CARDS IN ONE ROW (130px HEIGHT) ─────
    coverage = get_market_coverage_stats()
    card1_icon = """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#008F63" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>"""
    card2_icon = """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#9333EA" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="9" y2="2"></line><line x1="15" y1="6" x2="17" y2="6"></line><line x1="15" y1="10" x2="17" y2="10"></line><line x1="15" y1="14" x2="17" y2="14"></line><line x1="15" y1="18" x2="17" y2="18"></line></svg>"""
    card3_icon = """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>"""

    card1 = render_kpi_card("Global Markets", str(coverage["global_markets"]), "+1 today", card1_icon, "#E6F8F0", "#008F63", "radial-gradient(ellipse at bottom right, rgba(0,143,99,0.2) 0%, rgba(255,255,255,0) 70%)")
    card2 = render_kpi_card("Tracked Companies", coverage["tracked_companies"], "Across 50+ countries", card2_icon, "#F4EEFC", "#9333EA", "radial-gradient(ellipse at bottom right, rgba(147,51,234,0.18) 0%, rgba(255,255,255,0) 70%)")
    card3 = render_kpi_card("Major Indexes", str(coverage["major_indices"]), "S&P 500, NIFTY, FTSE ...", card3_icon, "#E6F8F2", "#059669", "radial-gradient(ellipse at bottom right, rgba(5,150,105,0.18) 0%, rgba(255,255,255,0) 70%)")
    card4 = render_kpi_card("Market Data", coverage["provider_status"], f"(via {coverage['provider_name']})", "", "#E8F8EE", "#16A34A", "radial-gradient(ellipse at bottom right, rgba(22,163,74,0.2) 0%, rgba(255,255,255,0) 70%)", is_live_dot=True)

    kpi_raw = f"""<div class="ss-stats-row" style="display:flex; gap:16px; width:100%; font-family:'Inter',sans-serif; margin-bottom:12px;">{card1}{card2}{card3}{card4}</div>"""
    st.html(clean_html(kpi_raw))

    # ── 5. MAIN ANALYTICS SECTION: MAP (65%) & MARKET MOVERS (35%) ─────
    indices_data = get_world_market_indices()
    top_gainers, top_losers = get_market_movers()

    map_col, movers_col = st.columns([65, 35], gap="large")

    globe_icon_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#008F63" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
    movers_icon_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#008F63" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>'

    with map_col:
        # Card Anchor and Header
        map_header_html = f"""
        <div class="analytics-map-card" style="display:flex; align-items:center; gap:10px; margin-bottom:12px; font-family:'Inter',sans-serif;">
            {svg_to_data_uri(globe_icon_svg, 24, 24)}
            <span style="font-size:24px; font-weight:800; color:#102238; letter-spacing:-0.02em;">Global Market Performance</span>
        </div>
        """
        st.html(clean_html(map_header_html))

        # Render interactive world map with pan/zoom and live tooltip updates
        map_fig = create_world_map(indices_data, selected_country=st.session_state.get("market", "United States"))
        st.plotly_chart(map_fig, use_container_width=True, config={"displayModeBar": False, "scrollZoom": True})

        # Activity Legend inside bottom of Map Card
        legend_raw = """
        <div style="display: flex; justify-content: center; align-items: center; gap: 24px; font-size: 13px; color: #52677A; margin-top: 6px; padding-top: 4px; font-family: 'Inter', sans-serif; font-weight: 600;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #16A34A;"></span>
                <span>High Activity</span>
            </div>
            <span style="color: #D5D0C5;">|</span>
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #F59E0B;"></span>
                <span>Low Activity</span>
            </div>
            <span style="color: #D5D0C5;">|</span>
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #3B82F6;"></span>
                <span>No Activity</span>
            </div>
        </div>
        """
        st.html(clean_html(legend_raw))

    with movers_col:
        # Card Anchor and Header
        movers_header_html = f"""
        <div class="analytics-movers-card" style="display:flex; align-items:center; gap:10px; margin-bottom:12px; font-family:'Inter',sans-serif;">
            {svg_to_data_uri(movers_icon_svg, 24, 24)}
            <span style="font-size:24px; font-weight:800; color:#102238; letter-spacing:-0.02em;">Market Movers</span>
        </div>
        """
        st.html(clean_html(movers_header_html))

        # Movers Navigation Pills (Top Gainers vs Top Losers) matching Reference Image 1
        if "movers_tab" not in st.session_state:
            st.session_state["movers_tab"] = "Top Gainers"

        current_movers_tab = st.session_state["movers_tab"]

        btn_c1, btn_c2 = st.columns(2, gap="small")
        with btn_c1:
            if st.button("Top Gainers", key="btn_mv_gainers", type="primary" if current_movers_tab == "Top Gainers" else "secondary", use_container_width=True):
                st.session_state["movers_tab"] = "Top Gainers"
                st.rerun()
        with btn_c2:
            if st.button("Top Losers", key="btn_mv_losers", type="primary" if current_movers_tab == "Top Losers" else "secondary", use_container_width=True):
                st.session_state["movers_tab"] = "Top Losers"
                st.rerun()

        # Render rows
        active_rows = top_gainers if current_movers_tab == "Top Gainers" else top_losers
        item_rows = []
        for r in active_rows:
            p_str = f"{r['price']:,.2f}" if r.get('price') else "N/A"
            chg = r.get("pct_change", 0.0)
            is_pos = chg >= 0
            badge_bg = "#E8F8EE" if is_pos else "#FEE8E8"
            color = "#16A34A" if is_pos else "#E5484D"
            sign = "+" if is_pos else ""
            clean_ticker = r['ticker']
            item_rows.append(f"""
            <div class="mover-row-item" style="display:flex; justify-content:space-between; align-items:center; height:44px; border-bottom:1px solid #F0ECDF; padding:0 8px; font-family:'Inter', sans-serif; transition:all 0.18s ease;">
                <div style="font-weight:700; color:#102238; font-size:15.5px; width:95px;">{clean_ticker}</div>
                <div style="color:#102238; font-weight:600; text-align:right; font-size:15px; flex:1; padding-right:16px;">{p_str}</div>
                <div style="text-align:right;">
                    <span style="background:{badge_bg}; color:{color}; padding:4px 11px; border-radius:7px; font-weight:700; font-size:13.5px; display:inline-block; min-width:70px; text-align:center;">{sign}{chg:.2f}%</span>
                </div>
            </div>
            """)

        box_raw = f"""<div style="display:flex; flex-direction:column; width:100%; margin-top:6px; font-family:'Inter', sans-serif;">{"".join(item_rows)}</div>"""
        st.html(clean_html(box_raw))

        st.html("<div style='height: 12px;'></div>")
        if st.button("View more →", key="view_more_movers"):
            if active_rows:
                st.session_state["ticker"] = active_rows[0].get("full_ticker") or active_rows[0]["ticker"]
                st.session_state["page"] = "Stock Explorer"
                st.rerun()

    # ── 6. FOOTER ────────────────────────────────────────────────
    footer_raw = """
    <div class="ss-footer">
        <div>StockSense AI v3.0.0 · Dual feed via Twelve Data & yfinance · Historical analysis only · Not financial advice</div>
        <div style="display: flex; align-items: center; gap: 7px; color: #16A34A; font-weight: 700;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #16A34A; display: inline-block;"></span> System Operational
        </div>
    </div>
    """
    st.html(clean_html(footer_raw))
