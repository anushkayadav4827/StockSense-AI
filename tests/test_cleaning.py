import pytest
import pandas as pd
import numpy as np
from data_cleaning import clean_price_data

def test_clean_price_data_basic():
    dates = pd.date_range("2025-01-01", periods=5)
    df = pd.DataFrame({
        "Open": [100, 102, 101, 103, 104],
        "High": [105, 106, 104, 107, 108],
        "Low": [99, 101, 98, 102, 103],
        "Close": [103, 104, 102, 106, 107],
        "Volume": [1000, 1500, 1200, 1800, 2000]
    }, index=dates)

    cleaned_df, report = clean_price_data(df)
    assert not cleaned_df.empty
    assert "adj_close" in cleaned_df.columns
    assert report["source_rows"] == 5
    assert report["valid_rows"] == 5
    assert report["invalid_ohlc"] == 0

def test_clean_price_data_invalid_ohlc():
    dates = pd.date_range("2025-01-01", periods=3)
    # Row 1 has High < Low
    df = pd.DataFrame({
        "Open": [100, 102, 101],
        "High": [95, 106, 104],  # High < Low
        "Low": [99, 101, 98],
        "Close": [103, 104, 102],
        "Volume": [1000, 1500, 1200]
    }, index=dates)

    cleaned_df, report = clean_price_data(df)
    assert report["invalid_ohlc"] == 1
