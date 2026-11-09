# -*- coding: utf-8 -*-
"""
Tests for Company Fundamentals mapping, data retrieval, and chart generation.
"""
import pytest
import pandas as pd
from data_provider import fetch_fundamentals, fetch_fast_info
from visualizations import create_financials_combo_chart

def test_fetch_fundamentals_structure():
    funds = fetch_fundamentals("AAPL")
    assert isinstance(funds, dict)
    assert "info" in funds
    assert "financials" in funds
    assert "balance_sheet" in funds
    assert "cashflow" in funds

def test_fetch_fast_info_structure():
    fast = fetch_fast_info("AAPL")
    assert isinstance(fast, dict)
    assert "price" in fast
    assert "pct_change" in fast
    assert fast["price"] > 0

def test_create_financials_combo_chart():
    # Test with empty dataframe (fallback test)
    fig_empty = create_financials_combo_chart(pd.DataFrame(), height=295)
    assert fig_empty is not None
    assert len(fig_empty.data) == 2  # Revenue and Net Income traces
    assert fig_empty.layout.height == 295

    # Test with mock financials dataframe
    mock_df = pd.DataFrame(
        {
            "2025-09-30": [400e9, 100e9],
            "2024-09-30": [350e9, 90e9],
            "2023-09-30": [300e9, 80e9],
        },
        index=["Total Revenue", "Net Income"]
    )
    fig_mock = create_financials_combo_chart(mock_df, height=300)
    assert len(fig_mock.data) == 2
    assert fig_mock.layout.height == 300

