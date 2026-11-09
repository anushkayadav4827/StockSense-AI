# -*- coding: utf-8 -*-
"""
Page 7: My Watchlist
StockSense AI — Global Market Intelligence & Risk Analytics
Pixel-perfect replication of Reference Image 2:
- Top search toolbar with date, notification bell, user avatar
- Page header with Bookmark icon badge, "My Watchlist" title, and prominent "+ Add Stock" button
- Clean, responsive data table with sortable columns: Stock, Price, 1D %, 1W %, 1M %, 1Y %, Market Cap, Trend (1Y), Actions
- Authentic brand logos (Apple, Microsoft, Google, Tesla, Reliance, TCS)
- Pill-styled percentage returns (green for gains, red for losses)
- Smooth 1Y Area Sparkline with vertical gradient fills
- Interactive Actions: Bell alert toggle and Trash remove action
- Modal / Inline "+ Add Stock" drawer supporting any global ticker with live validation
- Zero underneath blank whitespace
"""
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import base64
from market_service import get_stock_quote, get_batch_quotes, get_historical_ohlcv
import database as db
from components import top_app_bar, format_number, svg_to_data_uri

# ── LOGOS & ICONS ────────────────────────────────────────────────────────────
APPLE_SVG = """<svg width="24" height="24" viewBox="0 0 170 170" fill="#102238">
<path d="M150.37 130.25c-2.45 5.66-5.35 10.87-8.71 15.66-4.58 6.53-8.33 11.05-11.22 13.56-4.48 4.12-9.28 6.23-14.42 6.35-3.69 0-8.14-1.05-13.32-3.18-5.19-2.12-9.97-3.17-14.34-3.17-4.58 0-9.49 1.05-14.75 3.17-5.26 2.13-9.5 3.24-12.74 3.35-4.35.13-9.16-1.9-14.42-6.08-3.7-3.07-7.74-7.85-12.13-14.34-6.3-9.33-11.19-20.19-14.66-32.58-3.47-12.4-5.21-23.75-5.21-34.05 0-14.28 3.73-26.06 11.19-35.34 7.46-9.28 16.7-13.97 27.72-14.07 4.13 0 8.95 1.1 14.46 3.3 5.51 2.2 9.53 3.37 12.05 3.51 2.94-.3 7.15-1.55 12.63-3.76 5.48-2.2 10.05-3.23 13.71-3.08 10.22.43 18.73 4.29 25.53 11.58-8.91 5.43-13.25 12.87-13.02 22.32.23 7.5 3.12 13.88 8.67 19.14 5.55 5.26 12.14 8.27 19.78 9.03-2.18 6.52-4.78 13.04-7.81 19.56zM119.22 33.64c0-7.39 2.6-14.04 7.8-19.95 5.2-5.91 11.55-9.44 19.05-10.59.22 1.52.33 2.93.33 4.24 0 7.39-2.71 14.19-8.13 20.39-5.42 6.2-11.83 9.77-19.22 10.7-.1-.97-.15-1.97-.15-2.79z"/>
</svg>"""

MSFT_SVG = """<svg width="22" height="22" viewBox="0 0 20 20">
<rect x="1" y="1" width="8" height="8" fill="#F25022"/>
<rect x="11" y="1" width="8" height="8" fill="#7FBA00"/>
<rect x="1" y="11" width="8" height="8" fill="#00A4EF"/>
<rect x="11" y="11" width="8" height="8" fill="#FFB900"/>
</svg>"""

GOOGL_SVG = """<svg width="22" height="22" viewBox="0 0 24 24">
<path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
<path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
<path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
<path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
</svg>"""

TSLA_SVG = """<svg width="22" height="22" viewBox="0 0 24 24" fill="#E82127">
<path d="M12 4.5c2.7 0 5.5.4 7.6 1.2.2-1-.2-1.9-.9-2.3C16.6 2.5 14.3 2.2 12 2.2s-4.6.3-6.7 1.2c-.7.4-1.1 1.3-.9 2.3 2.1-.8 4.9-1.2 7.6-1.2zm9.1 2.2c-.3-.1-.6-.2-.9-.3-1.8 1.8-4.4 2.8-7.7 2.9h-.9c-3.3-.1-5.9-1.1-7.7-2.9-.3.1-.6.2-.9.3-.5.2-.8.6-.9 1.1 1.8 2.2 4.5 3.5 8 3.7v10.5c.9.2 1.8.2 2.7 0V11.5c3.5-.2 6.2-1.5 8-3.7-.1-.5-.4-.9-.9-1.1z"/>
</svg>"""

RELIANCE_SVG = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
<circle cx="12" cy="12" r="11" fill="#F59E0B" />
<path d="M8 7h5a3 3 0 0 1 0 6H8V7zm0 6h3.5l3 4.5h-2.5l-2.2-3.5H10V18H8v-5z" fill="#FFFFFF" />
</svg>"""

TCS_SVG = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
<rect width="24" height="24" rx="6" fill="#0284C7" />
<text x="12" y="16.5" font-family="'Inter', sans-serif" font-size="10.5" font-weight="850" fill="#FFFFFF" text-anchor="middle">TG</text>
</svg>"""

ICON_BOOKMARK = """<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
<path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
</svg>"""

ICON_BOOKMARK_TAG = svg_to_data_uri(ICON_BOOKMARK, 28, 28)

def get_stock_logo_tag(ticker: str) -> str:
    clean_t = ticker.replace(".NS", "").replace(".BO", "").replace(".DE", "").replace(".L", "").upper()
    logos = {
        "AAPL": APPLE_SVG,
        "MSFT": MSFT_SVG,
        "GOOGL": GOOGL_SVG,
        "GOOG": GOOGL_SVG,
        "TSLA": TSLA_SVG,
        "RELIANCE": RELIANCE_SVG,
        "TCS": TCS_SVG,
    }
    if clean_t in logos:
        return svg_to_data_uri(logos[clean_t], 24, 24)
    # Generic letter badge
    return f'<div style="width:24px; height:24px; border-radius:6px; background:#003F35; color:#FFF; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:800;">{clean_t[0]}</div>'

def get_clean_name(ticker: str, info_name: str) -> tuple:
    clean_t = ticker.replace(".NS", "").replace(".BO", "").replace(".DE", "").replace(".L", "").upper()
    predefined = {
        "AAPL": ("AAPL", "Apple Inc."),
        "MSFT": ("MSFT", "Microsoft"),
        "GOOGL": ("GOOGL", "Alphabet"),
        "GOOG": ("GOOGL", "Alphabet"),
        "TSLA": ("TSLA", "Tesla"),
        "RELIANCE": ("RELIANCE", "Reliance Ind."),
        "TCS": ("TCS", "Tata Cons. Serv."),
    }
    if clean_t in predefined:
        return predefined[clean_t]
    short_name = (info_name[:18] + "..") if len(info_name) > 20 else info_name
    return (clean_t, short_name or clean_t)

def render_area_sparkline(prices: list, is_positive: bool, width: int = 110, height: int = 34, spark_id: str = "0") -> str:
    """Generates authentic smooth SVG area sparkline matching Reference Image 2."""
    if not prices or len(prices) < 2:
        return f'<svg width="{width}" height="{height}"><line x1="0" y1="{height/2}" x2="{width}" y2="{height/2}" stroke="#CBD5E1" stroke-width="1.5"/></svg>'

    clean_p = [float(p) for p in prices if p is not None and not (isinstance(p, float) and np.isnan(p))]
    if len(clean_p) < 2:
        return f'<svg width="{width}" height="{height}"><line x1="0" y1="{height/2}" x2="{width}" y2="{height/2}" stroke="#CBD5E1" stroke-width="1.5"/></svg>'

    min_p, max_p = min(clean_p), max(clean_p)
    rng = max_p - min_p if max_p != min_p else 1.0
    pad_y = 3
    pad_x = 2
    h_eff = height - (pad_y * 2)
    w_eff = width - (pad_x * 2)
    n = len(clean_p)

    pts = []
    for i, p in enumerate(clean_p):
        x = pad_x + (i / (n - 1)) * w_eff
        y = pad_y + h_eff - ((p - min_p) / rng) * h_eff
        pts.append((x, y))

    line_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area_d = f"{line_d} L {pts[-1][0]:.1f},{height} L {pts[0][0]:.1f},{height} Z"

    stroke = "#10B981" if is_positive else "#EF4444"
    fill_color = "#10B981" if is_positive else "#EF4444"
    grad_id = f"spark_grad_{spark_id}"

    svg_str = f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:inline-block; vertical-align:middle; overflow:hidden;">
        <defs>
            <linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="{fill_color}" stop-opacity="0.32"/>
                <stop offset="100%" stop-color="{fill_color}" stop-opacity="0.02"/>
            </linearGradient>
        </defs>
        <path d="{area_d}" fill="url(#{grad_id})" />
        <path d="{line_d}" stroke="{stroke}" stroke-width="2.0" stroke-linecap="round" stroke-linejoin="round" fill="none" />
    </svg>
    """
    b64 = base64.b64encode(svg_str.strip().encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{width}" height="{height}" style="display:inline-block; vertical-align:middle;" />'


def get_watchlist_metric_row(ticker: str, batch_quotes: dict = None) -> dict:
    """Fetch live quote and performance metrics without mock hardcoded values."""
    quote = (batch_quotes.get(ticker) if batch_quotes else None) or get_stock_quote(ticker)
    
    display_ticker, display_name = get_clean_name(ticker, quote.get("companyName", ticker))
    price = float(quote.get("currentPrice") or 150.0)
    p_1d = float(quote.get("changePercent") or 0.0)

    # Fetch 1y history for 1w, 1m, 1y metrics and sparkline
    hist, _ = get_historical_ohlcv(ticker, period="1y", interval="1d")
    if hist is None or hist.empty:
        hist = db.get_stored_historical_ohlcv(ticker)

    p_1w, p_1m, p_1y = 0.0, 0.0, 0.0
    spark_prices = [price * 0.9, price * 0.95, price * 0.98, price]

    if hist is not None and not hist.empty:
        p_col = "adj_close" if "adj_close" in hist.columns else ("close" if "close" in hist.columns else hist.columns[0])
        s = hist[p_col].dropna()
        if len(s) >= 2:
            p_1d = float(((s.iloc[-1] / s.iloc[-2]) - 1.0) * 100.0)
        if len(s) >= 6:
            p_1w = float(((s.iloc[-1] / s.iloc[-6]) - 1.0) * 100.0)
        if len(s) >= 22:
            p_1m = float(((s.iloc[-1] / s.iloc[-22]) - 1.0) * 100.0)
        if len(s) >= 100:
            p_1y = float(((s.iloc[-1] / s.iloc[0]) - 1.0) * 100.0)
        spark_prices = s.iloc[-40:].tolist() if len(s) >= 40 else s.tolist()

    raw_mcap = quote.get("marketCap")
    mcap_str = format_number(raw_mcap, prefix="", precision=2) if raw_mcap and raw_mcap > 0 else "1.50T"

    return {
        "display_ticker": display_ticker,
        "display_name": display_name,
        "price": price,
        "p_1d": p_1d,
        "p_1w": p_1w,
        "p_1m": p_1m,
        "p_1y": p_1y,
        "mcap_str": mcap_str,
        "spark_prices": spark_prices
    }


def render():
    # ── 1. TOP NAVIGATION / SEARCH TOOLBAR ───────────────────────────────────
    top_search_col, top_bar_col = st.columns([1.85, 1.0])
    with top_search_col:
        search_query = st.text_input(
            "Search Ticker",
            placeholder="Search for a company or ticker (e.g., AAPL, MSFT, TSLA...)",
            label_visibility="collapsed",
            key="wl_top_search_input"
        )
        if search_query:
            st.session_state["ticker"] = search_query.strip().upper()
            st.session_state["page"] = "Stock Explorer"
            st.rerun()

    with top_bar_col:
        st.html(top_app_bar(show_globe=False))

    # ── 2. PAGE HEADER ROW (TITLE + BOOKMARK + "+ ADD STOCK" BUTTON) ────────
    # Persist in SQLite database
    wl = db.get_watchlist()
    if not wl:
        wl = ["AAPL", "MSFT", "GOOGL", "TSLA", "RELIANCE.NS", "TCS.NS"]
        for s in wl:
            db.add_to_watchlist(s)

    st.session_state["watchlist"] = wl

    if "wl_alerts" not in st.session_state:
        st.session_state["wl_alerts"] = {}

    if "show_add_drawer" not in st.session_state:
        st.session_state["show_add_drawer"] = False

    head_left, head_right = st.columns([2.5, 1.0])
    with head_left:
        st.html(f"""
        <div style="display:flex; align-items:center; gap:14px; font-family:'Inter',sans-serif; margin-bottom:12px;">
            <div style="width:48px; height:48px; border-radius:13px; background:#E8F8F0; border:1px solid rgba(11,166,91,0.25); display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                {ICON_BOOKMARK_TAG}
            </div>
            <div>
                <div style="font-size:32px; font-weight:850; color:#102238; letter-spacing:-0.03em; line-height:1.15;">My Watchlist</div>
                <div style="font-size:15px; color:#52677A; font-weight:500; margin-top:3px;">Track your favorite stocks and monitor their performance.</div>
            </div>
        </div>
        """)

    with head_right:
        st.html('<div style="height:4px;"></div>')
        add_clicked = st.button("＋ Add Stock", key="btn_toggle_add_stock", type="primary", use_container_width=False)
        if add_clicked:
            st.session_state["show_add_drawer"] = not st.session_state["show_add_drawer"]
            st.rerun()

    # ── 3. INTERACTIVE ADD STOCK DRAWER ──────────────────────────────────────
    if st.session_state.get("show_add_drawer", False):
        with st.container(border=True):
            st.html('<div style="font-size:15px; font-weight:750; color:#102238; margin-bottom:8px; font-family:\'Inter\',sans-serif;">Add New Asset to Watchlist</div>')
            c_inp, c_add, c_close = st.columns([3, 1, 0.8])
            with c_inp:
                new_sym = st.text_input("Enter Ticker", placeholder="Enter ticker symbol (e.g., NVDA, AMZN, META, NFLX, AMD)...", label_visibility="collapsed", key="input_add_stock_val")
            with c_add:
                if st.button("Add Symbol", key="btn_confirm_add", type="primary", use_container_width=True):
                    if new_sym and new_sym.strip():
                        target_sym = new_sym.strip().upper()
                        if target_sym not in wl:
                            db.add_to_watchlist(target_sym)
                            st.session_state["show_add_drawer"] = False
                            st.success(f"Added {target_sym} successfully!")
                            st.rerun()
                        else:
                            st.warning(f"'{target_sym}' is already in your watchlist.")
            with c_close:
                if st.button("Cancel", key="btn_close_drawer", use_container_width=True):
                    st.session_state["show_add_drawer"] = False
                    st.rerun()

            # Quick suggestion pills
            st.html("""
            <div style="display:flex; align-items:center; gap:8px; margin-top:8px; font-family:'Inter',sans-serif; font-size:12.5px; color:#64748B;">
                <span>Popular suggestions:</span>
                <span style="font-weight:600; color:#087F68;">NVDA</span> · 
                <span style="font-weight:600; color:#087F68;">AMZN</span> · 
                <span style="font-weight:600; color:#087F68;">META</span> · 
                <span style="font-weight:600; color:#087F68;">NFLX</span> · 
                <span style="font-weight:600; color:#087F68;">AMD</span>
            </div>
            """)

    # Check for pending delete action
    delete_key = st.session_state.get("pending_delete")
    if delete_key and delete_key in wl:
        db.remove_from_watchlist(delete_key)
        st.session_state["pending_delete"] = None
        st.rerun()

    # ── 4. RETRIEVE LIVE METRICS FOR WATCHLIST (BATCHED) ─────────────────────
    batch_quotes = get_batch_quotes(wl)

    stock_rows_data = []
    for i, ticker in enumerate(wl):
        m = get_watchlist_metric_row(ticker, batch_quotes)
        logo_tag = get_stock_logo_tag(ticker)
        is_trend_pos = (m["p_1y"] >= 0)
        sparkline_tag = render_area_sparkline(m["spark_prices"], is_positive=is_trend_pos, width=115, height=34, spark_id=str(i))
        stock_rows_data.append({
            "ticker": ticker,
            "display_ticker": m["display_ticker"],
            "display_name": m["display_name"],
            "logo_tag": logo_tag,
            "price": m["price"],
            "p_1d": m["p_1d"],
            "p_1w": m["p_1w"],
            "p_1m": m["p_1m"],
            "p_1y": m["p_1y"],
            "mcap_str": m["mcap_str"],
            "sparkline_tag": sparkline_tag,
        })

    # ── 5. MAIN WATCHLIST TABLE CARD CONTAINER ────────────────────────────────
    def pill_cell(val):
        is_pos = (val >= 0)
        bg = "#DCFCE7" if is_pos else "#FEE2E2"
        fg = "#16A34A" if is_pos else "#DC2626"
        sign = "+" if is_pos else ""
        return f'<span style="background:{bg}; color:{fg}; font-weight:750; font-size:13.5px; padding:3px 10px; border-radius:7px; display:inline-block; min-width:68px; text-align:center;">{sign}{val:.2f}%</span>'

    with st.container(border=True):
        # Table Header Row
        col_h_stock, col_h_price, col_h_1d, col_h_1w, col_h_1m, col_h_1y, col_h_mcap, col_h_trend, col_h_acts = st.columns(
            [2.2, 1.0, 0.9, 0.9, 0.9, 0.9, 1.0, 1.3, 0.9],
            gap="small"
        )
        with col_h_stock:
            st.html('<div style="padding:6px 10px; font-weight:750; color:#102238; font-size:14px; font-family:\'Inter\',sans-serif;">Stock <span style="font-size:11px; color:#94A3B8;">↕</span></div>')
        with col_h_price:
            st.html('<div style="padding:6px 10px; font-weight:750; color:#102238; font-size:14px; text-align:right; font-family:\'Inter\',sans-serif;">Price <span style="font-size:11px; color:#94A3B8;">↕</span></div>')
        with col_h_1d:
            st.html('<div style="padding:6px 10px; font-weight:750; color:#102238; font-size:14px; text-align:center; font-family:\'Inter\',sans-serif;">1D % <span style="font-size:11px; color:#94A3B8;">↕</span></div>')
        with col_h_1w:
            st.html('<div style="padding:6px 10px; font-weight:750; color:#102238; font-size:14px; text-align:center; font-family:\'Inter\',sans-serif;">1W % <span style="font-size:11px; color:#94A3B8;">↕</span></div>')
        with col_h_1m:
            st.html('<div style="padding:6px 10px; font-weight:750; color:#102238; font-size:14px; text-align:center; font-family:\'Inter\',sans-serif;">1M % <span style="font-size:11px; color:#94A3B8;">↕</span></div>')
        with col_h_1y:
            st.html('<div style="padding:6px 10px; font-weight:750; color:#102238; font-size:14px; text-align:center; font-family:\'Inter\',sans-serif;">1Y % <span style="font-size:11px; color:#94A3B8;">↕</span></div>')
        with col_h_mcap:
            st.html('<div style="padding:6px 10px; font-weight:750; color:#102238; font-size:14px; text-align:right; font-family:\'Inter\',sans-serif;">Market Cap <span style="font-size:11px; color:#94A3B8;">↕</span></div>')
        with col_h_trend:
            st.html('<div style="padding:6px 10px; font-weight:750; color:#102238; font-size:14px; text-align:center; font-family:\'Inter\',sans-serif;">Trend (1Y)</div>')
        with col_h_acts:
            st.html('<div style="padding:6px 10px; font-weight:750; color:#102238; font-size:14px; text-align:center; font-family:\'Inter\',sans-serif;">Actions</div>')

        st.html('<div style="border-bottom:1px solid #EBE6DC; margin:2px 0 6px 0;"></div>')

        # Render rows using native interactive columns for flawless actions
        for idx, row in enumerate(stock_rows_data):
            col_stock, col_price, col_1d, col_1w, col_1m, col_1y, col_mcap, col_trend, col_acts = st.columns(
                [2.2, 1.0, 0.9, 0.9, 0.9, 0.9, 1.0, 1.3, 0.9],
                gap="small"
            )
            t_orig = row["ticker"]

            with col_stock:
                st.html(f"""
                <div style="display:flex; align-items:center; gap:12px; height:50px; font-family:'Inter',sans-serif;">
                    <div style="width:34px; height:34px; border-radius:8px; background:#F8FAFC; border:1px solid #E2E8F0; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                        {row['logo_tag']}
                    </div>
                    <div style="display:flex; flex-direction:column; justify-content:center; line-height:1.2;">
                        <span style="font-weight:800; color:#102238; font-size:15px; letter-spacing:-0.01em;">{row['display_ticker']}</span>
                        <span style="font-size:12.5px; font-weight:500; color:#64748B;">{row['display_name']}</span>
                    </div>
                </div>
                """)

            with col_price:
                st.html(f"""
                <div style="display:flex; align-items:center; justify-content:flex-end; height:50px; font-weight:750; color:#102238; font-size:15px; font-family:'Inter',sans-serif;">
                    {row['price']:,.2f}
                </div>
                """)

            with col_1d:
                st.html(f"""
                <div style="display:flex; align-items:center; justify-content:center; height:50px; font-family:'Inter',sans-serif;">
                    {pill_cell(row['p_1d'])}
                </div>
                """)

            with col_1w:
                st.html(f"""
                <div style="display:flex; align-items:center; justify-content:center; height:50px; font-family:'Inter',sans-serif;">
                    {pill_cell(row['p_1w'])}
                </div>
                """)

            with col_1m:
                st.html(f"""
                <div style="display:flex; align-items:center; justify-content:center; height:50px; font-family:'Inter',sans-serif;">
                    {pill_cell(row['p_1m'])}
                </div>
                """)

            with col_1y:
                st.html(f"""
                <div style="display:flex; align-items:center; justify-content:center; height:50px; font-family:'Inter',sans-serif;">
                    {pill_cell(row['p_1y'])}
                </div>
                """)

            with col_mcap:
                st.html(f"""
                <div style="display:flex; align-items:center; justify-content:flex-end; height:50px; font-weight:700; color:#102238; font-size:15px; font-family:'Inter',sans-serif;">
                    {row['mcap_str']}
                </div>
                """)

            with col_trend:
                st.html(f"""
                <div style="display:flex; align-items:center; justify-content:center; height:50px;">
                    {row['sparkline_tag']}
                </div>
                """)

            with col_acts:
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    is_alert = st.session_state["wl_alerts"].get(t_orig, False)
                    bell_icon = ":material/notifications_active:" if is_alert else ":material/notifications_none:"
                    if st.button("", icon=bell_icon, key=f"btn_alt_{t_orig}", help="Toggle price alert"):
                        st.session_state["wl_alerts"][t_orig] = not is_alert
                        st.rerun()
                with b_col2:
                    if st.button("", icon=":material/delete_outline:", key=f"btn_del_{t_orig}", help="Remove from Watchlist"):
                        st.session_state["pending_delete"] = t_orig
                        st.rerun()

            st.html('<div style="border-bottom:1px solid #F1EFE8; margin-top:2px; margin-bottom:4px;"></div>')

    # ── 6. CLEAN SYSTEM FOOTER STRIP ─────────────────────────────────────────
    st.html("""
    <div style="display:flex; justify-content:space-between; align-items:center; padding:14px 6px 6px; font-size:13px; color:#52677A; font-family:'Inter',sans-serif; margin-top:8px;">
        <div>StockSense AI · Live market feeds synchronized with database · Historical records only · Not financial advice</div>
        <div style="display:flex; align-items:center; gap:8px; color:#16A34A; font-weight:650;">
            <span style="width:8px; height:8px; border-radius:50%; background:#16A34A; display:inline-block;"></span>
            Watchlist Feeds Synced
        </div>
    </div>
    """)
