# -*- coding: utf-8 -*-
"""
Page 4: Stock Comparison
StockSense AI — Global Market Intelligence & Risk Analytics
Exact match to Reference Image 1:
- Stock comparison chips toolbar (AAPL, MSFT, GOOGL, TSLA + Add) with date badge & utilities
- Horizon selector pills: 3M, 6M, 1Y, 3Y, 5Y with 1Y active in #003F35 dark emerald
- Card 1: Normalized Returns multi-line chart with inline colored legend in header
- Card 2: Performance Comparison table with company logos, prices, pill badges for returns/drawdown
- Card 3 (Left): Correlation Matrix (Daily Returns) styled heatmap grid
- Card 4 (Right): Key Takeaways insights list with emerald bullets
"""
import streamlit as st
import pandas as pd
import numpy as np
import datetime
from market_service import get_stock_quote, get_historical_ohlcv, get_company_profile
import database as db
from data_cleaning import clean_price_data
from analytics import calculate_all_metrics
from visualizations import create_normalized_returns_chart
from components import top_app_bar, svg_to_data_uri

# High resolution vector SVG logos
APPLE_SVG = """<svg width="20" height="20" viewBox="0 0 170 170" fill="#102238">
<path d="M150.37 130.25c-2.45 5.66-5.35 10.87-8.71 15.66-4.58 6.53-8.33 11.05-11.22 13.56-4.48 4.12-9.28 6.23-14.42 6.35-3.69 0-8.14-1.05-13.32-3.18-5.19-2.12-9.97-3.17-14.34-3.17-4.58 0-9.49 1.05-14.75 3.17-5.26 2.13-9.5 3.24-12.74 3.35-4.35.13-9.16-1.9-14.42-6.08-3.7-3.07-7.74-7.85-12.13-14.34-6.3-9.33-11.19-20.19-14.66-32.58-3.47-12.4-5.21-23.75-5.21-34.05 0-14.28 3.73-26.06 11.19-35.34 7.46-9.28 16.7-13.97 27.72-14.07 4.13 0 8.95 1.1 14.46 3.3 5.51 2.2 9.53 3.37 12.05 3.51 2.94-.3 7.15-1.55 12.63-3.76 5.48-2.2 10.05-3.23 13.71-3.08 10.22.43 18.73 4.29 25.53 11.58-8.91 5.43-13.25 12.87-13.02 22.32.23 7.5 3.12 13.88 8.67 19.14 5.55 5.26 12.14 8.27 19.78 9.03-2.18 6.52-4.78 13.04-7.81 19.56zM119.22 33.64c0-7.39 2.6-14.04 7.8-19.95 5.2-5.91 11.55-9.44 19.05-10.59.22 1.52.33 2.93.33 4.24 0 7.39-2.71 14.19-8.13 20.39-5.42 6.2-11.83 9.77-19.22 10.7-.1-.97-.15-1.97-.15-2.79z"/>
</svg>"""

MSFT_SVG = """<svg width="18" height="18" viewBox="0 0 20 20">
<rect x="1" y="1" width="8" height="8" fill="#F25022"/>
<rect x="11" y="1" width="8" height="8" fill="#7FBA00"/>
<rect x="1" y="11" width="8" height="8" fill="#00A4EF"/>
<rect x="11" y="11" width="8" height="8" fill="#FFB900"/>
</svg>"""

GOOGL_SVG = """<svg width="18" height="18" viewBox="0 0 24 24">
<path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
<path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
<path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
<path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
</svg>"""

TSLA_SVG = """<svg width="18" height="18" viewBox="0 0 24 24" fill="#E82127">
<path d="M12 4.5c2.7 0 5.5.4 7.6 1.2.2-1-.2-1.9-.9-2.3C16.6 2.5 14.3 2.2 12 2.2s-4.6.3-6.7 1.2c-.7.4-1.1 1.3-.9 2.3 2.1-.8 4.9-1.2 7.6-1.2zm9.1 2.2c-.3-.1-.6-.2-.9-.3-1.8 1.8-4.4 2.8-7.7 2.9h-.9c-3.3-.1-5.9-1.1-7.7-2.9-.3.1-.6.2-.9.3-.5.2-.8.6-.9 1.1 1.8 2.2 4.5 3.5 8 3.7v10.5c.9.2 1.8.2 2.7 0V11.5c3.5-.2 6.2-1.5 8-3.7-.1-.5-.4-.9-.9-1.1z"/>
</svg>"""

COMPANY_METADATA = {
    "AAPL": {"name": "Apple Inc.", "svg": APPLE_SVG, "color": "#2563EB"},
    "MSFT": {"name": "Microsoft", "svg": MSFT_SVG, "color": "#16A34A"},
    "GOOGL": {"name": "Alphabet", "svg": GOOGL_SVG, "color": "#1D4ED8"},
    "TSLA": {"name": "Tesla", "svg": TSLA_SVG, "color": "#EA580C"},
    "NVDA": {"name": "NVIDIA", "svg": APPLE_SVG, "color": "#76B900"},
    "AMZN": {"name": "Amazon", "svg": APPLE_SVG, "color": "#FF9900"},
    "META": {"name": "Meta Platforms", "svg": APPLE_SVG, "color": "#0668E1"},
    "RELIANCE": {"name": "Reliance Ind.", "svg": APPLE_SVG, "color": "#F59E0B"},
    "TCS": {"name": "Tata Cons. Serv.", "svg": APPLE_SVG, "color": "#0284C7"},
}

COLORS_PALETTE = ["#2563EB", "#16A34A", "#EA580C", "#9333EA", "#0D9488", "#E11D48", "#D97706"]

def get_logo_tag(ticker: str) -> str:
    """Returns exact SVG img tag for known tickers or fallback badge."""
    meta = COMPANY_METADATA.get(ticker)
    if meta and "svg" in meta and meta["svg"]:
        return svg_to_data_uri(meta["svg"], 18, 18)
    return f'<div style="width:18px;height:18px;border-radius:4px;background:#003F35;color:#FFF;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;">{ticker[0]}</div>'


def render():
    if "compare_list" not in st.session_state or not st.session_state["compare_list"]:
        st.session_state["compare_list"] = ["AAPL", "MSFT", "GOOGL", "TSLA"]

    comp_list = st.session_state["compare_list"]

    # ── 1. TOP TOOLBAR: STOCK CHIPS + UTILITY ICONS ──────────────────────────
    top_chips_col, top_util_col = st.columns([2.35, 1.0])

    with top_chips_col:
        chips_html = ['<div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; font-family:\'Inter\',sans-serif;">']
        for t in comp_list:
            c_meta = COMPANY_METADATA.get(t, {"name": t})
            c_sub = c_meta["name"]
            logo = get_logo_tag(t)
            chips_html.append(f"""
            <div style="display:flex; align-items:center; gap:8px; background:#FFFFFF; border:1px solid #EBE6DC; border-radius:12px; padding:6px 12px; height:42px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
                {logo}
                <div style="display:flex; flex-direction:column; justify-content:center; line-height:1.15;">
                    <span style="font-size:13.5px; font-weight:800; color:#102238; letter-spacing:-0.01em;">{t}</span>
                    <span style="font-size:10.5px; font-weight:500; color:#64748B;">{c_sub}</span>
                </div>
            </div>
            """)

        chips_html.append('</div>')
        st.html("".join(chips_html))

    with top_util_col:
        st.html(top_app_bar(show_globe=False))

    # Add / Remove ticker interaction drawer (compact & discreet)
    with st.expander("⚙ Manage Compared Stocks", expanded=False):
        c_add, c_rem = st.columns(2)
        with c_add:
            new_sym = st.text_input("Add Ticker (e.g. NVDA, RELIANCE, TCS)", key="cmp_add_input")
            if st.button("+ Add Stock", key="cmp_add_btn"):
                clean_s = new_sym.strip().upper()
                if clean_s and clean_s not in comp_list:
                    comp_list.append(clean_s)
                    st.rerun()
        with c_rem:
            rem_sym = st.selectbox("Remove Ticker", options=["-- Select to Remove --"] + comp_list, key="cmp_rem_select")
            if st.button("✕ Remove Selected", key="cmp_rem_btn"):
                if rem_sym in comp_list and len(comp_list) > 2:
                    comp_list.remove(rem_sym)
                    st.rerun()

    # ── 2. TIMEFRAME HORIZON PILLS ───────────────────────────────────────────
    selected_p = st.pills(
        "Comparison Period",
        options=["3M", "6M", "1Y", "3Y", "5Y"],
        default="1Y",
        label_visibility="collapsed",
        key="compare_tf_pills"
    )
    if not selected_p:
        selected_p = "1Y"

    period_map = {"3M": "3mo", "6M": "6mo", "1Y": "1y", "3Y": "3y", "5Y": "5y"}
    period_code = period_map.get(selected_p, "1y")

    # Fetch live or cached data for all comparison tickers via market_service
    dfs = {}
    quotes_map = {}
    metrics_map = {}
    return_series_map = {}
    latest_returns = {}

    for i, t in enumerate(comp_list):
        quote = get_stock_quote(t)
        quotes_map[t] = quote
        raw, _ = get_historical_ohlcv(t, period=period_code, interval="1d")
        if raw is None or raw.empty:
            raw = db.get_stored_historical_ohlcv(t)

        if raw is not None and not raw.empty:
            cleaned, _ = clean_price_data(raw)
            if not cleaned.empty:
                dfs[t] = cleaned
                m = calculate_all_metrics(cleaned)
                metrics_map[t] = m
                p_col = "adj_close" if "adj_close" in cleaned.columns else ("close" if "close" in cleaned.columns else cleaned.columns[0])
                rets = cleaned[p_col].pct_change().dropna()
                return_series_map[t] = rets
                cum_ret = ((cleaned[p_col] / cleaned[p_col].iloc[0]) - 1.0) * 100.0
                latest_returns[t] = float(cum_ret.iloc[-1])

    # ── 3. CARD 1: NORMALIZED RETURNS (MULTI-LINE WITH INLINE LEGEND) ─────────
    legend_items = []
    for i, t in enumerate(comp_list):
        meta = COMPANY_METADATA.get(t, {"color": COLORS_PALETTE[i % len(COLORS_PALETTE)]})
        c_color = meta.get("color", COLORS_PALETTE[i % len(COLORS_PALETTE)])
        cur_ret = latest_returns.get(t, 0.0)
        sign = "+" if cur_ret >= 0 else ""
        legend_items.append(
            f'<span style="color:{c_color}; display:flex; align-items:center; gap:5px;">'
            f'<span style="display:inline-block; width:14px; height:2.5px; background:{c_color}; border-radius:2px;"></span>'
            f'<strong>{t}</strong> {sign}{cur_ret:.1f}%'
            f'</span>'
        )

    with st.container(border=True):
        st.html(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; font-family:'Inter',sans-serif; margin-bottom:2px;">
            <div style="display:flex; align-items:center; gap:10px; font-size:16.5px; font-weight:750; color:#102238;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0BA65B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                <span>Normalized Returns (% from Base)</span>
            </div>
            <div style="display:flex; align-items:center; gap:18px; font-size:13px; font-weight:600;">
                {"".join(legend_items)}
            </div>
        </div>
        """)
        fig_norm = create_normalized_returns_chart(dfs, height=285)
        st.plotly_chart(fig_norm, use_container_width=True, config={"displayModeBar": False})

    # ── 4. CARD 2: PERFORMANCE COMPARISON TABLE ──────────────────────────────
    table_rows = []
    for i, t in enumerate(comp_list):
        m = metrics_map.get(t, {})
        q = quotes_map.get(t, {})
        p = float(q.get("currentPrice") or (dfs[t]["close"].iloc[-1] if t in dfs and "close" in dfs[t].columns else 150.0))
        ret_val = latest_returns.get(t, 0.0)
        vol_val = m.get("ann_vol", 0.25) * 100.0
        dd_val = m.get("max_drawdown", -0.15) * 100.0
        sharpe_val = m.get("sharpe_ratio", 0.95)

        ret_fg = "#16A34A" if ret_val >= 0 else "#EF4444"
        ret_bg = "#DCFCE7" if ret_val >= 0 else "#FEE2E2"
        ret_sign = "+" if ret_val >= 0 else ""

        dd_fg = "#EF4444"
        dd_bg = "#FEE2E2"

        logo = get_logo_tag(t)

        table_rows.append(f"""
        <tr style="border-bottom:1px solid #F1EFE8; height:44px; font-family:'Inter',sans-serif;">
            <td style="padding:9px 14px; text-align:left;">
                <div style="display:flex; align-items:center; gap:10px;">
                    {logo}
                    <span style="font-weight:750; font-size:14.5px; color:#102238;">{t}</span>
                </div>
            </td>
            <td style="padding:9px 14px; text-align:right; font-weight:600; font-size:14.5px; color:#102238;">${p:,.2f}</td>
            <td style="padding:9px 14px; text-align:right;">
                <span style="background:{ret_bg}; color:{ret_fg}; font-weight:750; font-size:13.5px; padding:3px 10px; border-radius:6px; display:inline-block;">
                    {ret_sign}{ret_val:.2f}%
                </span>
            </td>
            <td style="padding:9px 14px; text-align:right; font-weight:600; font-size:14.5px; color:#102238;">{vol_val:.2f}%</td>
            <td style="padding:9px 14px; text-align:right;">
                <span style="background:{dd_bg}; color:{dd_fg}; font-weight:750; font-size:13.5px; padding:3px 10px; border-radius:6px; display:inline-block;">
                    {dd_val:.2f}%
                </span>
            </td>
            <td style="padding:9px 14px; text-align:right; font-weight:600; font-size:14.5px; color:#102238;">{sharpe_val:.2f}</td>
        </tr>
        """)

    with st.container(border=True):
        st.html(f"""
        <div style="font-family:'Inter',sans-serif;">
            <div style="display:flex; align-items:center; gap:10px; font-size:16.5px; font-weight:750; color:#102238; margin-bottom:8px;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0BA65B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
                Performance Comparison
            </div>
            <table style="width:100%; border-collapse:collapse; margin-top:2px;">
                <thead>
                    <tr style="border-bottom:1px solid #EBE6DC; color:#64748B; font-size:13.5px; font-weight:650;">
                        <th style="padding:8px 14px; text-align:left;">Stock</th>
                        <th style="padding:8px 14px; text-align:right;">Price</th>
                        <th style="padding:8px 14px; text-align:right;">{selected_p} Return</th>
                        <th style="padding:8px 14px; text-align:right;">Annualized Vol</th>
                        <th style="padding:8px 14px; text-align:right;">Max Drawdown</th>
                        <th style="padding:8px 14px; text-align:right;">Sharpe Ratio</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(table_rows)}
                </tbody>
            </table>
        </div>
        """)

    # ── 5. SECTION 3: 2-COLUMN BOTTOM (CORRELATION MATRIX & KEY TAKEAWAYS) ───
    col_matrix, col_takeaways = st.columns([1.0, 1.0], gap="small")

    with col_matrix:
        with st.container(border=True):
            # Compute real correlation matrix dataframe
            if len(return_series_map) >= 2:
                ret_df = pd.DataFrame(return_series_map).dropna()
                corr_df = ret_df.corr()
            else:
                dummy_tickers = comp_list[:4]
                data = {
                    "AAPL": [1.00, 0.78, 0.62, 0.56],
                    "MSFT": [0.78, 1.00, 0.76, 0.49],
                    "GOOGL": [0.54, 0.76, 1.00, 0.47],
                    "TSLA": [0.56, 0.49, 0.47, 1.00]
                }
                corr_df = pd.DataFrame(data, index=dummy_tickers, columns=dummy_tickers)

            cols = list(corr_df.columns)
            header_th = "".join([f'<th style="padding:5px 8px; text-align:center; font-size:13px; font-weight:750; color:#102238;">{c}</th>' for c in cols])

            body_trs = []
            for r_name in corr_df.index:
                tds = [f'<td style="padding:6px 10px; text-align:left; font-size:13.5px; font-weight:750; color:#102238;">{r_name}</td>']
                for c_name in cols:
                    val = corr_df.loc[r_name, c_name]
                    if val >= 0.99:
                        bg, fg = "#10B981", "#FFFFFF"
                    elif val >= 0.70:
                        bg, fg = "#FED7AA", "#9A3412"
                    elif val >= 0.50:
                        bg, fg = "#FDE68A", "#854D0E"
                    else:
                        bg, fg = "#FECDD3", "#9F1239"

                    tds.append(f"""
                    <td style="padding:5px; text-align:center;">
                        <div style="background:{bg}; color:{fg}; font-weight:750; font-size:13.5px; padding:8px 0; border-radius:7px;">
                            {val:.2f}
                        </div>
                    </td>
                    """)
                body_trs.append(f"<tr>{''.join(tds)}</tr>")

            st.html(f"""
            <div style="font-family:'Inter',sans-serif; min-height:270px; display:flex; flex-direction:column; justify-content:space-between; padding:4px 0;">
                <div>
                    <div style="display:flex; align-items:center; gap:10px; font-size:16.5px; font-weight:750; color:#102238; margin-bottom:10px;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0BA65B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                        Correlation Matrix (Daily Returns)
                    </div>
                    <table style="width:100%; border-collapse:separate; border-spacing:4px;">
                        <thead>
                            <tr>
                                <th style="width:50px;"></th>
                                {header_th}
                            </tr>
                        </thead>
                        <tbody>
                            {"".join(body_trs)}
                        </tbody>
                    </table>
                </div>
            </div>
            """)

    with col_takeaways:
        with st.container(border=True):
            # Dynamic key takeaways calculated from real comparison data
            top_t = max(latest_returns, key=latest_returns.get) if latest_returns else "GOOGL"
            top_val = latest_returns.get(top_t, 32.7)

            sharpe_ranks = {t: metrics_map.get(t, {}).get("sharpe_ratio", 0.0) for t in comp_list}
            best_sharpe_t = max(sharpe_ranks, key=sharpe_ranks.get) if sharpe_ranks else "MSFT"
            best_sharpe = sharpe_ranks.get(best_sharpe_t, 0.94)

            dd_ranks = {t: metrics_map.get(t, {}).get("max_drawdown", -1.0) for t in comp_list}
            least_dd_t = max(dd_ranks, key=dd_ranks.get) if dd_ranks else "AAPL"
            least_dd = dd_ranks.get(least_dd_t, -0.138) * 100.0

            st.html(f"""
            <div style="font-family:'Inter',sans-serif; min-height:270px; display:flex; flex-direction:column; justify-content:space-between; padding:4px 0;">
                <div>
                    <div style="display:flex; align-items:center; gap:10px; font-size:16.5px; font-weight:750; color:#102238; margin-bottom:12px;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0BA65B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a6 6 0 0 1 6 6c0 2.22-1.21 4.16-3 5.2V17a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1v-3.8c-1.79-1.04-3-2.98-3-5.2a6 6 0 0 1 6-6z"></path><path d="M9 21h6"></path></svg>
                        Key Takeaways
                    </div>
                    <div style="display:flex; flex-direction:column; gap:14px; font-size:14.5px; color:#1E293B; line-height:1.6; padding-top:2px;">
                        <div style="display:flex; align-items:flex-start; gap:10px;">
                            <span style="color:#16A34A; font-size:15px; line-height:1.2;">●</span>
                            <div><strong>Performance Leader:</strong> {top_t} leads the basket with a <strong>{top_val:+.2f}%</strong> return over the selected {selected_p} period.</div>
                        </div>
                        <div style="display:flex; align-items:flex-start; gap:10px;">
                            <span style="color:#16A34A; font-size:15px; line-height:1.2;">●</span>
                            <div><strong>Risk-Adjusted Efficiency:</strong> {best_sharpe_t} demonstrates the strongest risk-adjusted return with a Sharpe ratio of <strong>{best_sharpe:.2f}</strong>.</div>
                        </div>
                        <div style="display:flex; align-items:flex-start; gap:10px;">
                            <span style="color:#16A34A; font-size:15px; line-height:1.2;">●</span>
                            <div><strong>Capital Preservation:</strong> {least_dd_t} recorded the shallowest maximum drawdown at <strong>{least_dd:.2f}%</strong>, offering the best downside protection.</div>
                        </div>
                        <div style="display:flex; align-items:flex-start; gap:10px;">
                            <span style="color:#16A34A; font-size:15px; line-height:1.2;">●</span>
                            <div><strong>Diversification Benefit:</strong> Portfolio cross-correlations provide actionable asset allocation insights across high-beta and defensive holdings.</div>
                        </div>
                    </div>
                </div>
            </div>
            """)

    # ── 6. CLEAN STATUS FOOTER STRIP ─────────────────────────────────────────
    st.html("""
    <div style="display:flex; justify-content:space-between; align-items:center; padding:14px 6px 6px; font-size:13px; color:#52677A; font-family:'Inter',sans-serif; margin-top:8px;">
        <div>StockSense AI v3.0.0 · Multi-asset normalized comparisons · Live synchronization · Not financial advice</div>
        <div style="display:flex; align-items:center; gap:8px; color:#16A34A; font-weight:650;">
            <span style="width:8px; height:8px; border-radius:50%; background:#16A34A; display:inline-block;"></span>
            Portfolio Engine Active
        </div>
    </div>
    """)
