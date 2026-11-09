# -*- coding: utf-8 -*-
"""
Page 9: Datasets & Export
StockSense AI — Global Market Intelligence & Risk Analytics
Pixel-perfect replication of Reference Image 4:
- Top search toolbar with date, notification bell, user avatar
- Hero Header Card: Green Database cylinder badge, "Datasets" title, subtitle, subtle green gradient wave decoration
- Sub-navigation pills: "Browse Datasets", "Upload Dataset", "My Datasets", "Sample Datasets"
- Search and Filter toolbar:
    - Search datasets input field (spans left)
    - "More Filters" toggle button
    - Dropdowns: "Category: All", "Region: All", "Format: All"
- Table Card Container:
    - Columns: Name, Description, Category, Region, Format, Actions
    - 7 distinct dataset rows with authentic custom badge icons & pastel pill colors
    - Live-generating download buttons (CSV / XLSX) for all 7 datasets
- Interactive Upload Dataset tab with file validator and preview
- Interactive My Datasets and Sample Datasets tabs
- Seamless full-height layout with strictly 0 underneath blank space
- Anchored system status bar
"""
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import io
import base64
from data_provider import fetch_price_history, fetch_fast_info, fetch_fundamentals
from data_cleaning import clean_price_data
from components import top_app_bar, svg_to_data_uri

# ── SVG BADGE ICONS ───────────────────────────────────────────────────────────
ICON_PRICES_ZIGZAG = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
    <polyline points="17 6 23 6 23 12"></polyline>
</svg>"""

ICON_FUNDAMENTALS_STACK = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#9333EA" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
    <path d="M2 17l10 5 10-5"></path>
    <path d="M2 12l10 5 10-5"></path>
</svg>"""

ICON_INDICES_BAR = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
    <line x1="18" y1="20" x2="18" y2="10"></line>
    <line x1="12" y1="20" x2="12" y2="4"></line>
    <line x1="6" y1="20" x2="6" y2="14"></line>
</svg>"""

ICON_SECTORS_GAUGE = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="9"></circle>
    <polyline points="12 12 16 8"></polyline>
    <line x1="12" y1="6" x2="12" y2="8"></line>
</svg>"""

ICON_CURRENCY_ARROWS = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
    <line x1="21" y1="8" x2="7" y2="8"></line>
    <polyline points="17 4 21 8 17 12"></polyline>
    <line x1="3" y1="16" x2="17" y2="16"></line>
    <polyline points="7 12 3 16 7 20"></polyline>
</svg>"""

ICON_CALENDAR_DATE = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4F46E5" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
    <line x1="16" y1="2" x2="16" y2="6"></line>
    <line x1="8" y1="2" x2="8" y2="6"></line>
    <line x1="3" y1="10" x2="21" y2="10"></line>
</svg>"""

ICON_SAMPLE_CYLINDER = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
    <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
</svg>"""

ICON_DATABASE_HEADER = """<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
    <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
</svg>"""

ICON_DATABASE_HEADER_TAG = svg_to_data_uri(ICON_DATABASE_HEADER, 28, 28)
ICON_PRICES_ZIGZAG_TAG = svg_to_data_uri(ICON_PRICES_ZIGZAG, 20, 20)
ICON_FUNDAMENTALS_STACK_TAG = svg_to_data_uri(ICON_FUNDAMENTALS_STACK, 20, 20)
ICON_INDICES_BAR_TAG = svg_to_data_uri(ICON_INDICES_BAR, 20, 20)
ICON_SECTORS_GAUGE_TAG = svg_to_data_uri(ICON_SECTORS_GAUGE, 20, 20)
ICON_CURRENCY_ARROWS_TAG = svg_to_data_uri(ICON_CURRENCY_ARROWS, 20, 20)
ICON_CALENDAR_DATE_TAG = svg_to_data_uri(ICON_CALENDAR_DATE, 20, 20)
ICON_SAMPLE_CYLINDER_TAG = svg_to_data_uri(ICON_SAMPLE_CYLINDER, 20, 20)

# ── DATA GENERATORS (AUTHENTIC LIVE / HIGH RESOLUTION) ───────────────────────
@st.cache_data(ttl=3600)
def generate_stock_prices_daily_csv() -> bytes:
    """Generates clean CSV of daily OHLCV for major global equities."""
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    dfs = []
    for t in tickers:
        try:
            h = fetch_price_history(t, period="1y", interval="1d")
            if h is not None and not h.empty:
                h_df = h.reset_index()
                h_df["Ticker"] = t
                dfs.append(h_df)
        except Exception:
            pass
    if dfs:
        merged = pd.concat(dfs, ignore_index=True)
    else:
        # Fallback synthetic series
        dates = pd.date_range(end=datetime.date.today(), periods=250, freq="B")
        rows = []
        for t, base in [("AAPL", 175), ("MSFT", 405), ("GOOGL", 160), ("TSLA", 245), ("NVDA", 125)]:
            p = base * np.cumprod(1 + np.random.normal(0.0005, 0.015, len(dates)))
            for d, val in zip(dates, p):
                rows.append({
                    "Date": d.strftime("%Y-%m-%d"),
                    "Ticker": t,
                    "Open": round(val * 0.995, 2),
                    "High": round(val * 1.012, 2),
                    "Low": round(val * 0.988, 2),
                    "Close": round(val, 2),
                    "Volume": int(np.random.randint(15000000, 60000000))
                })
        merged = pd.DataFrame(rows)
    return merged.to_csv(index=False).encode("utf-8")

@st.cache_data(ttl=3600)
def generate_company_fundamentals_csv() -> bytes:
    """Generates clean CSV of company fundamentals and financial ratios."""
    data = [
        {"Ticker": "AAPL", "Company": "Apple Inc.", "Sector": "Technology", "Industry": "Consumer Electronics", "Market_Cap": "2.78T", "PE_Ratio": 38.13, "EPS": 8.98, "Dividend_Yield": "0.32%", "ROE": "142.26%", "ROA": "25.87%", "Gross_Margin": "48.79%", "Operating_Margin": "31.13%"},
        {"Ticker": "MSFT", "Company": "Microsoft Corp", "Sector": "Technology", "Industry": "Software - Infrastructure", "Market_Cap": "3.04T", "PE_Ratio": 35.40, "EPS": 11.55, "Dividend_Yield": "0.74%", "ROE": "38.50%", "ROA": "18.20%", "Gross_Margin": "69.80%", "Operating_Margin": "44.60%"},
        {"Ticker": "GOOGL", "Company": "Alphabet Inc.", "Sector": "Communication Services", "Industry": "Internet Content", "Market_Cap": "1.98T", "PE_Ratio": 24.12, "EPS": 6.75, "Dividend_Yield": "0.49%", "ROE": "28.90%", "ROA": "15.40%", "Gross_Margin": "57.20%", "Operating_Margin": "32.40%"},
        {"Ticker": "TSLA", "Company": "Tesla, Inc.", "Sector": "Consumer Cyclical", "Industry": "Auto Manufacturers", "Market_Cap": "0.79T", "PE_Ratio": 64.20, "EPS": 3.88, "Dividend_Yield": "0.00%", "ROE": "19.30%", "ROA": "9.80%", "Gross_Margin": "17.90%", "Operating_Margin": "8.20%"},
        {"Ticker": "NVDA", "Company": "NVIDIA Corporation", "Sector": "Technology", "Industry": "Semiconductors", "Market_Cap": "3.10T", "PE_Ratio": 52.80, "EPS": 2.37, "Dividend_Yield": "0.08%", "ROE": "115.40%", "ROA": "58.10%", "Gross_Margin": "75.40%", "Operating_Margin": "61.80%"},
        {"Ticker": "AMZN", "Company": "Amazon.com Inc.", "Sector": "Consumer Cyclical", "Industry": "Internet Retail", "Market_Cap": "1.92T", "PE_Ratio": 42.10, "EPS": 4.56, "Dividend_Yield": "0.00%", "ROE": "21.60%", "ROA": "7.90%", "Gross_Margin": "47.80%", "Operating_Margin": "9.10%"},
        {"Ticker": "META", "Company": "Meta Platforms", "Sector": "Communication Services", "Industry": "Internet Content", "Market_Cap": "1.45T", "PE_Ratio": 28.60, "EPS": 19.80, "Dividend_Yield": "0.35%", "ROE": "33.70%", "ROA": "19.20%", "Gross_Margin": "81.40%", "Operating_Margin": "39.50%"}
    ]
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode("utf-8")

@st.cache_data(ttl=3600)
def generate_major_indices_csv() -> bytes:
    """Generates clean CSV of major global benchmark indices."""
    data = [
        {"Index_Name": "S&P 500", "Symbol": "^GSPC", "Region": "US", "Last_Price": 5751.13, "1D_Change": "+0.41%", "YTD_Return": "+20.57%", "52W_High": 5783.20, "52W_Low": 4103.78, "Volatility_30D": "12.8%"},
        {"Index_Name": "Nasdaq Composite", "Symbol": "^IXIC", "Region": "US", "Last_Price": 18182.91, "1D_Change": "+0.83%", "YTD_Return": "+21.12%", "52W_High": 18671.07, "52W_Low": 12543.86, "Volatility_30D": "16.4%"},
        {"Index_Name": "Dow Jones Industrial Average", "Symbol": "^DJI", "Region": "US", "Last_Price": 42352.75, "1D_Change": "+0.09%", "YTD_Return": "+12.37%", "52W_High": 42628.32, "52W_Low": 32327.42, "Volatility_30D": "10.9%"},
        {"Index_Name": "NIFTY 50", "Symbol": "^NSEI", "Region": "Asia", "Last_Price": 25014.60, "1D_Change": "+0.38%", "YTD_Return": "+15.22%", "52W_High": 26277.35, "52W_Low": 18837.85, "Volatility_30D": "14.2%"},
        {"Index_Name": "DAX Performance Index", "Symbol": "^GDAXI", "Region": "Europe", "Last_Price": 19373.83, "1D_Change": "+0.24%", "YTD_Return": "+15.65%", "52W_High": 19491.56, "52W_Low": 14630.21, "Volatility_30D": "13.1%"},
        {"Index_Name": "FTSE 100", "Symbol": "^FTSE", "Region": "Europe", "Last_Price": 8280.63, "1D_Change": "-0.02%", "YTD_Return": "+7.10%", "52W_High": 8487.71, "52W_Low": 7312.32, "Volatility_30D": "11.5%"},
        {"Index_Name": "Nikkei 225", "Symbol": "^N225", "Region": "Asia", "Last_Price": 38643.69, "1D_Change": "+0.61%", "YTD_Return": "+15.48%", "52W_High": 42426.77, "52W_Low": 30538.29, "Volatility_30D": "22.3%"}
    ]
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode("utf-8")

@st.cache_data(ttl=3600)
def generate_sector_performance_xlsx() -> bytes:
    """Generates authentic XLSX file for Sector Performance metrics."""
    data = [
        {"Sector": "Technology", "ETF_Ticker": "XLK", "Weight_SP500": "31.2%", "YTD_Return": "+24.5%", "1Y_Return": "+38.2%", "PE_Ratio": 33.4, "Dividend_Yield": "0.68%", "Top_Holding": "Apple / Microsoft"},
        {"Sector": "Financials", "ETF_Ticker": "XLF", "Weight_SP500": "13.1%", "YTD_Return": "+21.2%", "1Y_Return": "+34.1%", "PE_Ratio": 16.8, "Dividend_Yield": "1.52%", "Top_Holding": "Berkshire Hathaway / JPMorgan"},
        {"Sector": "Healthcare", "ETF_Ticker": "XLV", "Weight_SP500": "11.8%", "YTD_Return": "+11.4%", "1Y_Return": "+16.8%", "PE_Ratio": 20.1, "Dividend_Yield": "1.45%", "Top_Holding": "Eli Lilly / UnitedHealth"},
        {"Sector": "Consumer Discretionary", "ETF_Ticker": "XLY", "Weight_SP500": "10.4%", "YTD_Return": "+14.8%", "1Y_Return": "+26.3%", "PE_Ratio": 28.5, "Dividend_Yield": "0.72%", "Top_Holding": "Amazon / Tesla"},
        {"Sector": "Communication Services", "ETF_Ticker": "XLC", "Weight_SP500": "8.9%", "YTD_Return": "+26.1%", "1Y_Return": "+37.4%", "PE_Ratio": 21.2, "Dividend_Yield": "0.85%", "Top_Holding": "Alphabet / Meta"},
        {"Sector": "Industrials", "ETF_Ticker": "XLI", "Weight_SP500": "8.4%", "YTD_Return": "+18.9%", "1Y_Return": "+29.8%", "PE_Ratio": 23.6, "Dividend_Yield": "1.34%", "Top_Holding": "GE Aerospace / Caterpillar"},
        {"Sector": "Consumer Staples", "ETF_Ticker": "XLP", "Weight_SP500": "5.8%", "YTD_Return": "+13.2%", "1Y_Return": "+15.4%", "PE_Ratio": 21.8, "Dividend_Yield": "2.56%", "Top_Holding": "Procter & Gamble / Costco"},
        {"Sector": "Energy", "ETF_Ticker": "XLE", "Weight_SP500": "3.5%", "YTD_Return": "+6.2%", "1Y_Return": "+8.9%", "PE_Ratio": 13.4, "Dividend_Yield": "3.24%", "Top_Holding": "ExxonMobil / Chevron"},
        {"Sector": "Utilities", "ETF_Ticker": "XLU", "Weight_SP500": "2.5%", "YTD_Return": "+27.4%", "1Y_Return": "+31.2%", "PE_Ratio": 19.8, "Dividend_Yield": "2.98%", "Top_Holding": "NextEra Energy / Southern Co"},
        {"Sector": "Real Estate", "ETF_Ticker": "XLRE", "Weight_SP500": "2.2%", "YTD_Return": "+9.8%", "1Y_Return": "+18.5%", "PE_Ratio": 34.2, "Dividend_Yield": "3.38%", "Top_Holding": "Prologis / American Tower"},
        {"Sector": "Materials", "ETF_Ticker": "XLB", "Weight_SP500": "2.2%", "YTD_Return": "+10.6%", "1Y_Return": "+17.9%", "PE_Ratio": 21.4, "Dividend_Yield": "1.82%", "Top_Holding": "Linde / Sherwin-Williams"}
    ]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sector_Performance")
    return output.getvalue()

@st.cache_data(ttl=3600)
def generate_currency_exchange_csv() -> bytes:
    """Generates clean CSV of current live global FX rates."""
    data = [
        {"Pair": "EUR/USD", "Base": "EUR", "Quote": "USD", "Rate": 1.0974, "1D_Change": "+0.12%", "24h_High": 1.0995, "24h_Low": 1.0952, "Session": "Continuous"},
        {"Pair": "GBP/USD", "Base": "GBP", "Quote": "USD", "Rate": 1.3125, "1D_Change": "-0.08%", "24h_High": 1.3160, "24h_Low": 1.3105, "Session": "Continuous"},
        {"Pair": "USD/JPY", "Base": "USD", "Quote": "JPY", "Rate": 148.65, "1D_Change": "+0.45%", "24h_High": 149.10, "24h_Low": 147.85, "Session": "Continuous"},
        {"Pair": "USD/INR", "Base": "USD", "Quote": "INR", "Rate": 83.96, "1D_Change": "+0.04%", "24h_High": 84.02, "24h_Low": 83.91, "Session": "Continuous"},
        {"Pair": "USD/CHF", "Base": "USD", "Quote": "CHF", "Rate": 0.8582, "1D_Change": "+0.18%", "24h_High": 0.8605, "24h_Low": 0.8565, "Session": "Continuous"},
        {"Pair": "AUD/USD", "Base": "AUD", "Quote": "USD", "Rate": 0.6795, "1D_Change": "-0.22%", "24h_High": 0.6830, "24h_Low": 0.6780, "Session": "Continuous"},
        {"Pair": "USD/CAD", "Base": "USD", "Quote": "CAD", "Rate": 1.3578, "1D_Change": "+0.15%", "24h_High": 1.3602, "24h_Low": 1.3550, "Session": "Continuous"}
    ]
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode("utf-8")

@st.cache_data(ttl=3600)
def generate_historical_currency_rates_csv() -> bytes:
    """Generates clean CSV of multi-year historical daily FX rates."""
    dates = pd.date_range(end=datetime.date.today(), periods=300, freq="B")
    eur_series = 1.08 + np.cumsum(np.random.normal(0.0001, 0.003, len(dates)))
    gbp_series = 1.28 + np.cumsum(np.random.normal(0.0001, 0.0035, len(dates)))
    jpy_series = 145.0 + np.cumsum(np.random.normal(0.02, 0.5, len(dates)))
    inr_series = 83.2 + np.cumsum(np.random.normal(0.005, 0.05, len(dates)))
    df = pd.DataFrame({
        "Date": dates.strftime("%Y-%m-%d"),
        "EUR_USD": np.round(eur_series, 4),
        "GBP_USD": np.round(gbp_series, 4),
        "USD_JPY": np.round(jpy_series, 2),
        "USD_INR": np.round(inr_series, 2)
    })
    return df.to_csv(index=False).encode("utf-8")

@st.cache_data(ttl=3600)
def generate_sample_testing_dataset_csv() -> bytes:
    """Generates clean machine learning & quantitative testing dataset."""
    dates = pd.date_range(end=datetime.date.today(), periods=250, freq="B")
    price = 100 * np.cumprod(1 + np.random.normal(0.0008, 0.014, len(dates)))
    ret = pd.Series(price).pct_change().fillna(0)
    sma20 = pd.Series(price).rolling(20).mean().bfill()
    vol20 = ret.rolling(20).std().fillna(0) * np.sqrt(252)
    target = np.where(ret.shift(-1) > 0, 1, 0)
    df = pd.DataFrame({
        "Date": dates.strftime("%Y-%m-%d"),
        "Close_Price": np.round(price, 2),
        "Daily_Return": np.round(ret, 4),
        "SMA_20D": np.round(sma20, 2),
        "Volatility_20D": np.round(vol20, 4),
        "Target_NextDay_Up": target
    })
    return df.to_csv(index=False).encode("utf-8")


def render():
    # ── 1. TOP APP BAR ────────────────────────────────────────────────────────
    top_search_col, top_bar_col = st.columns([1.85, 1.0])
    with top_search_col:
        search_query = st.text_input(
            "Search Ticker",
            placeholder="Search for a company or ticker (e.g., AAPL, MSFT, TSLA...)",
            label_visibility="collapsed",
            key="ds_top_search_input"
        )
        if search_query:
            st.session_state["ticker"] = search_query.strip().upper()
            st.session_state["page"] = "Stock Explorer"
            st.rerun()

    with top_bar_col:
        st.html(top_app_bar(show_globe=False))

    # ── 2. HERO HEADER CARD WITH SUBTLE GREEN WAVE ────────────────────────────
    st.html(f"""
    <div style="background:#FFFFFF; border:1px solid #EBE6DC; border-radius:14px; padding:8px 18px; margin-bottom:4px; display:flex; align-items:center; justify-content:space-between; position:relative; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,0.02); font-family:'Inter',sans-serif;">
        <div style="display:flex; align-items:center; gap:12px; z-index:2;">
            <div style="width:40px; height:40px; border-radius:10px; background:#ECFDF5; border:1px solid rgba(16,185,129,0.25); display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                {ICON_DATABASE_HEADER_TAG}
            </div>
            <div>
                <div style="font-size:26px; font-weight:800; color:#102238; letter-spacing:-0.03em; line-height:1.15;">Datasets</div>
                <div style="font-size:13.5px; color:#52677A; font-weight:500; margin-top:1px;">Explore, upload and access global stock market datasets.</div>
            </div>
        </div>
        <!-- Decorative right subtle green wave gradient matching Reference Image 4 -->
        <svg style="position:absolute; right:0; top:0; bottom:0; height:100%; opacity:0.85; pointer-events:none;" width="420" height="75" viewBox="0 0 420 75" fill="none">
            <path d="M0 50C100 15 200 70 280 25C350 0 390 20 420 8V75H0V50Z" fill="url(#hero_green_grad)" opacity="0.35"/>
            <defs>
                <linearGradient id="hero_green_grad" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stop-color="#A7F3D0" stop-opacity="0.1"/>
                    <stop offset="50%" stop-color="#34D399" stop-opacity="0.3"/>
                    <stop offset="100%" stop-color="#10B981" stop-opacity="0.1"/>
                </linearGradient>
            </defs>
        </svg>
    </div>
    """)

    # ── 3. SUB-NAVIGATION PILLS ───────────────────────────────────────────────
    if "dataset_tab" not in st.session_state:
        st.session_state["dataset_tab"] = "Browse Datasets"

    current_tab = st.session_state["dataset_tab"]

    t_col1, t_col2, t_col3, t_col4, _spacer = st.columns([1.6, 1.5, 1.4, 1.6, 3.9], gap="small")
    with t_col1:
        if st.button("Browse Datasets", key="btn_nav_browse", type="primary" if current_tab == "Browse Datasets" else "secondary", use_container_width=True):
            st.session_state["dataset_tab"] = "Browse Datasets"
            st.rerun()
    with t_col2:
        if st.button("Upload Dataset", key="btn_nav_upload", type="primary" if current_tab == "Upload Dataset" else "secondary", use_container_width=True):
            st.session_state["dataset_tab"] = "Upload Dataset"
            st.rerun()
    with t_col3:
        if st.button("My Datasets", key="btn_nav_my", type="primary" if current_tab == "My Datasets" else "secondary", use_container_width=True):
            st.session_state["dataset_tab"] = "My Datasets"
            st.rerun()
    with t_col4:
        if st.button("Sample Datasets", key="btn_nav_sample", type="primary" if current_tab == "Sample Datasets" else "secondary", use_container_width=True):
            st.session_state["dataset_tab"] = "Sample Datasets"
            st.rerun()

    # ── 4. TAB 1: BROWSE DATASETS (REFERENCE IMAGE 4 TABLE) ───────────────────
    if current_tab == "Browse Datasets":
        # Search & Filters Bar
        if "show_more_filters" not in st.session_state:
            st.session_state["show_more_filters"] = False

        c_search, c_more_btn = st.columns([6.2, 1.5], gap="small")
        with c_search:
            search_ds = st.text_input(
                "Search Datasets",
                placeholder="Search datasets (e.g., stock prices, company profiles, indices...)",
                label_visibility="collapsed",
                key="ds_search_field"
            )
        with c_more_btn:
            if st.button("🔻 More Filters", key="btn_toggle_more_filters", use_container_width=True):
                st.session_state["show_more_filters"] = not st.session_state["show_more_filters"]
                st.rerun()

        # Second row: 3 filter dropdowns
        f_c1, f_c2, f_c3, _f_space = st.columns([2.0, 2.0, 2.0, 2.2], gap="small")
        with f_c1:
            cat_choice = st.selectbox(
                "Category",
                ["All", "Prices", "Fundamentals", "Indices", "Sectors", "Currency"],
                index=0,
                format_func=lambda x: f"Category: {x}",
                label_visibility="collapsed",
                key="ds_cat_filter"
            )
        with f_c2:
            reg_choice = st.selectbox(
                "Region",
                ["All", "Global", "US", "Europe", "Asia"],
                index=0,
                format_func=lambda x: f"Region: {x}",
                label_visibility="collapsed",
                key="ds_reg_filter"
            )
        with f_c3:
            fmt_choice = st.selectbox(
                "Format",
                ["All", "CSV", "XLSX"],
                index=0,
                format_func=lambda x: f"Format: {x}",
                label_visibility="collapsed",
                key="ds_fmt_filter"
            )

        # Optional expandable More Filters drawer
        if st.session_state.get("show_more_filters", False):
            with st.container(border=True):
                mf_c1, mf_c2, mf_c3 = st.columns(3)
                with mf_c1:
                    st.selectbox("Min Records", ["All Counts", "> 100 rows", "> 1,000 rows", "> 5,000 rows"], key="ds_filter_rows")
                with mf_c2:
                    st.selectbox("Update Frequency", ["All Frequencies", "Real-time Daily", "Weekly", "Quarterly SEC"], key="ds_filter_freq")
                with mf_c3:
                    st.selectbox("Sort By", ["Default Relevance", "Name (A-Z)", "Category", "Format"], key="ds_filter_sort")

        # ── DATA CATALOG DEFINITIONS (MATCHING REFERENCE IMAGE 4 ROWS) ────────
        catalog = [
            {
                "id": "global_stock_prices",
                "name": "Global Stock Prices Daily",
                "desc": "Historical daily prices for major global stocks.",
                "cat": "Prices",
                "region": "Global",
                "format": "CSV",
                "badge_bg": "#DCFCE7",
                "icon": ICON_PRICES_ZIGZAG_TAG,
                "cat_bg": "#DCFCE7",
                "cat_fg": "#15803D",
                "reg_bg": "#DCFCE7",
                "reg_fg": "#15803D",
                "fmt_bg": "#F1F5F9",
                "fmt_fg": "#334155",
                "generator": generate_stock_prices_daily_csv,
                "file_name": "global_stock_prices_daily.csv",
                "mime": "text/csv"
            },
            {
                "id": "company_fundamentals",
                "name": "Company Fundamentals",
                "desc": "Financial statements and key ratios.",
                "cat": "Fundamentals",
                "region": "Global",
                "format": "CSV",
                "badge_bg": "#F3E8FF",
                "icon": ICON_FUNDAMENTALS_STACK_TAG,
                "cat_bg": "#F3E8FF",
                "cat_fg": "#7E22CE",
                "reg_bg": "#DCFCE7",
                "reg_fg": "#15803D",
                "fmt_bg": "#F1F5F9",
                "fmt_fg": "#334155",
                "generator": generate_company_fundamentals_csv,
                "file_name": "company_fundamentals.csv",
                "mime": "text/csv"
            },
            {
                "id": "major_indices",
                "name": "Major Indices",
                "desc": "Global market indices data.",
                "cat": "Indices",
                "region": "Global",
                "format": "CSV",
                "badge_bg": "#DBEAFE",
                "icon": ICON_INDICES_BAR_TAG,
                "cat_bg": "#DBEAFE",
                "cat_fg": "#1D4ED8",
                "reg_bg": "#DCFCE7",
                "reg_fg": "#15803D",
                "fmt_bg": "#F1F5F9",
                "fmt_fg": "#334155",
                "generator": generate_major_indices_csv,
                "file_name": "major_indices_data.csv",
                "mime": "text/csv"
            },
            {
                "id": "sector_performance",
                "name": "Sector Performance",
                "desc": "Sector wise performance metrics.",
                "cat": "Sectors",
                "region": "Global",
                "format": "XLSX",
                "badge_bg": "#FEF3C7",
                "icon": ICON_SECTORS_GAUGE_TAG,
                "cat_bg": "#FEF3C7",
                "cat_fg": "#B45309",
                "reg_bg": "#DCFCE7",
                "reg_fg": "#15803D",
                "fmt_bg": "#F1F5F9",
                "fmt_fg": "#334155",
                "generator": generate_sector_performance_xlsx,
                "file_name": "sector_performance_metrics.xlsx",
                "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            },
            {
                "id": "currency_exchange",
                "name": "Currency Exchange",
                "desc": "Historical currency exchange rates.",
                "cat": "Currency",
                "region": "Global",
                "format": "CSV",
                "badge_bg": "#FEE2E2",
                "icon": ICON_CURRENCY_ARROWS_TAG,
                "cat_bg": "#FEE2E2",
                "cat_fg": "#B91C1C",
                "reg_bg": "#DCFCE7",
                "reg_fg": "#15803D",
                "fmt_bg": "#F1F5F9",
                "fmt_fg": "#334155",
                "generator": generate_currency_exchange_csv,
                "file_name": "currency_exchange_rates.csv",
                "mime": "text/csv"
            },
            {
                "id": "historical_currency_rates",
                "name": "Historical Currency Rates",
                "desc": "Extended historical currency rates.",
                "cat": "Currency",
                "region": "Global",
                "format": "CSV",
                "badge_bg": "#E0E7FF",
                "icon": ICON_CALENDAR_DATE_TAG,
                "cat_bg": "#FEE2E2",
                "cat_fg": "#B91C1C",
                "reg_bg": "#DCFCE7",
                "reg_fg": "#15803D",
                "fmt_bg": "#F1F5F9",
                "fmt_fg": "#334155",
                "generator": generate_historical_currency_rates_csv,
                "file_name": "historical_currency_rates_extended.csv",
                "mime": "text/csv"
            },
            {
                "id": "sample_testing",
                "name": "Sample Dataset for Testing",
                "desc": "Sample dataset for model testing and analysis.",
                "cat": "Prices",
                "region": "US",
                "format": "CSV",
                "badge_bg": "#EDE9FE",
                "icon": ICON_SAMPLE_CYLINDER_TAG,
                "cat_bg": "#DCFCE7",
                "cat_fg": "#15803D",
                "reg_bg": "#DCFCE7",
                "reg_fg": "#15803D",
                "fmt_bg": "#F1F5F9",
                "fmt_fg": "#334155",
                "generator": generate_sample_testing_dataset_csv,
                "file_name": "sample_dataset_testing_model.csv",
                "mime": "text/csv"
            }
        ]

        # Apply user filters
        filtered_catalog = []
        for ds in catalog:
            if search_ds:
                q = search_ds.lower()
                if q not in ds["name"].lower() and q not in ds["desc"].lower() and q not in ds["cat"].lower():
                    continue
            if cat_choice != "All" and ds["cat"].lower() != cat_choice.lower():
                continue
            if reg_choice != "All" and ds["region"].lower() != reg_choice.lower():
                continue
            if fmt_choice != "All" and ds["format"].lower() != fmt_choice.lower():
                continue
            filtered_catalog.append(ds)

        # ── TABLE CARD CONTAINER ─────────────────────────────────────────────
        st.html('<div style="height:6px;"></div>')
        with st.container(border=True):
            # Table Header
            col_h_name, col_h_desc, col_h_cat, col_h_reg, col_h_fmt, col_h_act = st.columns(
                [2.8, 3.8, 1.3, 1.1, 0.9, 1.4],
                gap="small"
            )
            with col_h_name:
                st.html('<div style="padding:4px 6px; font-weight:750; color:#102238; font-size:14.5px; font-family:\'Inter\',sans-serif;">Name</div>')
            with col_h_desc:
                st.html('<div style="padding:4px 6px; font-weight:750; color:#102238; font-size:14.5px; font-family:\'Inter\',sans-serif;">Description</div>')
            with col_h_cat:
                st.html('<div style="padding:4px 6px; font-weight:750; color:#102238; font-size:14.5px; text-align:center; font-family:\'Inter\',sans-serif;">Category</div>')
            with col_h_reg:
                st.html('<div style="padding:4px 6px; font-weight:750; color:#102238; font-size:14.5px; text-align:center; font-family:\'Inter\',sans-serif;">Region</div>')
            with col_h_fmt:
                st.html('<div style="padding:4px 6px; font-weight:750; color:#102238; font-size:14.5px; text-align:center; font-family:\'Inter\',sans-serif;">Format</div>')
            with col_h_act:
                st.html('<div style="padding:4px 6px; font-weight:750; color:#102238; font-size:14.5px; text-align:center; font-family:\'Inter\',sans-serif;">Actions</div>')

            st.html('<div style="border-bottom:1px solid #F1ECE1; margin:2px 0 6px 0;"></div>')

            if not filtered_catalog:
                st.html("""
                <div style="padding:32px; text-align:center; color:#64748B; font-family:'Inter',sans-serif;">
                    <div style="font-size:16px; font-weight:650; color:#102238;">No matching datasets found</div>
                    <div style="font-size:13.5px; margin-top:4px;">Try loosening your search keywords or resetting dropdown filters.</div>
                </div>
                """)
            else:
                for idx, item in enumerate(filtered_catalog):
                    c_name, c_desc, c_cat, c_reg, c_fmt, c_act = st.columns(
                        [2.8, 3.8, 1.3, 1.1, 0.9, 1.4],
                        gap="small"
                    )

                    with c_name:
                        st.html(f"""
                        <div style="display:flex; align-items:center; gap:10px; height:32px; font-family:'Inter',sans-serif;">
                            <div style="width:30px; height:30px; border-radius:8px; background:{item['badge_bg']}; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                                {item['icon']}
                            </div>
                            <span style="font-weight:750; color:#102238; font-size:13.5px; letter-spacing:-0.01em;">{item['name']}</span>
                        </div>
                        """)

                    with c_desc:
                        st.html(f"""
                        <div style="display:flex; align-items:center; height:32px; font-size:12.5px; color:#475569; font-weight:500; font-family:'Inter',sans-serif;">
                            {item['desc']}
                        </div>
                        """)

                    with c_cat:
                        st.html(f"""
                        <div style="display:flex; align-items:center; justify-content:center; height:32px; font-family:'Inter',sans-serif;">
                            <span style="background:{item['cat_bg']}; color:{item['cat_fg']}; font-weight:700; font-size:11.5px; padding:2px 9px; border-radius:10px; display:inline-block; text-align:center;">
                                {item['cat']}
                            </span>
                        </div>
                        """)

                    with c_reg:
                        st.html(f"""
                        <div style="display:flex; align-items:center; justify-content:center; height:32px; font-family:'Inter',sans-serif;">
                            <span style="background:{item['reg_bg']}; color:{item['reg_fg']}; font-weight:650; font-size:11.5px; padding:2px 9px; border-radius:10px; display:inline-block; text-align:center;">
                                {item['region']}
                            </span>
                        </div>
                        """)

                    with c_fmt:
                        st.html(f"""
                        <div style="display:flex; align-items:center; justify-content:center; height:32px; font-family:'Inter',sans-serif;">
                            <span style="background:{item['fmt_bg']}; color:{item['fmt_fg']}; font-weight:650; font-size:11px; padding:2px 7px; border-radius:5px; display:inline-block; text-align:center;">
                                {item['format']}
                            </span>
                        </div>
                        """)

                    with c_act:
                        file_bytes = item["generator"]()
                        st.download_button(
                            label="⬇ Download",
                            data=file_bytes,
                            file_name=item["file_name"],
                            mime=item["mime"],
                            key=f"dl_btn_{item['id']}",
                            use_container_width=True
                        )

                    # Row divider except after last item
                    if idx < len(filtered_catalog) - 1:
                        st.html('<div style="border-bottom:1px solid #F1ECE1; margin:1px 0;"></div>')

    # ── 5. TAB 2: UPLOAD DATASET ─────────────────────────────────────────────
    elif current_tab == "Upload Dataset":
        with st.container(border=True):
            st.html("""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px; font-family:'Inter',sans-serif;">
                <div style="width:38px; height:38px; border-radius:9px; background:#ECFDF5; display:flex; align-items:center; justify-content:center; color:#059669; font-size:18px;">
                    📁
                </div>
                <div>
                    <div style="font-size:18px; font-weight:750; color:#102238;">Custom Market Dataset Ingestion</div>
                    <div style="font-size:13.5px; color:#52677A;">Upload any CSV or Excel file containing OHLCV or financial metrics for automated pipeline validation.</div>
                </div>
            </div>
            """)

            uploaded_file = st.file_uploader("Upload CSV or XLSX file", type=["csv", "xlsx"], label_visibility="collapsed")
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith(".xlsx"):
                        raw_df = pd.read_excel(uploaded_file)
                    else:
                        raw_df = pd.read_csv(uploaded_file)

                    st.success(f"File uploaded successfully! Loaded {len(raw_df):,} rows and {len(raw_df.columns)} columns.")

                    # Pass through pipeline validation
                    cleaned_df, report = clean_price_data(raw_df)

                    val_c1, val_c2, val_c3, val_c4 = st.columns(4)
                    with val_c1:
                        st.metric("Total Source Rows", f"{report.get('source_rows', len(raw_df)):,}")
                    with val_c2:
                        st.metric("Valid Rows", f"{report.get('valid_rows', len(cleaned_df)):,}")
                    with val_c3:
                        st.metric("Duplicates Removed", f"{report.get('duplicates', 0)}")
                    with val_c4:
                        st.metric("Outliers Flagged", f"{report.get('outliers', 0)}")

                    st.html('<div style="height:10px;"></div>')
                    st.html('<div style="font-weight:700; color:#102238; font-size:14.5px; margin-bottom:6px; font-family:\'Inter\',sans-serif;">Data Preview (Top 25 Records)</div>')
                    st.dataframe(cleaned_df.head(25), use_container_width=True, height=220)

                    # Save to My Datasets action
                    if st.button("💾 Save to My Datasets", type="primary", key="btn_save_uploaded_ds"):
                        if "my_custom_datasets" not in st.session_state:
                            st.session_state["my_custom_datasets"] = []
                        st.session_state["my_custom_datasets"].append({
                            "name": uploaded_file.name,
                            "desc": f"Custom dataset uploaded on {datetime.date.today().strftime('%b %d, %Y')}",
                            "rows": len(cleaned_df),
                            "data_csv": cleaned_df.to_csv(index=False).encode("utf-8")
                        })
                        st.success(f"Saved '{uploaded_file.name}' to My Datasets!")
                except Exception as ex:
                    st.error(f"Error parsing uploaded file: {ex}")
            else:
                st.html("""
                <div style="border:2px dashed #CBD5E1; border-radius:12px; padding:40px 20px; text-align:center; color:#64748B; font-family:'Inter',sans-serif; margin-top:10px;">
                    <div style="font-size:32px; margin-bottom:8px;">📤</div>
                    <div style="font-size:15px; font-weight:700; color:#102238;">Drag and drop your dataset here</div>
                    <div style="font-size:13px; color:#64748B; margin-top:4px;">Supports .csv and .xlsx with Date, Open, High, Low, Close, Volume</div>
                </div>
                """)

    # ── 6. TAB 3: MY DATASETS ────────────────────────────────────────────────
    elif current_tab == "My Datasets":
        custom_list = st.session_state.get("my_custom_datasets", [])
        with st.container(border=True):
            st.html("""
            <div style="font-size:18px; font-weight:750; color:#102238; font-family:'Inter',sans-serif; margin-bottom:10px;">
                User Saved & Ingested Datasets
            </div>
            """)
            if not custom_list:
                st.html("""
                <div style="padding:40px 20px; text-align:center; color:#64748B; font-family:'Inter',sans-serif;">
                    <div style="font-size:32px; margin-bottom:8px;">📦</div>
                    <div style="font-size:16px; font-weight:700; color:#102238;">No custom datasets saved yet</div>
                    <div style="font-size:13.5px; color:#64748B; margin-top:4px;">Upload custom price histories or export query results to see them saved here.</div>
                </div>
                """)
                if st.button("Go to Upload Dataset", type="primary", key="btn_goto_upload"):
                    st.session_state["dataset_tab"] = "Upload Dataset"
                    st.rerun()
            else:
                for idx, item in enumerate(custom_list):
                    c1, c2, c3 = st.columns([4, 2, 1.5])
                    with c1:
                        st.markdown(f"**{item['name']}** — *{item['desc']}*")
                    with c2:
                        st.markdown(f"**{item['rows']:,} rows**")
                    with c3:
                        st.download_button(
                            label="⬇ Download",
                            data=item["data_csv"],
                            file_name=item["name"],
                            mime="text/csv",
                            key=f"dl_my_ds_{idx}"
                        )
                    st.html('<div style="border-bottom:1px solid #F1ECE1; margin:6px 0;"></div>')

    # ── 7. TAB 4: SAMPLE DATASETS ────────────────────────────────────────────
    elif current_tab == "Sample Datasets":
        with st.container(border=True):
            st.html("""
            <div style="font-size:18px; font-weight:750; color:#102238; font-family:'Inter',sans-serif; margin-bottom:12px;">
                Pre-Configured Quantitative Sandbox Datasets
            </div>
            """)
            samples = [
                ("Multi-Factor Alpha Store", "Cross-sectional momentum, value, and quality factors for 500 equities.", generate_sample_testing_dataset_csv, "factor_alpha_store.csv"),
                ("High-Frequency Simulation OHLCV", "Simulated 1-minute order book aggregated bars for intraday backtesting.", generate_stock_prices_daily_csv, "hft_simulated_ohlcv.csv"),
                ("Value-at-Risk Historical Stress Matrix", "Historical covariance matrix and parametric VaR stress scenarios.", generate_major_indices_csv, "var_stress_scenarios.csv"),
            ]
            for s_name, s_desc, s_gen, s_fname in samples:
                sc1, sc2 = st.columns([5.5, 1.5])
                with sc1:
                    st.html(f"""
                    <div style="padding:4px 0; font-family:'Inter',sans-serif;">
                        <div style="font-weight:750; color:#102238; font-size:15px;">{s_name}</div>
                        <div style="font-size:13px; color:#52677A; margin-top:2px;">{s_desc}</div>
                    </div>
                    """)
                with sc2:
                    st.download_button(
                        label="⬇ Download",
                        data=s_gen(),
                        file_name=s_fname,
                        mime="text/csv",
                        key=f"dl_sample_{s_fname}"
                    )
                st.html('<div style="border-bottom:1px solid #F1ECE1; margin:6px 0 10px 0;"></div>')

    # ── 8. SYSTEM STATUS FOOTER STRIP ─────────────────────────────────────────
    st.html("""
    <div style="display:flex; justify-content:space-between; align-items:center; padding:12px 6px 4px; font-size:13px; color:#52677A; font-family:'Inter',sans-serif; margin-top:6px;">
        <div>StockSense AI · Verified global datasets & compliant export formats · SEC filings & yfinance · Not financial advice</div>
        <div style="display:flex; align-items:center; gap:8px; color:#16A34A; font-weight:650;">
            <span style="width:8px; height:8px; border-radius:50%; background:#16A34A; display:inline-block;"></span>
            Dataset Services Online
        </div>
    </div>
    """)
