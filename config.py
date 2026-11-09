# -*- coding: utf-8 -*-
"""
Configuration and constants for StockSense AI
"""

import os
from dotenv import load_dotenv

load_dotenv()

# App Constants
APP_NAME = "StockSense AI"
APP_SUBTITLE = "Global Market Intelligence & Risk Analytics"
APP_VERSION = "v3.0.0"
DATA_PROVIDER_NAME = "yfinance"

# Groq LLM Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_DEFAULT_MODEL = "openai/gpt-oss-120b"
GROQ_MODELS = [
    "openai/gpt-oss-120b (Recommended)",
    "openai/gpt-oss-20b (Fast)",
    "qwen/qwen3.8-27b",
    "allam-2-7b"
]

# Market Data Providers Configuration
TWELVE_DATA_API_KEY = os.environ.get("TWELVE_DATA_API_KEY", "")

# Default state values
DEFAULT_TICKER = "AAPL"
DEFAULT_MARKET = "United States"
DEFAULT_BENCHMARK = "SPY"
DEFAULT_RISK_FREE_RATE = 0.045  # 4.5% annual
TRADING_DAYS_PER_YEAR = 252

# Default comparison list
DEFAULT_COMPARE_LIST = ["AAPL", "MSFT", "GOOGL", "TSLA"]

# Default Watchlist
DEFAULT_WATCHLIST = ["AAPL", "MSFT", "GOOGL", "TSLA", "RELIANCE.NS", "TCS.NS"]

# Market Movers (12 major global assets)
MARKET_MOVERS = [
    {"ticker": "AAPL", "name": "Apple", "country": "United States", "region": "US"},
    {"ticker": "MSFT", "name": "Microsoft", "country": "United States", "region": "US"},
    {"ticker": "NVDA", "name": "NVIDIA", "country": "United States", "region": "US"},
    {"ticker": "TSLA", "name": "Tesla", "country": "United States", "region": "US"},
    {"ticker": "ASML", "name": "ASML Holding", "country": "Netherlands", "region": "Europe"},
    {"ticker": "SAP.DE", "name": "SAP", "country": "Germany", "region": "Europe"},
    {"ticker": "HSBA.L", "name": "HSBC Holdings", "country": "United Kingdom", "region": "Europe"},
    {"ticker": "9984.T", "name": "SoftBank Group", "country": "Japan", "region": "Asia"},
    {"ticker": "TCS.NS", "name": "Tata Consultancy", "country": "India", "region": "Asia"},
    {"ticker": "RELIANCE.NS", "name": "Reliance Ind.", "country": "India", "region": "Asia"},
    {"ticker": "BHP.AX", "name": "BHP Group", "country": "Australia", "region": "Other"},
    {"ticker": "005930.KS", "name": "Samsung Electronics", "country": "South Korea", "region": "Asia"},
]

# Supported Markets and Tickers
MARKETS = {
    "United States": [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM",
        "V", "JNJ", "WMT", "SPY", "QQQ", "DIA"
    ],
    "India": [
        "TCS.NS", "RELIANCE.NS", "INFY.NS", "HDFCBANK.NS",
        "WIPRO.NS", "ICICIBANK.NS"
    ],
    "United Kingdom": [
        "HSBA.L", "BP.L", "GSK.L", "AZN.L", "SHEL.L"
    ],
    "Germany": [
        "SAP.DE", "BMW.DE", "SIEMENS.DE", "VOW3.DE"
    ],
    "Japan": [
        "9984.T", "7203.T", "6758.T"
    ],
    "Australia": [
        "BHP.AX", "CBA.AX", "NAB.AX"
    ],
    "Canada": [
        "SHOP.TO", "RY.TO", "TD.TO"
    ],
    "Brazil": [
        "VALE3.SA", "PETR4.SA"
    ],
    "China": [
        "BABA", "JD", "PDD", "BIDU"
    ],
    "France": [
        "MC.PA", "TTE.PA", "SAN.PA"
    ]
}

# Major global benchmarks
BENCHMARKS = {
    "SPY": "S&P 500 ETF (SPY)",
    "QQQ": "NASDAQ 100 ETF (QQQ)",
    "IWM": "Russell 2000 ETF (IWM)",
    "EFA": "MSCI EAFE Dev Markets (EFA)",
    "EEM": "MSCI Emerging Markets (EEM)",
    "^GSPC": "S&P 500 Index (^GSPC)",
    "^DJI": "Dow Jones Industrial (^DJI)",
    "^IXIC": "NASDAQ Composite (^IXIC)"
}

# Key Index Annotations for Global World Map
WORLD_INDICES = [
    {"name": "USA", "index": "S&P 500", "ticker": "^GSPC", "lat": 38.0, "lon": -97.0},
    {"name": "UK", "index": "FTSE 100", "ticker": "^FTSE", "lat": 54.0, "lon": -2.0},
    {"name": "Germany", "index": "DAX", "ticker": "^GDAXI", "lat": 51.0, "lon": 10.0},
    {"name": "Japan", "index": "Nikkei 225", "ticker": "^N225", "lat": 36.0, "lon": 138.0},
    {"name": "India", "index": "NIFTY 50", "ticker": "^NSEI", "lat": 21.0, "lon": 78.0},
    {"name": "Brazil", "index": "IBOVESPA", "ticker": "^BVSP", "lat": -14.0, "lon": -51.0},
    {"name": "Australia", "index": "ASX 200", "ticker": "^AXJO", "lat": -25.0, "lon": 133.0},
    {"name": "Canada", "index": "S&P/TSX", "ticker": "^GSPTSE", "lat": 56.0, "lon": -106.0}
]

# Theme Colors
COLORS = {
    "bg_page": "#0a0e1a",
    "bg_sidebar": "#0d1117",
    "bg_card": "#111827",
    "bg_card_alt": "#161f2e",
    "border": "#1f2937",
    "border_accent": "#2d3748",
    "accent_green": "#22c55e",
    "accent_blue": "#3b82f6",
    "accent_violet": "#8b5cf6",
    "accent_cyan": "#06b6d4",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#4b5563",
    "text_label": "#64748b",
    "positive": "#22c55e",
    "negative": "#ef4444",
    "warning": "#f59e0b",
    "neutral": "#6b7280"
}
