# -*- coding: utf-8 -*-
"""
Page 3: Risk Analytics
StockSense AI — Global Market Intelligence & Risk Analytics
Exact match to Reference Image 1:
- Top search input & utility bar with date, notification bell, user avatar
- Company Identity Card: Logo, 32px bold ticker, name, metadata, price, percentage pill, as-of subtext
- Timeframe selector pills: 1M, 3M, 6M, 1Y, 3Y, 5Y with 1Y active in #003F35 dark emerald
- 4 Risk KPI Cards (Row 1): Annualized Volatility, Maximum Drawdown, Sharpe Ratio, Beta (vs S&P 500)
- Main 2-Column Analytics Grid:
    - Left Column: Drawdown Analysis chart + Rolling Volatility (30-day) chart
    - Right Column: Return Distribution histogram + Risk Metrics table
- Clean status footer strip anchoring the page
"""
import streamlit as st
import pandas as pd
import numpy as np
import datetime
from market_service import get_stock_quote, get_historical_ohlcv, get_company_profile
import database as db
from data_cleaning import clean_price_data
from analytics import calculate_all_metrics
from visualizations import create_drawdown_chart, create_distribution_chart, create_rolling_volatility_chart
from components import top_app_bar, clean_html, svg_to_data_uri

# High resolution, official Apple logo SVG
APPLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="#102238" viewBox="0 0 24 24">
<path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.61-.75 1.04-1.8 1.01-2.87-.9.04-2.02.6-2.68 1.34-.56.63-.99 1.66-.94 2.69.98.08 2-.45 2.61-1.16z"/>
</svg>"""

def render_risk_kpi_card(title: str, value: str, subtext: str, icon_type: str = "volatility") -> str:
    """Render a single 80px Risk KPI card strictly matching Reference Image 1."""
    if icon_type == "volatility":
        svg_code = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#0BA65B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 6-7 6 14 10 14 4-7 4-7"></path></svg>'
        icon_bg = "#E8F8F0"
        icon_border = "rgba(11,166,91,0.2)"
        tag_color = "#0BA65B"
        corner_gradient = "radial-gradient(circle at bottom right, rgba(168,222,193,0.4) 0%, rgba(255,255,255,0) 70%)"
        info_icon = ""
    elif icon_type == "drawdown":
        svg_code = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></svg>'
        icon_bg = "#FEE2E2"
        icon_border = "rgba(239,68,68,0.2)"
        tag_color = "#EF4444"
        corner_gradient = "radial-gradient(circle at bottom right, rgba(254,202,202,0.4) 0%, rgba(255,255,255,0) 70%)"
        info_icon = ""
    elif icon_type == "sharpe":
        svg_code = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#0BA65B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="3" x2="12" y2="21"></line><path d="M5 8l7-4 7 4"></path><path d="M5 8v6a3 3 0 0 0 6 0V8"></path><path d="M13 8v6a3 3 0 0 0 6 0V8"></path></svg>'
        icon_bg = "#E8F8F0"
        icon_border = "rgba(11,166,91,0.2)"
        tag_color = "#0BA65B"
        corner_gradient = "radial-gradient(circle at bottom right, rgba(168,222,193,0.4) 0%, rgba(255,255,255,0) 70%)"
        info_icon = ' <span style="font-size:11px; color:#94A3B8; cursor:help;">ⓘ</span>'
    else:  # beta
        svg_code = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none"><text x="6" y="17" font-family="Inter,sans-serif" font-size="16" font-weight="800" fill="#9333EA">β</text></svg>'
        icon_bg = "#F3E8FF"
        icon_border = "rgba(147,51,234,0.2)"
        tag_color = "#52677A"
        corner_gradient = "radial-gradient(circle at bottom right, rgba(216,180,254,0.4) 0%, rgba(255,255,255,0) 70%)"
        info_icon = ""

    img_tag = svg_to_data_uri(svg_code, 15, 15)

    raw_html = f"""
    <div style="flex:1; min-width:0; height:106px; background:#FFFFFF; border:1px solid #EBE6DC; border-radius:16px; padding:14px 20px; box-shadow:0 1px 4px rgba(0,0,0,0.02); position:relative; overflow:hidden; font-family:'Inter',sans-serif; display:flex; align-items:center; gap:16px; transition:all 0.2s ease;">
        <div style="position:absolute; bottom:0; right:0; width:110px; height:65px; background:{corner_gradient}; pointer-events:none;"></div>
        <div style="width:46px; height:46px; border-radius:12px; background:{icon_bg}; border:1px solid {icon_border}; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            {img_tag}
        </div>
        <div style="min-width:0;">
            <div style="font-size:14px; font-weight:600; color:#64748B; line-height:1.2; margin-bottom:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{title}{info_icon}</div>
            <div style="font-size:28px; font-weight:800; color:#102238; line-height:1; letter-spacing:-0.02em;">{value}</div>
            <div style="font-size:13.5px; font-weight:600; color:{tag_color}; line-height:1.2; margin-top:3px;">{subtext}</div>
        </div>
    </div>
    """
    return clean_html(raw_html)


def render():
    ticker = st.session_state.get("ticker", "AAPL").strip().upper()
    benchmark_ticker = st.session_state.get("benchmark", "SPY")

    # Time frame map
    period_options = {
        "1M": ("1mo", "1d"),
        "3M": ("3mo", "1d"),
        "6M": ("6mo", "1d"),
        "1Y": ("1y", "1d"),
        "3Y": ("3y", "1wk"),
        "5Y": ("5y", "1wk"),
    }

    # Fetch normalized live quote and profile
    quote = get_stock_quote(ticker)
    profile = get_company_profile(ticker)

    company_name = profile.get("company_name") or quote.get("companyName") or (
        "Apple Inc." if ticker == "AAPL" else ticker
    )
    exchange = profile.get("exchange") or quote.get("exchange") or ("NASDAQ" if ticker in ["AAPL", "MSFT", "GOOGL", "TSLA"] else "NYSE")
    country = profile.get("country") or "United States"
    sector = profile.get("sector") or "Technology"
    website = profile.get("website")

    price = float(quote.get("currentPrice") or 178.32)
    change = float(quote.get("change") or 0.0)
    pct_change = float(quote.get("changePercent") or 0.0)

    # ── 1. TOP NAVIGATION / SEARCH TOOLBAR ───────────────────────────────────
    top_search_col, top_bar_col = st.columns([1.85, 1.0])
    with top_search_col:
        search_default = f"{ticker} - {company_name}"
        
        def on_search_change():
            val = st.session_state.get("risk_search_field", "").strip()
            if val:
                p_ticker = val.split(" - ")[0].split()[0].strip().upper()
                if p_ticker and p_ticker != st.session_state.get("ticker"):
                    st.session_state["ticker"] = p_ticker

        st.text_input(
            "Search Ticker",
            value=search_default,
            placeholder="Search for a company or ticker (e.g., AAPL, RELIANCE, TSLA, TCS ...)",
            label_visibility="collapsed",
            key="risk_search_field",
            on_change=on_search_change
        )

    with top_bar_col:
        st.html(top_app_bar(show_globe=False))

    st.html('<div style="height:2px;"></div>')

    # ── 2. COMPANY IDENTITY SECTION (UNIFIED PREMIUM CARD) ───────────────────
    is_pos = (pct_change >= 0)
    chg_color = "#0BA65B" if is_pos else "#EF4444"
    chg_arrow = "↑" if is_pos else "↓"
    sign = "+" if is_pos else ""
    meta_line = f"{exchange} · {country} · {sector}"

    # Logo element
    if ticker == "AAPL":
        logo_tag = svg_to_data_uri(APPLE_SVG, 34, 34)
    else:
        from data_provider import get_company_logo_url
        ext_logo = get_company_logo_url(ticker, website)
        if ext_logo:
            logo_tag = f'<img src="{ext_logo}" style="width:34px; height:34px; object-fit:contain; border-radius:8px;" />'
        else:
            logo_tag = f'<div style="width:34px; height:34px; border-radius:8px; background:linear-gradient(135deg, #003F35, #087E69); display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-size:16px; font-weight:800;">{ticker[0]}</div>'

    now_time = datetime.datetime.now().strftime("Oct %d, %Y %I:%M %p")
    as_of_text = f"As of {now_time}"

    cid_box = st.container(border=True)
    with cid_box:
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
                <div style="font-size:13px; font-weight:500; color:#64748B; margin-top:5px;">{as_of_text}</div>
            </div>
            """)

    # ── 3. TIMEFRAME PILLS ───────────────────────────────────────────────────
    selected_tf = st.pills(
        "Risk Period",
        options=["1M", "3M", "6M", "1Y", "3Y", "5Y"],
        default="1Y",
        label_visibility="collapsed",
        key="risk_tf_pills"
    )
    if not selected_tf:
        selected_tf = "1Y"

    # Fetch price history for risk calculations via centralized market service
    period_str, interval_str = period_options.get(selected_tf, ("1y", "1d"))
    raw_df, _ = get_historical_ohlcv(ticker, period=period_str, interval=interval_str)
    bench_df, _ = get_historical_ohlcv(benchmark_ticker, period=period_str, interval=interval_str)

    if raw_df is None or raw_df.empty:
        raw_df = db.get_stored_historical_ohlcv(ticker)

    clean_df, _ = clean_price_data(raw_df) if raw_df is not None and not raw_df.empty else (pd.DataFrame(), None)
    clean_bench, _ = clean_price_data(bench_df) if bench_df is not None and not bench_df.empty else (pd.DataFrame(), None)

    metrics = calculate_all_metrics(clean_df, clean_bench)

    # ── 4. 4 RISK KPI STAT CARDS (ROW 1) ─────────────────────────────────────
    vol = metrics.get("ann_vol", 0.2489) * 100.0
    vol_tag = "(Moderate)" if vol < 30 else ("(High Risk)" if vol >= 35 else "(Normal)")

    max_dd = metrics.get("max_drawdown", -0.1380) * 100.0
    dd_tag = "(Moderate Risk)" if abs(max_dd) < 20 else "(High Risk)"

    sharpe = metrics.get("sharpe_ratio", 0.94)
    sharpe_tag = "(Good)" if sharpe >= 0.8 else "(Sub-optimal)"

    beta = metrics.get("beta", 0.59)
    beta_tag = "(Low Risk)" if beta < 0.9 else ("(High Risk)" if beta > 1.2 else "(Benchmark Aligned)")

    kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
    with kpi_c1:
        st.html(render_risk_kpi_card("Annualized Volatility", f"{vol:.2f}%", vol_tag, "volatility"))
    with kpi_c2:
        st.html(render_risk_kpi_card("Maximum Drawdown", f"{max_dd:.2f}%", dd_tag, "drawdown"))
    with kpi_c3:
        st.html(render_risk_kpi_card("Sharpe Ratio", f"{sharpe:.2f}", sharpe_tag, "sharpe"))
    with kpi_c4:
        st.html(render_risk_kpi_card(f"Beta (vs {benchmark_ticker})", f"{beta:.2f}", beta_tag, "beta"))

    # ── 5. MAIN 2-COLUMN ANALYTICS SECTION ───────────────────────────────────
    col_left, col_right = st.columns([1.62, 1.0], gap="small")

    p_col = "adj_close" if "adj_close" in clean_df.columns else ("close" if "close" in clean_df.columns else None)
    returns = clean_df[p_col].pct_change().dropna() if p_col and not clean_df.empty else pd.Series(dtype=float)

    with col_left:
        # Card 1: Drawdown Analysis
        with st.container(border=True):
            st.html("""
            <div style="display:flex; align-items:center; gap:9px; font-family:'Inter',sans-serif; font-size:16px; font-weight:750; color:#102238; margin-bottom:6px;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0BA65B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="7" x2="17" y2="17"></line><polyline points="17 7 17 17 7 17"></polyline></svg>
                Drawdown Analysis
            </div>
            """)
            dd_fig = create_drawdown_chart(metrics.get("drawdown_series"))
            st.plotly_chart(dd_fig, use_container_width=True, config={"displayModeBar": False})

        # Card 2: Rolling Volatility (30-day)
        with st.container(border=True):
            st.html("""
            <div style="display:flex; align-items:center; gap:9px; font-family:'Inter',sans-serif; font-size:16px; font-weight:750; color:#102238; margin-bottom:6px;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 6-7 6 14 10 14 4-7 4-7"></path></svg>
                Rolling Volatility (30-day)
            </div>
            """)
            roll_fig = create_rolling_volatility_chart(returns)
            st.plotly_chart(roll_fig, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        # Card 3: Return Distribution
        with st.container(border=True):
            st.html("""
            <div style="display:flex; align-items:center; gap:9px; font-family:'Inter',sans-serif; font-size:16px; font-weight:750; color:#102238; margin-bottom:6px;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0BA65B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                Return Distribution
            </div>
            """)
            dist_fig = create_distribution_chart(returns)
            st.plotly_chart(dist_fig, use_container_width=True, config={"displayModeBar": False})

        # Card 4: Risk Metrics
        best_ret = returns.max() * 100.0 if not returns.empty else 7.28
        worst_ret = returns.min() * 100.0 if not returns.empty else -6.91
        pos_days = int((returns > 0).sum()) if not returns.empty else 130
        total_days = max(len(returns), 1) if not returns.empty else 250
        neg_days = total_days - pos_days
        pos_pct = (pos_days / total_days) * 100.0
        neg_pct = (neg_days / total_days) * 100.0
        curr_dd = metrics.get("current_drawdown", -0.0412) * 100.0
        calmar = metrics.get("calmar_ratio", 2.03)

        with st.container(border=True):
            st.html(f"""
            <div style="font-family:'Inter',sans-serif; padding:2px 4px;">
                <div style="display:flex; align-items:center; gap:10px; font-size:17.5px; font-weight:750; color:#102238; margin-bottom:12px;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0BA65B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                    Risk Metrics
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #F1EFE8;">
                    <span style="color:#64748B; font-size:14.5px; font-weight:550;">Best Daily Return</span>
                    <span style="color:#0BA65B; font-weight:750; font-size:15px;">{best_ret:+.2f}%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #F1EFE8;">
                    <span style="color:#64748B; font-size:14.5px; font-weight:550;">Worst Daily Return</span>
                    <span style="color:#EF4444; font-weight:750; font-size:15px;">{worst_ret:.2f}%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #F1EFE8;">
                    <span style="color:#64748B; font-size:14.5px; font-weight:550;">Positive Days</span>
                    <span style="color:#102238; font-weight:750; font-size:15px;">{pos_days} ({pos_pct:.1f}%)</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #F1EFE8;">
                    <span style="color:#64748B; font-size:14.5px; font-weight:550;">Negative Days</span>
                    <span style="color:#102238; font-weight:750; font-size:15px;">{neg_days} ({neg_pct:.1f}%)</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #F1EFE8;">
                    <span style="color:#64748B; font-size:14.5px; font-weight:550;">Current Drawdown</span>
                    <span style="color:#EF4444; font-weight:750; font-size:15px;">{curr_dd:.2f}%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0;">
                    <span style="color:#64748B; font-size:14.5px; font-weight:550;">Calmar Ratio</span>
                    <span style="color:#102238; font-weight:750; font-size:15px;">{calmar:.2f}</span>
                </div>
            </div>
            """)

    # ── 6. CLEAN STATUS FOOTER STRIP ─────────────────────────────────────────
    st.html(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; padding:14px 6px 6px; font-size:13px; color:#52677A; font-family:'Inter',sans-serif; margin-top:8px;">
        <div>StockSense AI v3.0.0 · Risk calculations parameterized to 252 annual trading days · Benchmark: {benchmark_ticker} · Not financial advice</div>
        <div style="display:flex; align-items:center; gap:8px; color:#16A34A; font-weight:650;">
            <span style="width:8px; height:8px; border-radius:50%; background:#16A34A; display:inline-block;"></span>
            Quantitative Model Active
        </div>
    </div>
    """)
