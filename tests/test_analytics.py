import pytest
import pandas as pd
import numpy as np
from analytics import (
    calculate_daily_returns,
    calculate_cumulative_returns,
    calculate_annualized_volatility,
    calculate_drawdown_series,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
    calculate_beta
)

def test_daily_returns():
    prices = pd.Series([100.0, 105.0, 102.0, 110.0])
    returns = calculate_daily_returns(prices)
    assert len(returns) == 3
    assert pytest.approx(returns.iloc[0], 0.001) == 0.05
    assert pytest.approx(returns.iloc[1], 0.001) == -0.02857

def test_annualized_volatility():
    np.random.seed(42)
    daily_returns = pd.Series(np.random.normal(0, 0.01, 252))
    vol = calculate_annualized_volatility(daily_returns)
    assert vol > 0.0
    assert 0.05 < vol < 0.30

def test_max_drawdown():
    prices = pd.Series([100.0, 120.0, 90.0, 110.0])
    # Peak is 120, trough is 90 -> drawdown is (90 - 120) / 120 = -30 / 120 = -0.25 (-25%)
    mdd = calculate_max_drawdown(prices)
    assert pytest.approx(mdd, 0.001) == -0.25

def test_sharpe_ratio():
    returns = pd.Series([0.01, 0.02, 0.01, -0.005, 0.015] * 20)
    sr = calculate_sharpe_ratio(returns, risk_free_rate=0.0)
    assert sr > 0.0

def test_beta():
    # Asset moves exactly with market (needs len >= 10)
    market = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02] * 3)
    asset = market * 1.5
    b = calculate_beta(asset, market)
    assert b == pytest.approx(1.5, rel=0.01)
