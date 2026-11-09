# StockSense AI — Global Market Intelligence & Quantitative Risk Analytics

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?logo=plotly&logoColor=white)
![Groq AI](https://img.shields.io/badge/Groq_AI-LLaMA_3.3_--_70B-F55036?logo=groq&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite_v3-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-11%2F11%20Passing-16a34a?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**An institutional-grade financial intelligence and quantitative risk dashboard bridging deep statistical modeling, live multi-exchange market feeds, and high-speed LLM analytical inference.**

[Features](#-core-platform-modules) • [Architecture](#-system-architecture) • [Data Pipeline](#-data-pipeline--quantitative-methodology) • [Quick Start](#-installation--quick-start) • [Testing](#-testing--quality-assurance)

</div>

---

## 📌 Executive Overview

**StockSense AI** is an advanced, production-grade market intelligence platform engineered for financial analysts, quantitative researchers, and active investors. By combining real-time streaming market data, historical econometric time-series analysis, statistical risk modeling, and evidence-grounded AI synthesis, StockSense AI delivers a Bloomberg-terminal caliber experience through an intuitive, editorial interface.

The platform strictly enforces a **Zero-Synthetic Data Policy**: every metric, ratio, chart, and correlation displayed across its 10 views originates from verified live API feeds or validated historical local snapshot databases.

---

## 🏛️ System Architecture

StockSense AI follows a modular, decoupled architecture where data ingestion, mathematical computation, persistent caching, AI inference, and UI rendering operate as independent, resilient layers.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER (UI)                           │
│  Streamlit 1.40+ • Custom CSS Engine (styles.py) • Inter Typography         │
│  Interactive Plotly Visualizations • Dynamic GeoJSON World Map • 3D Globe   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                            ROUTING & VIEW MODULES                           │
│  Global Overview  │  Stock Explorer  │  Risk Analytics  │  Stock Comparison │
│  Fundamentals     │  AI Analyst      │  Watchlist       │  Data Quality     │
│  Datasets/Export  │  Settings        │                                      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                    ANALYTICS & AI INTELLIGENCE ENGINE                       │
│  analytics.py (Volatility, Drawdown, Sharpe, Beta, VaR, Calmar)             │
│  llm_analyst.py (Groq API • LLaMA 3.3 70B • Grounded Financial Briefs)      │
│  insights.py (Rule-Based Anomaly & Trend Detection)                         │
└──────────────────┬───────────────────────────────────────┬──────────────────┘
                   │                                       │
┌──────────────────┴──────────────────┐ ┌──────────────────┴──────────────────┐
│   DATA CLEANING & VALIDATION PIPELINE│ │      STORAGE & PERSISTENCE LAYER     │
│  data_cleaning.py                   │ │  stocksense.db (SQLite Snapshot Cache)│
│  • OHLCV Integrity & Gap Imputation │ │  • In-Memory TTL Cache (@st.cache_data│
│  • Corporate Action Adjustment      │ │  • Historical Price & Meta Persistence│
│  • Outlier Rejection & Normalization│ │  • Zero Unhandled Failover Log        │
└──────────────────┬──────────────────┘ └──────────────────┬──────────────────┘
                   │                                       │
┌──────────────────┴───────────────────────────────────────┴──────────────────┐
│                      CENTRALIZED DATA INGESTION ENGINE                      │
│  data_provider.py • market_service.py                                       │
│  ├── Primary Stream: Twelve Data API (Real-time intraday & quotes)          │
│  ├── Secondary Failover: Yahoo Finance (yfinance historical OHLCV & SEC)    │
│  └── Tertiary Stream: MarketStack API (Global cross-exchange coverage)      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Core Platform Modules

### 1. 🌐 Global Overview & Macro Intelligence
- **Geospatial Market Map**: Interactive, pan-and-zoom world map built on a Natural Earth Robinson projection with dynamic country performance pins (US, CA, BR, UK, DE, IN, JP, AU) indicating live activity status.
- **Top-Right 3D Globe**: Custom rotating Earth visualization accented with a soft emerald aura.
- **Frosted Glass KPI Cards**: 4 responsive summary metrics displaying active tracked markets, 25,430+ global equities, major indices, and real-time feed latency.
- **Market Movers Panel**: Instant tab switching between **Top Gainers** and **Top Losers** with real-time price changes, badges, and percentage spreads.
- **Intelligent Omnibar**: Unified ticker and company autocomplete search bar with direct routing to deep analysis.

### 2. 🔍 Stock Explorer & Technical Charting
- **Dual Subplot OHLCV Charts**: High-performance interactive Candlestick and Price Area subplots coupled with a color-coded volume histogram.
- **Multi-Period Range Selectors**: Flexible timeframe pills (`1D`, `5D`, `1M`, `3M`, `6M`, `1Y`, `5Y`, `MAX`) with dynamic aggregation intervals.
- **Key Metric Badges**: Live indicators including Open, High, Low, Previous Close, Volume, Market Capitalization, Trailing P/E, 52-Week High, and 52-Week Low.

### 3. 📉 Quantitative Risk Analytics
- **Risk KPI Matrix**: Annualized Volatility ($\sigma$), Maximum Historical Drawdown, Sharpe Ratio, and Benchmark Beta ($\beta$ vs. SPY/S&P 500) paired with automated risk classification pills.
- **Drawdown Analysis**: High-resolution underwater equity curve charting portfolio drawdowns over time with dynamic red area fill.
- **Return Distribution Histogram**: Daily logarithmic return frequency distribution overlaid with an empirical mean benchmark line and color-coded tail risk bins.
- **30-Day Rolling Volatility**: Dynamic trend line tracking annualized 30-day window standard deviations.
- **Parametric Risk Table**: Quantitative breakdown including Best/Worst Daily Return, Positive/Negative Session Ratio, Current Drawdown, and Calmar Ratio.

### 4. ⚖️ Multi-Asset Stock Comparison
- **Normalized Cumulative Returns**: Multi-line normalized performance chart indexed to a common base ($T_0 = 0\%$) for direct cross-asset alpha comparison.
- **Cross-Asset Correlation Matrix**: Quantitative Heatmap displaying Pearson correlation coefficients across daily return series.
- **Comparative Metrics Table**: Side-by-side benchmarking of current price, period return, volatility, max drawdown, and Sharpe efficiency.
- **Quantitative Takeaways**: Automated bulleted synthesis summarizing performance leaders, risk-adjusted standouts, and diversification benefits.

### 5. 🏢 Company Fundamentals & SEC Financials
- **Company Profile**: Vector brand insignia, executive summary, sector, industry, founding date, employee count, global headquarters, and official web portals.
- **TTM Financials Grid**: 6 high-impact KPI tiles detailing Market Cap, Total Revenue, Net Income, Trailing EPS, P/E Ratio, and Dividend Yield.
- **Historical Revenue & Net Income Bar Chart**: Dual-grouped annual bar visualization (`#054F3F` forest emerald and `#34D399` mint green) with direct billion-dollar callouts.
- **Key Financial Ratios**: DuPont breakdown (ROE, ROA), Capital Structure (Debt-to-Equity), Liquidity (Current Ratio), and Margins (Gross & Operating).
- **Tabbed Statements**: Comprehensive drilldown into formal SEC Income Statements, Balance Sheets, and Cash Flow tables.

### 6. 🤖 Evidence-Grounded AI Market Analyst
- **LLM Engine**: Powered by Groq-accelerated inference utilizing ultra-low latency models (`llama-3.3-70b-versatile` / `openai/gpt-oss-120b`).
- **Grounded Financial Prompting**: AI generation strictly bound to empirical quantitative outputs computed by the local engine (zero hallucination of stock prices or ratios).
- **Structured Intelligence Briefs**:
  - Executive Performance Summary
  - Asymmetric Downside Risk Evaluation
  - Key Quantitative Observations (Alpha drivers, session distributions)
  - Macro Considerations & Horizon Analysis

### 7. ⭐ Watchlist & Live Tracking
- **Multi-Asset Monitoring**: Add, remove, and track personalized equity portfolios.
- **Real-Time Spread Table**: Price, 1D%, 1W%, 1M%, 1Y%, Market Cap, and alerts.
- **Inline SVG Sparklines**: Ultra-lightweight inline 30-day micro trend charts (no Plotly overhead) color-coded to positive/negative trajectory.

### 8. 🛡️ Data Quality & Source Integrity
- **Feed Health Monitor**: Live connection state to Twelve Data, yfinance, and local SQLite snapshot caches.
- **Audit Metrics**: Total processed records, duplicate detection counters, null-value tallies, and completeness ratios.
- **Gap & Anomaly Breakdown**: Interactive bar chart tracking missing values per field.
- **Validation Checklist**: Real-time pass/fail indicators covering trading calendar alignment, extreme outlier boundaries, and split integrity.

### 9. 📁 Datasets & Export
- **Catalog Browser**: Search, preview, and inspect available historical market datasets and index constituents.
- **Custom CSV Exporter**: Download cleaned, normalized OHLCV time-series directly for offline modeling in Excel, R, or Python.

### 10. ⚙️ Settings & Configuration
- **Risk-Free Rate ($\mathbf{R_f}$)**: Adjustable treasury baseline (default: 4.5% annual).
- **Benchmark Reference**: Configurable regression asset (SPY, QQQ, DIA, IWM, NIFTY50).
- **API Credentials Vault**: Secure management and testing for Twelve Data, MarketStack, and Groq keys.
- **Cache Controller**: One-click in-memory TTL cache eviction and local database re-sync.

---

## 🧮 Data Pipeline & Quantitative Methodology

### 1. Data Hygiene & Cleaning Pipeline (`data_cleaning.py`)
All raw incoming feeds pass through a deterministic four-stage sanitization pipeline prior to analysis:
1. **Datetime Index Normalization**: All timestamps are converted to UTC, aligned to standard market exchange calendars, and stripped of timezone offsets.
2. **Missing Value Imputation**: Forward-fill (`ffill`) followed by backward-fill (`bfill`) preserves continuous price series across market halts without introducing forward-looking bias.
3. **Outlier Filtering**: Statistical detection flags non-market single-tick spikes ($> \pm 50\%$ anomalous jumps unconfirmed by volume).
4. **Volume Floor Enforcement**: Negative or corrupted zero-volume days on non-holiday sessions are audited and corrected.

### 2. Mathematical Formulations (`analytics.py`)

| Metric | Mathematical Formula | Description |
| :--- | :--- | :--- |
| **Daily Returns** | $R_t = \frac{P_t - P_{t-1}}{P_{t-1}}$ | Percentage change of consecutive closing prices |
| **Annualized Volatility** | $\sigma_{\text{ann}} = \sqrt{252} \cdot \sqrt{\frac{1}{N-1} \sum_{t=1}^N (R_t - \bar{R})^2}$ | Standard deviation scaled by standard 252 annual trading sessions |
| **Maximum Drawdown (MDD)** | $\text{MDD} = \min_{t} \left( \frac{P_t - \max_{s \le t} P_s}{\max_{s \le t} P_s} \right)$ | Peak-to-trough decline over the selected timeframe |
| **Sharpe Ratio** | $\text{Sharpe} = \frac{R_p - R_f}{\sigma_{\text{ann}}}$ | Risk-adjusted excess return over annualized risk-free rate ($R_f$) |
| **Sortino Ratio** | $\text{Sortino} = \frac{R_p - R_f}{\sigma_{\text{downstream}}}$ | Risk-adjusted return penalizing downside volatility only |
| **Beta Coefficient ($\mathbf{\beta}$)** | $\beta = \frac{\text{Cov}(R_i, R_m)}{\text{Var}(R_m)}$ | Systematic sensitivity of stock $i$ relative to benchmark $m$ |
| **Calmar Ratio** | $\text{Calmar} = \frac{R_{\text{cagr}}}{|\text{MDD}|}$ | Ratio of compounded annual growth rate to maximum drawdown |

---

## 📂 Project Directory Structure

```text
Stocksense/
├── app.py                           # Application entry point & URL routing
├── config.py                        # Global constants, ticker universe, and defaults
├── styles.py                        # Unified CSS design system & component rules
├── components.py                    # Reusable HTML/SVG component builders
├── visualizations.py                # Plotly charting engine (OHLCV, Drawdown, Heatmap)
├── analytics.py                     # Quantitative risk & econometric formulas
├── data_provider.py                 # Multi-provider financial data ingestion engine
├── data_cleaning.py                 # Data hygiene, imputation, and validation pipeline
├── market_service.py                # Centralized market caching & quote aggregation
├── database.py                      # SQLite historical snapshot store (stocksense.db)
├── llm_analyst.py                   # Groq LLM integration for grounded AI briefs
├── insights.py                      # Rule-based quantitative insight generation
├── requirements.txt                 # Pinned project dependencies
├── README.md                        # Documentation & architecture manual
│
├── views/                           # Modular dashboard page controllers
│   ├── __init__.py                  # View namespace exports
│   ├── global_overview.py           # World map, 3D globe, and market movers
│   ├── stock_explorer.py            # Candlestick chart and technical overview
│   ├── risk_analytics.py            # Drawdown, distribution, volatility, and beta
│   ├── stock_comparison.py          # Multi-asset normalized returns and correlations
│   ├── company_fundamentals.py      # SEC financial statements and TTM ratios
│   ├── ai_analyst.py                # Groq-powered evidence-based AI reports
│   ├── watchlist.py                 # Custom ticker monitor with SVG sparklines
│   ├── data_quality.py              # Data hygiene metrics and audit checks
│   ├── datasets.py                  # Dataset catalog and CSV download manager
│   └── settings.py                  # API keys, risk-free rate, and model config
│
├── tests/                           # Automated unit & integration test suite
│   ├── test_analytics.py            # Quantitative math verification (Sharpe, Beta, MDD)
│   ├── test_cleaning.py             # Data imputation and sanity tests
│   ├── test_data_provider.py        # Feed failover and quote normalizer tests
│   └── test_fundamentals.py         # Financial statement parsing tests
│
└── scratch/                         # Development & automated CDP visual validation scripts
```

---

## 🚀 Installation & Quick Start

### 1. Prerequisites
- Python **3.11** or higher
- Git

### 2. Clone Repository & Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/your-username/stocksense-ai.git
cd stocksense-ai

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables *(Optional)*
StockSense AI works out-of-the-box using built-in public market data and failover endpoints. To enable high-speed AI analysis or expanded intraday feeds, create a `.env` file in the root directory:

```env
# Groq Cloud API Key for AI Market Analyst (Free tier available at console.groq.com)
GROQ_API_KEY=gsk_your_groq_api_key_here

# Twelve Data API Key for real-time intraday quotes
TWELVE_DATA_API_KEY=your_twelve_data_api_key_here

# MarketStack API Key (Optional tertiary feed)
MARKETSTACK_API_KEY=your_marketstack_api_key_here
```
*(Keys can also be configured directly via the in-app **Settings** page at runtime).*

### 5. Launch Application
```bash
streamlit run app.py
```
Open your browser to: **`http://localhost:8501`**

---

## 🧪 Testing & Quality Assurance

StockSense AI includes an automated test suite verifying quantitative algorithms, data sanitization, provider failover, and ratio calculations:

```bash
# Execute full test suite
python -m pytest tests/ -v
```

### Test Coverage Highlights:
- **`tests/test_analytics.py`**: Verifies exact mathematical precision for Annualized Volatility, Sharpe Ratio, Sortino Ratio, Beta, and Maximum Drawdown against standard benchmarks.
- **`tests/test_cleaning.py`**: Asserts that timestamp gaps are imputed, corporate action anomalies are handled, and DataFrame shapes remain consistent.
- **`tests/test_data_provider.py`**: Validates failover logic, caching TTL expiry, and response schema normalization.
- **`tests/test_fundamentals.py`**: Tests SEC filing parsers, TTM metric aggregators, and billion/trillion currency formatting.

---

## 🔒 Security & Best Practices

- **Zero API Key Exposure**: All sensitive credentials can be loaded via local environment variables or managed securely inside ephemeral session state.
- **Local SQLite Caching**: Eliminates redundant external API calls, respecting rate limits and ensuring fast sub-second rendering.
- **No Third-Party Tracking**: StockSense AI operates as a self-contained local analytical application without external telemetries or tracking scripts.

---