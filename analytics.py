# -*- coding: utf-8 -*-
"""
Financial and risk metrics analytics engine for StockSense AI
"""
import numpy as np
import pandas as pd
from config import TRADING_DAYS_PER_YEAR, DEFAULT_RISK_FREE_RATE

def calculate_daily_returns(series: pd.Series) -> pd.Series:
    """Daily simple return: r_t = (P_t / P_{t-1}) - 1"""
    return series.pct_change().dropna()


def calculate_cumulative_returns(series: pd.Series) -> pd.Series:
    """Cumulative return: cum_r = (1 + r).cumprod() - 1"""
    r = calculate_daily_returns(series)
    return (1.0 + r).cumprod() - 1.0


def calculate_annualized_volatility(returns: pd.Series, periods: int = TRADING_DAYS_PER_YEAR) -> float:
    """Annualized volatility: vol = std(r) * sqrt(252)"""
    if returns.empty or len(returns) < 2:
        return 0.0
    return float(returns.std() * np.sqrt(periods))


def calculate_drawdown_series(price_series: pd.Series) -> pd.Series:
    """
    Compute drawdown series:
    peak = cummax()
    drawdown = (price - peak) / peak
    """
    if price_series.empty:
        return pd.Series(dtype=float)
    peak = price_series.cummax()
    return (price_series - peak) / peak


def calculate_max_drawdown(price_series: pd.Series) -> float:
    """Max drawdown = min(drawdown)"""
    dd = calculate_drawdown_series(price_series)
    if dd.empty:
        return 0.0
    return float(dd.min())


def calculate_current_drawdown(price_series: pd.Series) -> float:
    """Current drawdown = drawdown of the most recent observation"""
    dd = calculate_drawdown_series(price_series)
    if dd.empty:
        return 0.0
    return float(dd.iloc[-1])


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = DEFAULT_RISK_FREE_RATE, periods: int = TRADING_DAYS_PER_YEAR) -> float:
    """
    Sharpe ratio:
    excess = r - (rf / 252)
    sharpe = mean(excess) / std(excess) * sqrt(252)
    """
    if returns.empty or len(returns) < 2:
        return 0.0
    daily_rf = risk_free_rate / periods
    excess = returns - daily_rf
    std = excess.std()
    if std == 0 or np.isnan(std):
        return 0.0
    return float((excess.mean() / std) * np.sqrt(periods))


def calculate_sortino_ratio(returns: pd.Series, risk_free_rate: float = DEFAULT_RISK_FREE_RATE, periods: int = TRADING_DAYS_PER_YEAR) -> float:
    """
    Sortino ratio:
    downside = std(r[r < 0]) * sqrt(252)
    sortino = (mean(r) * 252 - rf) / downside
    """
    if returns.empty:
        return 0.0
    downside_returns = returns[returns < 0]
    if downside_returns.empty:
        return 0.0
    downside_vol = downside_returns.std() * np.sqrt(periods)
    if downside_vol == 0 or np.isnan(downside_vol):
        return 0.0
    ann_return = returns.mean() * periods
    return float((ann_return - risk_free_rate) / downside_vol)


def calculate_beta(stock_returns: pd.Series, benchmark_returns: pd.Series) -> float:
    """
    Beta vs Benchmark (OLS method on aligned returns):
    beta = cov(stock, benchmark) / var(benchmark)
    """
    if stock_returns.empty or benchmark_returns.empty:
        return 1.0
    aligned = pd.concat([stock_returns, benchmark_returns], axis=1, join="inner").dropna()
    if len(aligned) < 10:
        return 1.0
    s_ret = aligned.iloc[:, 0]
    b_ret = aligned.iloc[:, 1]
    var_b = b_ret.var()
    if var_b == 0 or np.isnan(var_b):
        return 1.0
    cov = s_ret.cov(b_ret)
    return float(cov / var_b)


def calculate_calmar_ratio(annualized_return: float, max_drawdown: float) -> float:
    """Calmar ratio = annualized_return / abs(max_drawdown)"""
    if abs(max_drawdown) < 1e-6:
        return 0.0
    return float(annualized_return / abs(max_drawdown))


def calculate_rolling_volatility(returns: pd.Series, window: int = 21, periods: int = TRADING_DAYS_PER_YEAR) -> pd.Series:
    """Rolling annualized volatility: returns.rolling(window).std() * sqrt(252)"""
    return (returns.rolling(window).std() * np.sqrt(periods)).dropna()


def calculate_all_metrics(df: pd.DataFrame, benchmark_df: pd.DataFrame = None, risk_free_rate: float = DEFAULT_RISK_FREE_RATE) -> dict:
    """
    Compute comprehensive metrics package for a stock.
    """
    if df is None or df.empty:
        return {}

    # Locate close / adj_close series
    price_col = "adj_close" if "adj_close" in df.columns else ("Adj Close" if "Adj Close" in df.columns else "Close")
    prices = df[price_col].dropna()
    if prices.empty:
        return {}

    returns = calculate_daily_returns(prices)
    if returns.empty:
        return {}

    total_return = float((prices.iloc[-1] / prices.iloc[0]) - 1.0)
    n_days = len(prices)
    ann_return = float((1.0 + total_return) ** (TRADING_DAYS_PER_YEAR / max(n_days, 1)) - 1.0) if total_return > -1.0 else -1.0

    ann_vol = calculate_annualized_volatility(returns)
    dd_series = calculate_drawdown_series(prices)
    max_dd = calculate_max_drawdown(prices)
    curr_dd = calculate_current_drawdown(prices)
    sharpe = calculate_sharpe_ratio(returns, risk_free_rate=risk_free_rate)
    sortino = calculate_sortino_ratio(returns, risk_free_rate=risk_free_rate)
    calmar = calculate_calmar_ratio(ann_return, max_dd)

    # Beta
    beta = 1.0
    if benchmark_df is not None and not benchmark_df.empty:
        b_col = "adj_close" if "adj_close" in benchmark_df.columns else ("Adj Close" if "Adj Close" in benchmark_df.columns else "Close")
        b_prices = benchmark_df[b_col].dropna()
        b_returns = calculate_daily_returns(b_prices)
        beta = calculate_beta(returns, b_returns)

    pos_days = int((returns > 0).sum())
    neg_days = int((returns < 0).sum())
    total_days = len(returns)
    pos_pct = (pos_days / total_days * 100.0) if total_days > 0 else 0.0
    neg_pct = (neg_days / total_days * 100.0) if total_days > 0 else 0.0

    best_day = float(returns.max()) if not returns.empty else 0.0
    worst_day = float(returns.min()) if not returns.empty else 0.0

    return {
        "prices": prices,
        "returns": returns,
        "drawdown_series": dd_series,
        "total_return": total_return,
        "ann_return": ann_return,
        "ann_vol": ann_vol,
        "max_drawdown": max_dd,
        "curr_drawdown": curr_dd,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "beta": beta,
        "calmar_ratio": calmar,
        "best_day": best_day,
        "worst_day": worst_day,
        "pos_days": pos_days,
        "neg_days": neg_days,
        "pos_pct": pos_pct,
        "neg_pct": neg_pct,
        "total_sessions": total_days,
        "start_date": prices.index[0],
        "end_date": prices.index[-1]
    }
