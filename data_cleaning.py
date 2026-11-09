# -*- coding: utf-8 -*-
"""
Data validation, cleaning, and quality analysis pipeline for StockSense AI
"""
import pandas as pd
import numpy as np

def clean_price_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Standardize, clean, and validate raw price OHLCV data.
    Returns: (cleaned_df, quality_report)
    """
    if df is None or df.empty:
        return pd.DataFrame(), {
            "source_rows": 0, "valid_rows": 0, "duplicates": 0,
            "invalid_ohlc": 0, "outliers": 0, "missing_ohlc": 0, "missing_volume": 0
        }

    cleaned = df.copy()
    source_rows = len(cleaned)

    # 1. Normalize column names to standard lowercase with underscore
    col_map = {}
    for col in cleaned.columns:
        clean_col = str(col).strip().lower().replace(" ", "_")
        col_map[col] = clean_col
    cleaned.rename(columns=col_map, inplace=True)

    # Ensure standard OHLCV names exist
    # Mapping variants
    standard_names = {
        "open": "open", "high": "high", "low": "low", "close": "close",
        "adj_close": "adj_close", "volume": "volume"
    }

    # Ensure index is datetime and sorted
    if not isinstance(cleaned.index, pd.DatetimeIndex):
        cleaned.index = pd.to_datetime(cleaned.index, errors='coerce')
    cleaned = cleaned[cleaned.index.notnull()]
    cleaned = cleaned.sort_index()

    # 2. Drop duplicates
    dups = cleaned.index.duplicated(keep="last")
    duplicates_count = int(dups.sum())
    cleaned = cleaned[~dups]

    # 3. Ensure adj_close column exists (use close if missing)
    if "adj_close" not in cleaned.columns:
        if "close" in cleaned.columns:
            cleaned["adj_close"] = cleaned["close"]
        else:
            cleaned["adj_close"] = np.nan

    # 4. Validate OHLC structure
    invalid_ohlc = 0
    if all(c in cleaned.columns for c in ["open", "high", "low", "close"]):
        # Check high < low or price <= 0
        invalid_mask = (cleaned["high"] < cleaned["low"]) | \
                       (cleaned["open"] <= 0) | (cleaned["high"] <= 0) | \
                       (cleaned["low"] <= 0) | (cleaned["close"] <= 0)
        invalid_ohlc = int(invalid_mask.sum())
        # Filter or clean invalid records
        cleaned = cleaned[~invalid_mask]

    # 5. Outlier detection on returns (|z-score| > 5)
    outliers = 0
    if "adj_close" in cleaned.columns and len(cleaned) > 10:
        ret = np.log(cleaned["adj_close"] / cleaned["adj_close"].shift(1))
        ret_mean = ret.mean()
        ret_std = ret.std()
        if ret_std and not np.isnan(ret_std) and ret_std > 0:
            z_scores = np.abs((ret - ret_mean) / ret_std)
            outliers = int((z_scores > 5.0).sum())

    # 6. Missing value handling (forward fill max 1 session)
    missing_ohlc = int(cleaned[["open", "high", "low", "close"]].isna().sum().sum()) if all(c in cleaned.columns for c in ["open", "high", "low", "close"]) else 0
    missing_volume = int(cleaned["volume"].isna().sum()) if "volume" in cleaned.columns else 0

    cleaned = cleaned.ffill(limit=1).bfill(limit=1)

    valid_rows = len(cleaned)

    quality_report = {
        "source_rows": source_rows,
        "valid_rows": valid_rows,
        "duplicates": duplicates_count,
        "invalid_ohlc": invalid_ohlc,
        "outliers": outliers,
        "missing_ohlc": missing_ohlc,
        "missing_volume": missing_volume
    }

    return cleaned, quality_report


def validate_dataset(df: pd.DataFrame) -> dict:
    """
    Run specific integrity checks for Data Quality view.
    """
    if df is None or df.empty:
        return {
            "no_negative_prices": False,
            "no_duplicate_dates": False,
            "valid_ohlc_structure": False,
            "date_sequence_verified": False,
            "total_records": 0,
            "valid_records": 0,
            "duplicate_count": 0,
            "missing_count": 0,
            "start_date": "N/A",
            "end_date": "N/A",
            "trading_days": 0
        }

    cols = [c.lower() for c in df.columns]
    price_cols = [c for c in cols if c in ["open", "high", "low", "close", "adj close", "adj_close"]]

    # Check negative prices
    neg_prices = False
    for pc in price_cols:
        col_actual = [c for c in df.columns if c.lower() == pc][0]
        if (df[col_actual] < 0).any():
            neg_prices = True
            break
    no_negative_prices = not neg_prices

    # Check duplicates
    duplicate_dates = df.index.duplicated().any()
    no_duplicate_dates = not duplicate_dates

    # Check OHLC structure
    valid_ohlc = True
    c_map = {c.lower(): c for c in df.columns}
    if "high" in c_map and "low" in c_map:
        if (df[c_map["high"]] < df[c_map["low"]]).any():
            valid_ohlc = False

    # Check sequence
    is_monotonic = df.index.is_monotonic_increasing

    start_date = df.index.min().strftime("%b %d, %Y") if hasattr(df.index.min(), 'strftime') else str(df.index.min())
    end_date = df.index.max().strftime("%b %d, %Y") if hasattr(df.index.max(), 'strftime') else str(df.index.max())

    total_records = len(df)
    missing_count = int(df.isna().sum().sum())
    duplicate_count = int(df.index.duplicated().sum())

    return {
        "no_negative_prices": no_negative_prices,
        "no_duplicate_dates": no_duplicate_dates,
        "valid_ohlc_structure": valid_ohlc,
        "date_sequence_verified": is_monotonic,
        "total_records": total_records,
        "valid_records": total_records - missing_count - duplicate_count,
        "duplicate_count": duplicate_count,
        "missing_count": missing_count,
        "start_date": start_date,
        "end_date": end_date,
        "trading_days": len(df)
    }
