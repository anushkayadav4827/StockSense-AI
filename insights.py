# -*- coding: utf-8 -*-
"""
Rule-based, evidence-grounded AI Market Insights generator for StockSense AI
Every insight directly references real calculated metrics.
"""

def generate_performance_insight(ticker: str, metrics: dict, period: str = "1Y") -> str:
    """Generate evidence-based performance summary text."""
    if not metrics:
        return f"Insufficient historical data available to evaluate {ticker}."

    tot_ret = metrics.get("total_return", 0.0) * 100.0
    ann_ret = metrics.get("ann_return", 0.0) * 100.0
    sharpe = metrics.get("sharpe_ratio", 0.0)

    perf_desc = "strong appreciation" if tot_ret > 20.0 else ("steady gains" if tot_ret > 5.0 else ("flat movement" if tot_ret > -5.0 else "underperformance"))
    sharpe_desc = "exceptional" if sharpe > 1.5 else ("favorable" if sharpe > 1.0 else ("moderate" if sharpe > 0.5 else "subdued"))
    ret_color = "#22c55e" if tot_ret >= 0 else "#ef4444"

    return (
        f"<strong>{ticker}</strong> has delivered a "
        f"<strong style='color:{ret_color}'>{tot_ret:+.2f}%</strong> return over the past {period} "
        f"(annualized pace of <strong>{ann_ret:+.2f}%</strong>), demonstrating {perf_desc}. "
        f"Risk-adjusted quality is {sharpe_desc} with a Sharpe ratio of <strong>{sharpe:.2f}</strong>."
    )


def generate_risk_insight(ticker: str, metrics: dict) -> str:
    """Generate risk assessment grounded in volatility, max drawdown, and beta."""
    if not metrics:
        return "Risk metrics are currently unavailable."

    vol = metrics.get("ann_vol", 0.0) * 100.0
    max_dd = metrics.get("max_drawdown", 0.0) * 100.0
    beta = metrics.get("beta", 1.0)

    vol_label = "low volatility" if vol < 20 else ("moderate volatility" if vol < 35 else "elevated volatility")
    beta_label = "defensive lower sensitivity" if beta < 0.85 else ("market-aligned correlation" if beta <= 1.2 else "higher systemic amplification")

    return (
        f"Annualized volatility is <strong>{vol:.2f}%</strong> ({vol_label}) with a historical peak-to-trough "
        f"maximum drawdown of <strong>{max_dd:.2f}%</strong>. The stock maintains a beta of <strong>{beta:.2f}</strong> "
        f"relative to the benchmark, indicating {beta_label} to broad market swings."
    )


def generate_observations(metrics: dict, fundamentals: dict = None) -> list:
    """Returns 3 evidence-grounded numbered observations."""
    obs = []
    if not metrics:
        return ["Awaiting metrics data."]

    sharpe = metrics.get("sharpe_ratio", 0.0)
    max_dd = metrics.get("max_drawdown", 0.0) * 100.0
    beta = metrics.get("beta", 1.0)
    pos_pct = metrics.get("pos_pct", 50.0)

    # Obs 1: Sharpe / Drawdown
    if sharpe > 1.0:
        obs.append(f"Strong risk-adjusted profile with a Sharpe of <strong>{sharpe:.2f}</strong>, indicating superior compensation per unit of risk.")
    elif sharpe > 0.5:
        obs.append(f"Fair risk-adjusted efficiency with a Sharpe ratio of <strong>{sharpe:.2f}</strong> over the evaluation window.")
    else:
        obs.append(f"Subdued risk compensation with a Sharpe ratio of <strong>{sharpe:.2f}</strong>, reflecting elevated downside exposure relative to returns.")

    # Obs 2: Drawdown resilience
    if max_dd > -15.0:
        obs.append(f"Resilient capital preservation with maximum drawdown contained within <strong>{max_dd:.2f}%</strong>.")
    elif max_dd > -30.0:
        obs.append(f"Moderate drawdown magnitude of <strong>{max_dd:.2f}%</strong>, requiring disciplined position sizing.")
    else:
        obs.append(f"Substantial cyclical drawdown of <strong>{max_dd:.2f}%</strong>, reflecting significant price volatility during sell-offs.")

    # Obs 3: Beta & win rate
    obs.append(f"Positive trading days occurred on <strong>{pos_pct:.1f}%</strong> of sessions, with a systemic beta of <strong>{beta:.2f}</strong> versus benchmark.")

    return obs[:3]


def generate_considerations(metrics: dict, fundamentals: dict = None) -> list:
    """Returns 2-3 risk warnings and things to consider."""
    items = []
    info = (fundamentals or {}).get("info", {}) if fundamentals else {}
    pe = info.get("trailingPE")

    if pe and pe > 0:
        items.append(f"Valuation multiple: Trailing P/E is <strong>{pe:.2f}x</strong>; monitor if future earnings expansion supports this valuation.")
    else:
        items.append("Valuation assessment: Ensure monitoring of macroeconomic and interest rate impacts on capital costs.")

    items.append("Sensitivity to broader sector momentum and quarterly earnings volatility.")
    items.append("Historical performance is indicative of past behavior and does not guarantee future results.")

    return items


def generate_comparison_takeaways(comparison_dict: dict) -> list:
    """
    Generate bullet points comparing multiple stocks.
    comparison_dict: {ticker: {"1y_return": float, "vol": float, "max_dd": float, "sharpe": float}}
    """
    if not comparison_dict:
        return ["Add stocks above to view comparative takeaways."]

    takeaways = []

    # Highest return
    best_ret_ticker = max(comparison_dict.keys(), key=lambda t: comparison_dict[t].get("1y_return", -999))
    best_ret = comparison_dict[best_ret_ticker].get("1y_return", 0.0) * 100.0
    takeaways.append(f"<strong>{best_ret_ticker}</strong> delivered the highest cumulative return (<strong>{best_ret:+.1f}%</strong>) across the observed window.")

    # Lowest volatility
    lowest_vol_ticker = min(comparison_dict.keys(), key=lambda t: comparison_dict[t].get("vol", 999))
    lowest_vol = comparison_dict[lowest_vol_ticker].get("vol", 0.0) * 100.0
    takeaways.append(f"<strong>{lowest_vol_ticker}</strong> exhibited the most defensive profile with lowest annualized volatility (<strong>{lowest_vol:.1f}%</strong>).")

    # Highest risk (max drawdown or highest vol)
    highest_risk_ticker = max(comparison_dict.keys(), key=lambda t: comparison_dict[t].get("vol", 0))
    highest_vol = comparison_dict[highest_risk_ticker].get("vol", 0.0) * 100.0
    takeaways.append(f"<strong>{highest_risk_ticker}</strong> registered the highest volatility (<strong>{highest_vol:.1f}%</strong>), requiring higher risk tolerance.")

    # Sharpe leader
    sharpe_leader = max(comparison_dict.keys(), key=lambda t: comparison_dict[t].get("sharpe", -999))
    sharpe_val = comparison_dict[sharpe_leader].get("sharpe", 0.0)
    takeaways.append(f"<strong>{sharpe_leader}</strong> demonstrated the strongest risk-adjusted return with a Sharpe ratio of <strong>{sharpe_val:.2f}</strong>.")

    return takeaways
