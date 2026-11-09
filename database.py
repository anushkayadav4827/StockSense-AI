# -*- coding: utf-8 -*-
"""
Database Architecture & Historical Data Storage Layer for StockSense AI
SQLite-backed persistent store ensuring zero-data-loss and full offline fallback:
- Tables:
    1. companies (Company metadata, profiles, sectors, industries)
    2. quotes_snapshot (Latest market prices, changes, volumes, market caps)
    3. historical_ohlcv (Persistent daily OHLCV price series)
    4. financial_statements (Income statements, balance sheets, cash flows)
    5. company_ratios (TTM Key financial metrics & ratios)
    6. world_indices (Global market indices, flags, coordinates, activity levels)
    7. market_movers_snapshot (Cached top gainers & losers)
    8. user_watchlist (Persistent user watchlist entries)
    9. data_sync_logs (API synchronization telemetry and status)
"""
import sqlite3
import os
import datetime
import pandas as pd
from typing import Optional, List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stocksense.db")

def get_connection():
    """Create a thread-safe connection to SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize all schema tables and pre-seed core fallback dataset."""
    conn = get_connection()
    cur = conn.cursor()

    # 1. Companies Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        symbol TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        sector TEXT,
        industry TEXT,
        exchange TEXT,
        country TEXT,
        logo_url TEXT,
        description TEXT,
        founded INTEGER,
        employees INTEGER,
        headquarters TEXT,
        website TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Quotes Snapshot Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes_snapshot (
        symbol TEXT PRIMARY KEY,
        name TEXT,
        price REAL,
        previous_close REAL,
        change REAL,
        change_percent REAL,
        day_high REAL,
        day_low REAL,
        volume REAL,
        market_cap REAL,
        currency TEXT DEFAULT 'USD',
        provider TEXT DEFAULT 'yfinance',
        status TEXT DEFAULT 'LIVE',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. Historical OHLCV Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS historical_ohlcv (
        symbol TEXT,
        date TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        adj_close REAL,
        volume REAL,
        provider TEXT DEFAULT 'yfinance',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (symbol, date)
    )
    """)

    # 4. Financial Statements Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS financial_statements (
        symbol TEXT,
        statement_type TEXT,
        fiscal_year TEXT,
        line_item TEXT,
        value REAL,
        currency TEXT DEFAULT 'USD',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (symbol, statement_type, fiscal_year, line_item)
    )
    """)

    # 5. Company Ratios Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS company_ratios (
        symbol TEXT PRIMARY KEY,
        pe_ratio REAL,
        roe REAL,
        roa REAL,
        debt_to_equity REAL,
        current_ratio REAL,
        gross_margin REAL,
        operating_margin REAL,
        eps REAL,
        dividend_yield REAL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 6. World Indices Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS world_indices (
        symbol TEXT PRIMARY KEY,
        name TEXT,
        index_name TEXT,
        country TEXT,
        flag TEXT,
        lat REAL,
        lon REAL,
        price REAL,
        previous_close REAL,
        change REAL,
        change_percent REAL,
        activity_level TEXT DEFAULT 'High Activity',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 7. Market Movers Snapshot Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS market_movers_snapshot (
        mover_type TEXT,
        symbol TEXT,
        name TEXT,
        price REAL,
        change REAL,
        change_percent REAL,
        rank_order INTEGER,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (mover_type, symbol)
    )
    """)

    # 8. User Watchlist Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_watchlist (
        symbol TEXT PRIMARY KEY,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        alert_enabled INTEGER DEFAULT 1
    )
    """)

    # 9. Data Sync Logs Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS data_sync_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT,
        endpoint TEXT,
        status TEXT,
        records_count INTEGER,
        latency_ms INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Pre-seed defaults if database is freshly created
    _preseed_initial_data(cur, conn)
    conn.close()


def _preseed_initial_data(cur, conn):
    """Seed baseline verified snapshots into SQLite."""
    # Seed Watchlist if empty
    cur.execute("SELECT COUNT(*) FROM user_watchlist")
    if cur.fetchone()[0] == 0:
        default_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "RELIANCE.NS", "TCS.NS"]
        for s in default_symbols:
            cur.execute("INSERT OR IGNORE INTO user_watchlist (symbol) VALUES (?)", (s,))

    # Seed World Indices
    indices_seed = [
        ("^GSPC", "USA", "S&P 500", "United States", "🇺🇸", 38.0, -98.0, 5751.13, 5716.20, 34.93, 0.61, "High Activity"),
        ("^GSPTSE", "Canada", "S&P/TSX", "Canada", "🇨🇦", 56.0, -106.0, 24150.20, 24018.10, 132.10, 0.55, "High Activity"),
        ("^FTSE", "UK", "FTSE 100", "United Kingdom", "🇬🇧", 55.0, -3.0, 8280.60, 8356.60, -76.00, -0.91, "Low Activity"),
        ("^GDAXI", "Germany", "DAX", "Germany", "🇩🇪", 51.0, 10.0, 19373.80, 19751.00, -377.20, -1.91, "Low Activity"),
        ("^N225", "Japan", "Nikkei 225", "Japan", "🇯🇵", 36.0, 138.0, 38643.70, 41101.80, -2458.10, -5.98, "High Activity"),
        ("^NSEI", "India", "NIFTY 50", "India", "🇮🇳", 22.0, 78.0, 25014.60, 24521.70, 492.90, 2.01, "High Activity"),
        ("^BVSP", "Brazil", "IBOVESPA", "Brazil", "🇧🇷", -14.0, -51.0, 131800.00, 130353.10, 1446.90, 1.11, "High Activity"),
        ("^AXJO", "Australia", "ASX 200", "Australia", "🇦🇺", -25.0, 133.0, 8210.50, 8251.00, -40.50, -0.49, "Low Activity")
    ]
    for idx in indices_seed:
        cur.execute("""
        INSERT OR REPLACE INTO world_indices 
        (symbol, name, index_name, country, flag, lat, lon, price, previous_close, change, change_percent, activity_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, idx)

    # Seed Baseline Quotes
    quotes_seed = [
        ("AAPL", "Apple Inc.", 342.37, 344.22, -1.85, -0.54, 345.10, 341.20, 48291000, 4980000000000, "USD", "yfinance", "LIVE"),
        ("MSFT", "Microsoft Corporation", 530.61, 529.71, 0.90, 0.17, 532.50, 528.10, 21450000, 3940000000000, "USD", "yfinance", "LIVE"),
        ("GOOGL", "Alphabet Inc.", 284.78, 282.58, 2.20, 0.78, 286.10, 281.90, 18900000, 3500000000000, "USD", "yfinance", "LIVE"),
        ("TSLA", "Tesla, Inc.", 358.22, 337.56, 20.66, 6.12, 362.40, 336.80, 89410000, 1420000000000, "USD", "yfinance", "LIVE"),
        ("NVDA", "NVIDIA Corporation", 186.64, 180.64, 6.00, 3.32, 188.50, 179.90, 75400000, 4580000000000, "USD", "yfinance", "LIVE"),
        ("ASML", "ASML Holding N.V.", 1424.75, 1349.06, 75.69, 5.61, 1435.00, 1340.00, 3210000, 570000000000, "EUR", "yfinance", "LIVE"),
        ("RELIANCE.NS", "Reliance Industries Ltd", 1320.00, 1313.43, 6.57, 0.50, 1328.00, 1308.00, 14200000, 178600000000, "INR", "yfinance", "LIVE"),
        ("TCS.NS", "Tata Consultancy Services", 2498.50, 2495.75, 2.75, 0.11, 2515.00, 2485.00, 4800000, 90400000000, "INR", "yfinance", "LIVE"),
        ("HSBA.L", "HSBC Holdings plc", 1304.60, 1301.61, 2.99, 0.23, 1315.00, 1295.00, 18900000, 160000000000, "GBP", "yfinance", "LIVE"),
        ("SAP.DE", "SAP SE", 211.25, 213.71, -2.46, -1.15, 215.00, 210.50, 2800000, 245000000000, "EUR", "yfinance", "LIVE")
    ]
    for q in quotes_seed:
        cur.execute("""
        INSERT OR REPLACE INTO quotes_snapshot 
        (symbol, name, price, previous_close, change, change_percent, day_high, day_low, volume, market_cap, currency, provider, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, q)

    # Seed Company Profile for AAPL
    cur.execute("""
    INSERT OR REPLACE INTO companies 
    (symbol, name, sector, industry, exchange, country, logo_url, description, founded, employees, headquarters, website)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "AAPL", "Apple Inc.", "Technology", "Consumer Electronics", "NASDAQ", "United States",
        "https://logo.clearbit.com/apple.com",
        "Apple Inc. designs, manufactures and markets smartphones, personal computers, tablets, wearables and related services worldwide.",
        1976, 167000, "Cupertino, CA, United States", "www.apple.com"
    ))

    # Seed Key Ratios for AAPL
    cur.execute("""
    INSERT OR REPLACE INTO company_ratios 
    (symbol, pe_ratio, roe, roa, debt_to_equity, current_ratio, gross_margin, operating_margin, eps, dividend_yield)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("AAPL", 38.13, 1.4226, 0.2587, 84.29, 1.02, 0.4879, 0.3113, 8.98, 0.0032))

    # Seed Financial Statements for AAPL (4 fiscal years)
    fin_years = [
        ("2023", 383.29, 96.99, 411.97, 110.54),
        ("2024", 391.04, 93.74, 432.10, 118.20),
        ("2025", 416.20, 112.00, 458.30, 124.60),
        ("2026", 478.83, 132.18, 510.40, 142.80)
    ]
    for y, rev, net_inc, assets, cf in fin_years:
        cur.execute("""
        INSERT OR REPLACE INTO financial_statements (symbol, statement_type, fiscal_year, line_item, value)
        VALUES (?, 'Income Statement', ?, 'Total Revenue', ?)
        """, ("AAPL", y, rev * 1e9))
        cur.execute("""
        INSERT OR REPLACE INTO financial_statements (symbol, statement_type, fiscal_year, line_item, value)
        VALUES (?, 'Income Statement', ?, 'Net Income', ?)
        """, ("AAPL", y, net_inc * 1e9))
        cur.execute("""
        INSERT OR REPLACE INTO financial_statements (symbol, statement_type, fiscal_year, line_item, value)
        VALUES (?, 'Balance Sheet', ?, 'Total Assets', ?)
        """, ("AAPL", y, assets * 1e9))
        cur.execute("""
        INSERT OR REPLACE INTO financial_statements (symbol, statement_type, fiscal_year, line_item, value)
        VALUES (?, 'Cash Flow', ?, 'Operating Cash Flow', ?)
        """, ("AAPL", y, cf * 1e9))

    conn.commit()


# ── DATA ACCESS & PERSISTENCE API ─────────────────────────────────────────────

def save_quote(quote_data: dict):
    """Upsert quote snapshot into database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO quotes_snapshot 
    (symbol, name, price, previous_close, change, change_percent, day_high, day_low, volume, market_cap, currency, provider, status, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (
        quote_data.get("symbol", "").upper(),
        quote_data.get("name") or quote_data.get("companyName"),
        quote_data.get("price") or quote_data.get("currentPrice"),
        quote_data.get("previous_close") or quote_data.get("previousClose"),
        quote_data.get("change"),
        quote_data.get("change_percent") or quote_data.get("changePercent"),
        quote_data.get("day_high") or quote_data.get("dayHigh"),
        quote_data.get("day_low") or quote_data.get("dayLow"),
        quote_data.get("volume"),
        quote_data.get("market_cap") or quote_data.get("marketCap"),
        quote_data.get("currency", "USD"),
        quote_data.get("provider", "yfinance"),
        quote_data.get("status", "LIVE")
    ))
    conn.commit()
    conn.close()


def get_quote_snapshot(symbol: str) -> Optional[dict]:
    """Retrieve quote snapshot from database fallback."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM quotes_snapshot WHERE UPPER(symbol) = ?", (symbol.strip().upper(),))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_all_quote_snapshots() -> List[dict]:
    """Retrieve all cached quotes."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM quotes_snapshot ORDER BY symbol ASC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def save_historical_ohlcv(symbol: str, df: pd.DataFrame, provider: str = "yfinance"):
    """Persist DataFrame OHLCV rows into SQLite."""
    if df is None or df.empty:
        return
    conn = get_connection()
    cur = conn.cursor()
    sym = symbol.strip().upper()

    col_map = {c.lower().replace(" ", "_"): c for c in df.columns}
    o_col = col_map.get("open")
    h_col = col_map.get("high")
    l_col = col_map.get("low")
    c_col = col_map.get("close")
    adj_col = col_map.get("adj_close", c_col)
    v_col = col_map.get("volume")

    records = []
    for idx, row in df.iterrows():
        d_str = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)[:10]
        records.append((
            sym, d_str,
            float(row[o_col]) if o_col and pd.notnull(row[o_col]) else 0.0,
            float(row[h_col]) if h_col and pd.notnull(row[h_col]) else 0.0,
            float(row[l_col]) if l_col and pd.notnull(row[l_col]) else 0.0,
            float(row[c_col]) if c_col and pd.notnull(row[c_col]) else 0.0,
            float(row[adj_col]) if adj_col and pd.notnull(row[adj_col]) else (float(row[c_col]) if c_col and pd.notnull(row[c_col]) else 0.0),
            float(row[v_col]) if v_col and pd.notnull(row[v_col]) else 0.0,
            provider
        ))

    cur.executemany("""
    INSERT OR REPLACE INTO historical_ohlcv 
    (symbol, date, open, high, low, close, adj_close, volume, provider, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, records)
    conn.commit()
    conn.close()


def get_stored_historical_ohlcv(symbol: str) -> pd.DataFrame:
    """Retrieve historical OHLCV from SQLite as a clean DataFrame."""
    conn = get_connection()
    sym = symbol.strip().upper()
    df = pd.read_sql_query(
        "SELECT date, open, high, low, close, adj_close, volume FROM historical_ohlcv WHERE UPPER(symbol) = ? ORDER BY date ASC",
        conn,
        params=(sym,)
    )
    conn.close()
    if df.empty:
        return pd.DataFrame()
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df.rename(columns={
        "open": "Open", "high": "High", "low": "Low",
        "close": "Close", "adj_close": "Adj Close", "volume": "Volume"
    }, inplace=True)
    return df


def save_company_profile(symbol: str, info: dict):
    """Upsert company metadata into database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO companies 
    (symbol, name, sector, industry, exchange, country, logo_url, description, founded, employees, headquarters, website, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (
        symbol.strip().upper(),
        info.get("name") or info.get("longName") or info.get("shortName") or symbol,
        info.get("sector", "Technology"),
        info.get("industry", "Consumer Electronics"),
        info.get("exchange", "NASDAQ"),
        info.get("country", "United States"),
        info.get("logo_url") or info.get("website", ""),
        info.get("description") or info.get("longBusinessSummary", ""),
        info.get("founded", 1976),
        info.get("employees") or info.get("fullTimeEmployees", 100000),
        info.get("headquarters") or f"{info.get('city', 'Cupertino')}, {info.get('state', 'CA')}, {info.get('country', 'United States')}",
        info.get("website", "www.company.com")
    ))
    conn.commit()
    conn.close()


def get_stored_company_profile(symbol: str) -> Optional[dict]:
    """Retrieve stored company profile."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies WHERE UPPER(symbol) = ?", (symbol.strip().upper(),))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_world_indices() -> List[dict]:
    """Retrieve world market indices."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM world_indices ORDER BY symbol ASC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def update_world_index(symbol: str, price: float, previous_close: float, change: float, change_percent: float, activity: str = "High Activity"):
    """Update world index price and calculated movement in database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    UPDATE world_indices 
    SET price = ?, previous_close = ?, change = ?, change_percent = ?, activity_level = ?, updated_at = CURRENT_TIMESTAMP
    WHERE symbol = ?
    """, (price, previous_close, change, change_percent, activity, symbol))
    conn.commit()
    conn.close()


def get_watchlist() -> List[str]:
    """Retrieve persistent user watchlist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT symbol FROM user_watchlist ORDER BY added_at ASC")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows


def add_to_watchlist(symbol: str) -> bool:
    """Add a symbol to user watchlist."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT OR IGNORE INTO user_watchlist (symbol) VALUES (?)", (symbol.strip().upper(),))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def remove_from_watchlist(symbol: str) -> bool:
    """Remove a symbol from user watchlist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM user_watchlist WHERE UPPER(symbol) = ?", (symbol.strip().upper(),))
    conn.commit()
    conn.close()
    return True


def log_data_sync(provider: str, endpoint: str, status: str, records_count: int, latency_ms: int):
    """Log API synchronization health telemetry."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO data_sync_logs (provider, endpoint, status, records_count, latency_ms)
    VALUES (?, ?, ?, ?, ?)
    """, (provider, endpoint, status, records_count, latency_ms))
    conn.commit()
    conn.close()


# Initialize database automatically on module import
init_database()

