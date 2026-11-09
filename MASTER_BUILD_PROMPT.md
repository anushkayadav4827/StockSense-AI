# STOCKSENSE AI — MASTER BUILD PROMPT v3.0
# Global Stock Market Intelligence & Risk Analytics Dashboard
# Build from scratch. No legacy code. Production quality only.

═══════════════════════════════════════════════════════════════
ROLE
═══════════════════════════════════════════════════════════════

You are a senior fintech engineer, quantitative analyst, and 
premium UI/UX designer. Build a complete, working, polished 
stock market analytics dashboard named StockSense AI.

This is NOT a mockup. NOT a demo with fake data. 
Every number must come from real, live market data.
Every chart must be interactive. Every page must be functional.

Work fully autonomously. Inspect → Build → Run → Fix → Verify.
Never stop to ask. Never explain without doing. Build first.

═══════════════════════════════════════════════════════════════
SECTION 1 — WHAT THIS PRODUCT IS
═══════════════════════════════════════════════════════════════

StockSense AI is a web dashboard for traders and investors to:
  • Explore global stock markets across 10+ countries
  • Analyze historical price, return, and volume data
  • Measure and understand risk (volatility, drawdown, beta)
  • Compare multiple stocks and benchmarks side-by-side
  • Read AI-generated insights grounded in real calculations
  • Monitor a personal watchlist with live prices
  • Inspect company fundamentals and financial ratios
  • Assess data quality and source transparency

═══════════════════════════════════════════════════════════════
SECTION 2 — TECH STACK
═══════════════════════════════════════════════════════════════

Framework:     Streamlit (latest)
Language:      Python 3.11+
Data:          yfinance (primary — free, unlimited, no key needed)
               pandas-datareader (secondary/fallback)
Charts:        Plotly (ALL charts — no matplotlib, no st.line_chart)
Calculations:  pandas, numpy, scipy
Styling:       Full custom CSS injected via st.markdown()
               Inter font from Google Fonts
               NO Streamlit default styling anywhere visible
Testing:       pytest
Caching:       st.cache_data with TTL

File structure:
  app.py                  ← entry point, routing only
  styles.py               ← complete CSS string (MAIN_CSS)
  components.py           ← reusable HTML/SVG component builders
  data_provider.py        ← yfinance wrapper, caching, error handling
  data_cleaning.py        ← validation, normalization pipeline
  analytics.py            ← all financial metric calculations
  insights.py             ← rule-based AI insight generator
  visualizations.py       ← all Plotly figure builders
  config.py               ← tickers, markets, constants
  pages/
    global_overview.py
    stock_explorer.py
    risk_analytics.py
    stock_comparison.py
    company_fundamentals.py
    ai_analyst.py
    watchlist.py
    data_quality.py
    datasets.py
    settings.py
  tests/
    test_analytics.py
    test_cleaning.py
    test_data_provider.py
  requirements.txt
  .env.example
  README.md

═══════════════════════════════════════════════════════════════
SECTION 3 — DESIGN SYSTEM (implement exactly, zero deviation)
═══════════════════════════════════════════════════════════════

── COLORS ──────────────────────────────────────────────────

  Background page:     #0a0e1a
  Background sidebar:  #0d1117
  Background card:     #111827
  Background card alt: #161f2e
  Border:              #1f2937
  Border accent:       #2d3748

  Accent green:        #22c55e   ← logo, active nav, positive
  Accent blue:         #3b82f6   ← primary charts, buttons
  Accent violet:       #8b5cf6   ← secondary highlights
  Accent cyan:         #06b6d4   ← tertiary data

  Text primary:        #f1f5f9
  Text secondary:      #94a3b8
  Text muted:          #4b5563
  Text label:          #64748b

  Positive return:     #22c55e
  Negative return:     #ef4444
  Warning:             #f59e0b
  Neutral:             #6b7280

── TYPOGRAPHY ──────────────────────────────────────────────

  Import: @import url('https://fonts.googleapis.com/css2?
           family=Inter:wght@300;400;500;600;700;800&display=swap');
  
  Base font: Inter, -apple-system, sans-serif
  
  Page H1:         700, 1.75rem, #f1f5f9, letter-spacing -0.02em
  Page H2:         600, 1.25rem, #f1f5f9
  Section label:   500, 0.65rem, #64748b, letter-spacing 0.12em, 
                   UPPERCASE
  Metric value:    700, 2rem, #f1f5f9
  Metric label:    400, 0.72rem, #94a3b8, uppercase, letter-spacing 0.08em
  Body text:       400, 0.875rem, #94a3b8, line-height 1.6
  Table cell:      400, 0.8rem, #e2e8f0
  Badge text:      600, 0.7rem

── SPACING ─────────────────────────────────────────────────

  Page padding:        0 2rem 2rem 2rem
  Card padding:        20px 24px
  Card border-radius:  12px
  Card gap:            16px
  Section gap:         32px
  Metric grid gap:     12px

── CARDS ───────────────────────────────────────────────────

  background:     #111827
  border:         1px solid #1f2937
  border-radius:  12px
  padding:        20px 24px
  
  Hover state:    border-color: #3b82f6, 
                  box-shadow: 0 0 0 1px rgba(59,130,246,0.3)
  
  Metric card specific:
    Min-width: 160px
    Value size: 2rem, 700 weight
    Change badge: inline-block, border-radius 4px, 
                  padding 2px 8px, font-size 0.72rem
    Positive badge: background #052e16, color #22c55e
    Negative badge: background #2d0a0a, color #ef4444

── SIDEBAR ─────────────────────────────────────────────────

  Width: 220px, fixed
  Background: #0d1117
  Border-right: 1px solid #1f2937
  
  Logo block:
    "StockSense AI" — Inter 700, 1rem, #f1f5f9
    "Global Market Intelligence" — Inter 500, 0.65rem, #22c55e
    Green circle icon (●) before logo text
  
  Nav section label:
    "NAVIGATION" — 0.6rem, #4b5563, uppercase, letter-spacing 0.15em
    margin-bottom: 8px, margin-top: 20px
  
  Nav button (each page):
    width: 100%, text-align: left
    padding: 8px 12px
    border-radius: 8px
    font: Inter 400 0.85rem #94a3b8
    border: none, background: transparent
    cursor: pointer
    
    ACTIVE state:
      background: #161f2e
      color: #f1f5f9
      border-left: 3px solid #22c55e
      font-weight: 500
    
    HOVER state:
      background: #111827
      color: #e2e8f0
  
  Controls below nav (MARKET, TICKER, DATE RANGE, BENCHMARK, COMPARE):
    Label: 0.65rem uppercase #64748b, margin-bottom 4px
    Input/select: dark bg #111827, border #1f2937, 
                  color #f1f5f9, border-radius 8px
  
  Bottom status bar:
    Provider name — green dot — "OK"
    "Last fetch: HH:MM:SS"
    font-size: 0.7rem, color: #4b5563

── CHARTS (all Plotly) ─────────────────────────────────────

  paper_bgcolor = 'rgba(0,0,0,0)'
  plot_bgcolor  = '#0d1117'
  font = dict(family='Inter', color='#94a3b8', size=11)
  
  Gridlines:   color='#1f2937', width=1
  Axes:        color='#1f2937', tickcolor='#4b5563', linecolor='#1f2937'
  Hover:       bgcolor='#1e2d45', bordercolor='#3b82f6', 
               font color='#f1f5f9'
  Legend:      bgcolor='rgba(0,0,0,0)', font color='#94a3b8'
  Margin:      l=50, r=20, t=30, b=40
  
  Line colors by series order:
    Primary:    #3b82f6 (blue)
    Secondary:  #22c55e (green)
    Tertiary:   #f59e0b (amber)
    Quaternary: #8b5cf6 (violet)
    Fifth:      #06b6d4 (cyan)
  
  Candlestick:
    Increasing: fillcolor='#22c55e', line color='#22c55e'
    Decreasing: fillcolor='#ef4444', line color='#ef4444'
  
  Area/fill charts:
    Positive area: rgba(34,197,94,0.15)
    Negative area: rgba(239,68,68,0.15)
  
  Volume bars: positive=#1d4428, negative=#3d1515

── GLOBAL CSS OVERRIDES ────────────────────────────────────

Inject this via st.markdown at the very top of app.py:

  /* Hide Streamlit branding */
  #MainMenu, footer, header {visibility: hidden;}
  
  /* Page background */
  .stApp { background: #0a0e1a; }
  .block-container { padding: 0 2rem 2rem 2rem; max-width: 100%; }
  
  /* Remove all default white/grey backgrounds */
  .stApp > div, [data-testid="stAppViewContainer"] { background: #0a0e1a; }
  
  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1f2937;
  }
  
  /* All buttons */
  .stButton > button {
    background: #111827; color: #94a3b8;
    border: 1px solid #1f2937; border-radius: 8px;
    font-family: Inter; font-size: 0.85rem;
  }
  
  /* Selectbox, text input */
  .stSelectbox > div > div,
  .stTextInput > div > div > input {
    background: #111827 !important;
    color: #f1f5f9 !important;
    border-color: #1f2937 !important;
    border-radius: 8px !important;
  }
  
  /* Dataframe */
  .stDataFrame { background: #111827; }
  .stDataFrame table { color: #e2e8f0; }
  .stDataFrame th { background: #161f2e; color: #94a3b8; }
  .stDataFrame td { border-color: #1f2937; }
  
  /* Expander */
  .streamlit-expanderHeader {
    background: #111827; color: #94a3b8;
    border: 1px solid #1f2937; border-radius: 8px;
  }
  
  /* Tabs (only used inside pages, not for main nav) */
  .stTabs [data-baseweb="tab-list"] { background: #0d1117; gap: 4px; }
  .stTabs [data-baseweb="tab"] {
    background: transparent; color: #64748b;
    border-radius: 6px; font-size: 0.8rem;
    padding: 6px 14px;
  }
  .stTabs [aria-selected="true"] {
    background: #161f2e; color: #f1f5f9;
    border-bottom: 2px solid #3b82f6;
  }
  
  /* Scrollbar */
  ::-webkit-scrollbar { width: 4px; height: 4px; }
  ::-webkit-scrollbar-track { background: #0a0e1a; }
  ::-webkit-scrollbar-thumb { background: #1f2937; border-radius: 4px; }

═══════════════════════════════════════════════════════════════
SECTION 4 — DATA PIPELINE
═══════════════════════════════════════════════════════════════

PRIMARY SOURCE: yfinance
  pip install yfinance — free, no API key, unlimited requests

DATA FETCHING RULES:
  1. @st.cache_data(ttl=3600) on all price history functions
  2. @st.cache_data(ttl=7200) on all .info / fundamentals functions
  3. Always wrap in try/except — never crash the app on bad ticker
  4. On error: show styled error card, never blank screen
  5. Default ticker: AAPL (always load on app start)
  6. Preload market movers list on Global Overview page load

MARKET MOVERS — fetch these 12 on startup:
  US:       AAPL, MSFT, NVDA, TSLA
  Europe:   ASML (Netherlands), SAP.DE (Germany), HSBA.L (UK)
  Asia:     9984.T (Japan/SoftBank), TCS.NS, RELIANCE.NS (India)
  Other:    BHP.AX (Australia), 005930.KS (Samsung/Korea)

DEFAULT TICKER LIST per market (configurable in config.py):
  United States:  AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META, JPM,
                  V, JNJ, WMT, SPY, QQQ, DIA
  India:          TCS.NS, RELIANCE.NS, INFY.NS, HDFCBANK.NS, 
                  WIPRO.NS, ICICIBANK.NS, NIFTY50=F
  UK:             HSBA.L, BP.L, GSK.L, AZN.L, SHEL.L
  Germany:        SAP.DE, BMW.DE, SIEMENS.DE, VOW3.DE
  Japan:          9984.T, 7203.T, 6758.T
  Australia:      BHP.AX, CBA.AX, NAB.AX
  Canada:         SHOP.TO, RY.TO, TD.TO
  Brazil:         VALE3.SA, PETR4.SA
  China:          BABA, JD, PDD, BIDU
  France:         MC.PA, TTE.PA, SAN.PA

BENCHMARKS available:
  SPY  (S&P 500 ETF)
  QQQ  (NASDAQ 100 ETF)
  IWM  (Russell 2000)
  EFA  (International developed)
  EEM  (Emerging markets)
  ^GSPC (S&P 500 Index)
  ^DJI  (Dow Jones)
  ^IXIC (NASDAQ)

FINANCIAL CALCULATIONS (in analytics.py):
  
  Daily simple return:
    r_t = (adj_close_t / adj_close_{t-1}) - 1
  
  Cumulative return:
    cum_r = (1 + r).cumprod() - 1
  
  Annualized volatility:
    vol = r.std() * sqrt(252)   ← always state 252 trading days
  
  Max drawdown:
    peak = adj_close.cummax()
    drawdown = (adj_close - peak) / peak
    max_dd = drawdown.min()
  
  Sharpe ratio:
    excess = r - (risk_free_rate / 252)
    sharpe = excess.mean() / excess.std() * sqrt(252)
    risk_free_rate = 0.045 (configurable in config.py)
  
  Sortino ratio:
    downside = r[r < 0].std() * sqrt(252)
    sortino = (r.mean() * 252 - risk_free_rate) / downside
  
  Beta:
    cov = aligned_stock_r.cov(benchmark_r)
    var = benchmark_r.var()
    beta = cov / var
    (use 252-session aligned window, OLS method)
  
  Calmar ratio:
    calmar = (annualized_return) / abs(max_drawdown)
  
  Rolling volatility:
    r.rolling(21).std() * sqrt(252)   ← 21-day window
    r.rolling(63).std() * sqrt(252)   ← 63-day window

DATA CLEANING (in data_cleaning.py):
  1. Normalize column names to lowercase with underscores
  2. Parse dates, sort chronologically, set as index
  3. Drop exact duplicate (date, symbol) pairs
  4. Flag rows where high < low or any OHLC price <= 0
  5. Flag outliers: |z-score of log returns| > 5 (review, don't delete)
  6. Handle NaN: forward-fill max 1 day (weekends), else mark missing
  7. Verify adj_close exists; use close as fallback with note
  8. Track: source_rows, valid_rows, duplicates, invalid_ohlc, 
            outliers, missing_ohlc, missing_volume
  9. Preserve raw downloaded data; work on cleaned copy

═══════════════════════════════════════════════════════════════
SECTION 5 — PAGE SPECIFICATIONS (build all 9)
═══════════════════════════════════════════════════════════════
![alt text](image.png)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 1: GLOBAL OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HEADER SECTION:
  Left: 
    H1: "StockSense AI"
    Subtitle: "Global Market Intelligence & Risk Analytics"
    Body: "Explore global markets, analyze performance, compare 
           stocks and get AI-powered insights."
    Search bar: full-width, placeholder "Search for a company 
                or ticker (e.g. AAPL, TSLA, NIFTY, TCS...)"
    On search submit → navigate to Stock Explorer with that ticker
  
  Right:
    3 stat boxes in a row:
      Box 1: star icon + "7" large + "Global Markets" label + 
             "+1 today" green badge
      Box 2: building icon + "25,430+" large + 
             "Tracked Companies" + "Across 50+ countries"
      Box 3: chart icon + "12" large + "Major Indexes" + 
             "S&P 500, NIFTY, FTSE..."
    Live badge: green pulsing dot + "Live" + "Market Data" + 
                "Via Twelve Data" (or yfinance)

GLOBAL MARKET PERFORMANCE section:
  
  Left side — World Map (Plotly choropleth):
    Countries with data: colored green-ish (#1a3a2a)
    Selected country: bright green (#22c55e)
    No data: dark (#111827)
    Country labels with index name + 1-day % change floated 
    on top of key countries (USA, UK, Germany, Japan, India, 
    Brazil, Australia) using go.Scattergeo annotations:
      Format: "USA\nS&P 500\n+0.61%"
      Color text by positive/negative
    Map style: 'natural earth', dark ocean (#0a0e1a), 
               land (#111827), border (#1f2937)
    No colorbar. Clean, minimal.
  
  Right side — Market Movers panel:
    Title: "Market Movers"
    Two tabs: [Top Gainers] [Top Losers]
    Table rows (5 per tab):
      Ticker | Company short name | Price | Change %
      Change % colored green/red with arrow ↑↓
    "View more →" link at bottom
    
    Data: fetch the 12 market movers list, sort by 1D change,
          top 5 = gainers, bottom 5 = losers (by 1D %)
    
    1D change = (current - prev_close) / prev_close * 100
    Use yfinance Ticker.fast_info for speed

FOOTER of this page:
  "StockSense AI v3.0.0 · yfinance · Historical analysis only 
   · Not financial advice"
  Data provider status pill

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 2: STOCK EXPLORER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PAGE HEADER:
  Left: Company logo (Clearbit: https://logo.clearbit.com/{domain})
        If Clearbit fails, show colored circle with first letter.
        Domain from yfinance info["website"]. Strip https://www.
  
  Company name H1 (e.g. "AAPL") large
  Full name below (e.g. "Apple Inc.")
  Breadcrumb: Exchange · Country · Sector in #94a3b8
  
  Right (aligned right):
    Price: $178.32 in 2.2rem 700 white
    Change: +2.14 (+1.21%) in green/red
    "As of Oct 1, 2026" in muted text
    
    Two buttons: [+ Add to Watchlist] [Compare ↗]

TIME PERIOD TABS:
  [1D] [5D] [1M] [3M] [6M] [1Y] [3Y] [5Y] [Max]
  Active tab: white text, bottom border #3b82f6
  Map to yfinance period strings: 1d, 5d, 1mo, 3mo, 6mo, 
                                   1y, 3y, 5y, max

MAIN CHART:
  Default: Candlestick + Volume subplot
  Chart tabs above it: [OHLCV + Volume] [Line] [Cumulative Return]
  
  Candlestick: green/red as defined in design system
  Volume subplot: height_ratio 3:1, bars colored by day direction
  
  Hover tooltip: Date, O, H, L, C, Volume, % change from prev
  Rangeslider: enabled, small, dark styled

STAT GRID below chart (2×4 grid):
  Open | High | Low | Prev Close
  Volume | Market Cap | P/E Ratio | 52W High
  
  Each cell: label top (#94a3b8, 0.7rem), value bottom (#f1f5f9, 1rem 600)
  Volume formatted with M/B abbreviation
  Market Cap: from yfinance info["marketCap"]
  52W High/Low: from yfinance info["fiftyTwoWeekHigh/Low"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 3: RISK ANALYTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PAGE HEADER: same as Stock Explorer (logo + price + time tabs)

METRIC CARDS ROW (4 cards):
  
  Card 1 — Annualized Volatility:
    Value: XX.XX%
    Label below in colored badge: 
      <20% = "Low Risk" (green)
      20-35% = "Moderate" (amber)  
      >35% = "High Risk" (red)
  
  Card 2 — Maximum Drawdown:
    Value: -XX.XX% in red
    Label: "Moderate Risk" / "High Risk" / "Low Risk"
  
  Card 3 — Sharpe Ratio:
    Value: X.XX
    Label: >1.5="Excellent" (green), 1-1.5="Good" (green),
           0.5-1="Fair" (amber), <0.5="Poor" (red)
    Info icon (ℹ) tooltip: "Risk-adjusted return. Higher = better."
  
  Card 4 — Beta vs S&P 500:
    Value: X.XX in blue or amber
    Label: <0.8="Defensive" (green), 0.8-1.2="Market-like" (blue),
           >1.2="Aggressive" (amber/red) + "(Slightly Higher Risk)"

CHARTS ROW 1 (two columns, equal width):
  
  Left — Drawdown Analysis:
    Title: "Drawdown Analysis"
    Plotly area chart, x=date, y=drawdown %
    Fill color: rgba(239,68,68,0.2) (red transparent)
    Line: #ef4444
    Y axis: formatted as %, reversed (0 at top)
    Horizontal line at 0% (dashed, #1f2937)
  
  Right — Return Distribution:
    Title: "Return Distribution"
    Histogram of daily returns
    Bins: 50
    Negative bars: #ef4444, Positive bars: #22c55e
    Vertical line at mean: dashed blue, labeled "Mean: X.XX%"
    X axis: percentage format

CHART ROW 2 (full width):
  Rolling Volatility (30-day):
    Two lines: 21-day (#3b82f6) and 63-day (#8b5cf6)
    Legend shown
    Y axis: percentage format
    Title: "Rolling Annualized Volatility"

RISK METRICS TABLE (right column alongside rolling vol):
  Two-column layout: metric name | value
  Rows:
    Best Daily Return    | +X.XX% (green)
    Worst Daily Return   | -X.XX% (red)
    Positive Days        | XXX (XX.X%)
    Negative Days        | XXX (XX.X%)
    Current Drawdown     | -X.XX% (red)
    Calmar Ratio         | X.XX

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 4: STOCK COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TICKER CHIPS HEADER:
  Selected tickers shown as dismissible chips:
    [AAPL ×] [MSFT ×] [GOOGL ×] [TSLA ×] [+ Add]
  Chip style: background #161f2e, border #3b82f6, 
              color #f1f5f9, border-radius 20px,
              padding 4px 12px, font 0.8rem
  ×  button: color #94a3b8, hover #ef4444
  Max 5 tickers. If 5 reached, disable + Add.
  Company name shown under ticker in chip in 0.65rem

TIME TABS: [3M] [6M] [1Y] [3Y] [5Y] — same style

NORMALIZED RETURNS CHART (full width):
  Title: "Normalized Returns"
  Y axis: "Cumulative Return (%) — Base = 0%"
  Each ticker = one line, color from series palette
  Legend: ticker + company name + current return %
    e.g. "AAPL  +18.4%"
  Starts at 0% for all tickers on selected start date

PERFORMANCE COMPARISON TABLE:
  Columns: Stock (colored circle + ticker) | Price | 1Y Return | 
           Annualized Vol | Max Drawdown | Sharpe Ratio
  
  Return cells: colored green/red
  Drawdown: red
  Sharpe: colored by threshold
  Sort by 1Y Return descending by default
  
  Show "Common window: YYYY-MM-DD to YYYY-MM-DD (NNN sessions)" 
  above table in muted text

CORRELATION MATRIX (left, square):
  Heatmap: colorscale from #ef4444 (−1) → #111827 (0) → #3b82f6 (+1)
  Show correlation value in each cell
  Diagonal = 1.00 always
  Title: "Correlation Matrix (Daily Returns)"

KEY TAKEAWAYS (right of matrix):
  Auto-generated text block from insights.py:
  Format:
    "• GOOGL delivered the highest 1Y return (32.7%)."
    "• AAPL and MSFT show more stable performance."
    "• TSLA has the highest volatility and drawdown."
    "• AAPL, MSFT and GOOGL are moderately correlated."
  Rules-based, not LLM. References actual calculated numbers.
  Each bullet in a styled card row.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 5: COMPANY FUNDAMENTALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TABS: [Overview] [Fundamentals] [Financial Statements] 
      [Key Ratios] [Dividends]

TAB 1 — OVERVIEW:
  Top row: company logo + name + price + change (same as Explorer)
  
  Three columns:
    Col 1 — Company Profile:
      Sector, Industry, Founded (if available), 
      Employees (formatted: 164,000), 
      Headquarters (from info["city"] + info["country"]),
      Website (clickable blue link)
    
    Col 2 — Key Financials (TTM):
      Market Cap, Revenue, Net Income, EPS,
      P/E Ratio, Dividend Yield
      Each as label → value pair, clean grid
    
    Col 3 — Key Ratios:
      ROE, ROA, Debt-to-Equity, Current Ratio,
      Gross Margin, Operating Margin
      Format as percentages where applicable
  
  Revenue & Net Income chart (bar + line combo):
    Bars: Revenue by year (blue)
    Line: Net Income by year (green)
    Use yfinance financials DataFrame
    X: last 4 fiscal years
    Dual Y axis if scales differ greatly
  
  Note: "Source: yfinance · US equities have best coverage"

TAB 2 — FINANCIALS STATEMENTS: 
  Show yfinance .financials, .balance_sheet, .cashflow
  as styled st.dataframe tables
  Format numbers in millions with "M" / billions with "B"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 6: AI MARKET ANALYST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HEADER:
  Robot icon (🤖 or SVG) + "AI Market Analyst" h2
  Subtitle: "Evidence-based insights from historical data 
             and financial metrics. Not financial advice."
  
  Info banner: "Every insight is derived from calculated 
                historical metrics — not generative AI. 
                Each claim references a specific number."

TABS: [All Insights] [Trend Analysis] [Risk Summary] 
      [Comparison Insights] [Key Takeaways]

TAB 1 — ALL INSIGHTS (two columns):
  
  Left column:
    
    Card — "📈 Overall Performance":
      Auto-text: "{TICKER} has delivered a {return}% return 
                 over the past {period}, outperforming / 
                 underperforming its sector average of {X}%."
      (Sector comparison: skip if unavailable, don't invent)
    
    Card — "⚠️ Risk Analysis":
      Auto-text using: volatility, max drawdown, beta, 
                       drawdown label, Sharpe
      Reference exact numbers. Explain what each means briefly.
    
    Card — "🔍 Key Observations" (numbered list, 3 items):
      Generated rules from insights.py:
        - If Sharpe > 1: "Strong risk-adjusted return..."
        - If max_dd < -20%: "Significant drawdown observed..."
        - If beta > 1.2: "Higher market sensitivity..."
        - Compare to benchmark if available
        - Price momentum observation
      Each observation: 2 sentences max, one number cited.
    
  Right column:
    
    Card — "💡 Things to Consider" (numbered list, 2-3 items):
      Always include caveats:
        - P/E vs sector if data available
        - Upcoming earnings note (from yfinance .calendar if available)
        - "Historical performance does not guarantee future returns."
      
    Card — "📊 Period Statistics":
      Quick stats table:
        Period: {start} to {end}
        Sessions: {N} trading days
        Best Month: {month} ({return}%)
        Worst Month: {month} ({return}%)
        Avg Monthly Return: {X}%

NEVER generate: price predictions, buy/sell ratings, 
                earnings forecasts, news events, 
                analyst ratings — unless from verified data source.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 7: WATCHLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HEADER:
  "My Watchlist" h2
  "Track your favorite stocks and monitor their performance."
  [+ Add Stock] button (primary, blue, top right)

DEFAULT WATCHLIST: AAPL, MSFT, GOOGL, TSLA, RELIANCE.NS, TCS.NS
(stored in st.session_state["watchlist"])

ADD STOCK FLOW:
  When "+ Add Stock" clicked → show text input for ticker
  Validate via yfinance (must return valid data)
  On success: add to session_state list and refresh table
  On fail: show "Ticker not found" error in red

TABLE COLUMNS:
  1. Stock: company logo (small 24px) + ticker (bold) + full name
  2. 1D %: colored +/-
  3. 3D %: colored +/-
  4. 1W %: colored +/-
  5. 1M %: colored +/-
  6. 1Y %: colored +/-
  7. Market Cap: formatted (2.78T / 394B)
  8. Trend: 30-day sparkline (inline SVG — see components.py)
  9. Actions: 🔔 bell icon | 🗑 delete icon

Sparkline: 30-day adj_close, normalize to 0-1 range,
           draw as 80×30px SVG polyline,
           color: green if +, red if -,
           no axes, no labels

Remove: clicking delete removes from session_state
Clicking any row: navigate to Stock Explorer with that ticker
Sort by: 1Y return descending by default

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 8: DATA QUALITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HEADER:
  "Data Quality & Source Information" h2
  "Overview of data integrity, last updates and API status."
  Provider badge: green dot + "yfinance" + "Connected"
  Last checked timestamp (right-aligned)

STAT STRIP (4 cards):
  Total Records | Valid Records | Duplicate Records | Missing Values
  Show absolute number + small % change indicator

CHARTS ROW:
  Left — Missing Values by Column:
    Horizontal bar chart
    Y axis: column names (Open, High, Low, Close, Volume, Adj Close)
    X axis: count of missing values
    Bar color: #ef4444 if > 0, #22c55e if 0
  
  Right — Date Coverage:
    Timeline bar showing start → end date
    "Jan 1, 2010 ←————————————→ Oct 1, 2026"
    "Total: 4,212 trading days"
    Progress bar styled green

DATA VALIDATION CHECKLIST:
  Four items with green ✓ or red ✗:
    ✓ No negative prices
    ✓ No duplicate dates  
    ✓ Valid OHLC structure
    ✓ Date sequence verified
  Run these checks live from data_cleaning.py

RAW DATA PREVIEW:
  Expandable section: "Raw Cleaned Data (first 100 rows)"
  Styled st.dataframe

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 9: DATASETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TABS: [Browse Datasets] [Upload Dataset] [My Datasets] 
      [Sample Datasets]

TAB 1 — BROWSE DATASETS:
  Search bar + Region dropdown + Format dropdown (CSV/JSON/All)
  
  Table: Name | Description | Category | Region | Format | Actions
  
  Pre-populated rows (these are real downloadable yfinance outputs):
    Global Stock Price Data | Daily OHLCV for 500+ tickers | 
      Prices | Global | CSV | [Download]
    Major Market Indices | S&P500, NIFTY50, DAX, FTSE | 
      Indices | Global | CSV | [Download]
    Sector Performance | 11 US sectors via ETFs (XLK, XLF...) | 
      Sector | US | CSV | [Download]
    Currency Exchange Rates | USD/EUR/GBP/JPY/INR via yfinance | 
      FX | Global | CSV | [Download]
    Volatility Index | VIX historical data | 
      Risk | US | CSV | [Download]
    Emerging Markets | EEM component country ETFs | 
      EM | Global | CSV | [Download]
  
  [Download] buttons trigger actual CSV export via:
    df = yf.download(ticker, period="5y")
    st.download_button(data=df.to_csv(), file_name=f"{ticker}_5y.csv")

TAB 2 — UPLOAD DATASET:
  st.file_uploader for CSV
  Auto-detect: symbol column, date column, price columns
  On upload: run through data_cleaning.py pipeline
  Show validation results
  Add to session_state["uploaded_datasets"]

═══════════════════════════════════════════════════════════════
SECTION 6 — COMPONENTS.PY — build these helpers
═══════════════════════════════════════════════════════════════

def metric_card(label, value, change=None, change_pct=None, 
                subtitle=None, color=None) -> str:
  """Returns HTML string for a metric card with styled value,
     optional change badge, optional subtitle label."""

def section_header(text) -> str:
  """Returns HTML for uppercase muted section label."""

def badge(text, sentiment) -> str:
  """sentiment: 'positive'|'negative'|'neutral'|'warning'
     Returns styled inline badge HTML."""

def stock_chip(ticker, name, removable=True) -> str:
  """Returns styled ticker chip HTML for comparison page."""

def sparkline_svg(prices: list, width=80, height=30) -> str:
  """Returns inline SVG sparkline. 
     Normalize prices to fit height. 
     Color: green if last > first, red otherwise."""

def stat_grid(stats: dict, columns=4) -> str:
  """Returns HTML grid of label:value pairs for 
     the OHLCV stat section in Stock Explorer."""

def validation_row(label, passed: bool) -> str:
  """Returns styled ✓ / ✗ row for Data Quality page."""

def provider_badge(provider, status) -> str:
  """Returns green/red dot + provider name pill."""

═══════════════════════════════════════════════════════════════
SECTION 7 — ROUTING & NAVIGATION
═══════════════════════════════════════════════════════════════

Navigation state: st.session_state["page"] (string)
Default page: "Global Overview"

Sidebar nav items (in order):
  Global Overview, Stock Explorer, Risk Analytics, 
  Stock Comparison, Company Fundamentals, AI Market Analyst,
  Watchlist, Datasets, Data Quality, Settings

When nav item clicked:
  st.session_state["page"] = page_name
  st.rerun()

Global state keys:
  st.session_state["ticker"]       ← selected ticker (default: "AAPL")
  st.session_state["market"]       ← selected market
  st.session_state["date_start"]   ← start date
  st.session_state["date_end"]     ← end date (default: today)
  st.session_state["benchmark"]    ← default: "SPY"
  st.session_state["compare_list"] ← list of comparison tickers
  st.session_state["watchlist"]    ← list of watchlist tickers
  st.session_state["page"]         ← current page

When ticker changes in sidebar, ALL pages update.
When date range changes, ALL pages update.

═══════════════════════════════════════════════════════════════
SECTION 8 — EXECUTION SEQUENCE
═══════════════════════════════════════════════════════════════

Execute strictly in this order. Complete each step fully before 
moving to the next. Run the app after each major step.

STEP 1 — FOUNDATION
  Create requirements.txt, install dependencies
  Create config.py with all ticker lists, constants, markets dict
  Create styles.py with complete MAIN_CSS string
  Create components.py with all helper functions
  Verify app.py launches with dark background and sidebar

STEP 2 — DATA LAYER
  Create data_provider.py:
    fetch_price_history(ticker, period, interval) → DataFrame
    fetch_fundamentals(ticker) → dict
    fetch_fast_info(ticker) → dict
    fetch_multiple(tickers, period) → dict of DataFrames
    get_company_logo_url(ticker) → str
    All functions cached, all wrapped in try/except
  
  Create data_cleaning.py:
    clean_price_data(df) → (cleaned_df, quality_report dict)
    validate_ohlc(df) → list of warnings
    detect_outliers(df) → flagged_df
  
  Create analytics.py:
    All calculation functions from Section 4
    calculate_all_metrics(df, benchmark_df, risk_free) → dict
  
  Create insights.py:
    generate_performance_insight(metrics) → str
    generate_risk_insight(metrics) → str
    generate_observations(metrics, fundamentals) → list
    generate_takeaways(metrics) → list
    generate_comparison_takeaways(comparison_dict) → list
  
  Test data pipeline: fetch AAPL 1Y, print cleaned shape and metrics

STEP 3 — GLOBAL OVERVIEW PAGE
  Build global_overview.py
  Implement world map with country annotations
  Implement market movers fetch and table
  Implement stat strip
  Verify map renders, movers load

STEP 4 — STOCK EXPLORER PAGE
  Build stock_explorer.py
  Implement logo fetch with fallback
  Implement time period tabs updating chart
  Implement candlestick + volume chart
  Implement stat grid
  Verify ticker change updates everything

STEP 5 — RISK ANALYTICS PAGE
  Build risk_analytics.py
  Implement all metric cards with labels
  Implement drawdown chart + distribution chart
  Implement rolling volatility chart
  Implement risk metrics table

STEP 6 — STOCK COMPARISON PAGE
  Build stock_comparison.py
  Implement ticker chips with add/remove
  Implement normalized return chart (multi-line)
  Implement comparison table
  Implement correlation matrix
  Implement key takeaways
  Test with AAPL + MSFT + GOOGL + TSLA

STEP 7 — COMPANY FUNDAMENTALS PAGE
  Build company_fundamentals.py
  Implement all three columns
  Implement revenue/net income combo chart
  Test with AAPL (best yfinance coverage)

STEP 8 — AI MARKET ANALYST PAGE
  Build ai_analyst.py
  Implement all insight cards
  Wire to insights.py functions
  Verify all numbers are real calculated values

STEP 9 — WATCHLIST PAGE
  Build watchlist.py
  Implement add/remove
  Implement sparkline SVG
  Test persistence across page navigation

STEP 10 — REMAINING PAGES
  Build data_quality.py
  Build datasets.py with download buttons
  Build settings.py

STEP 11 — FINAL CHECKS
  Run full app
  Navigate all 9 pages, fix any errors
  Check: no white/light backgrounds anywhere
  Check: AAPL loads correct live data
  Check: comparison works for 4 tickers
  Check: watchlist add/remove works
  Check: all Plotly charts dark themed

═══════════════════════════════════════════════════════════════
SECTION 9 — QUALITY GATES (all must pass before done)
═══════════════════════════════════════════════════════════════

□ App loads in under 5 seconds for AAPL default view
□ All 9 pages render without Python exceptions
□ Zero white or beige backgrounds anywhere
□ Zero st.metric() calls (use custom HTML cards only)
□ Zero fake/synthetic/hardcoded financial numbers visible
□ All prices from yfinance — labeled with provider
□ Candlestick chart renders on Stock Explorer
□ Multi-ticker comparison works for AAPL+MSFT+TSLA+GOOGL
□ Correlation matrix shows real computed values
□ Watchlist persists across page changes in same session
□ World map highlights selected country
□ Market movers table shows real 1D% changes
□ Company logo loads for AAPL (or fallback letter shows)
□ All charts use consistent dark Plotly theme defined above
□ Inter font renders throughout (not system sans-serif)
□ All numbers formatted: prices=$X,XXX.XX, 
                         returns=+/-XX.XX%, 
                         large=X.XXT/B/M
□ "Not financial advice" appears on every page footer
□ Data provider status shows in sidebar bottom
□ No st.warning() or st.error() visible during normal operation

═══════════════════════════════════════════════════════════════
SECTION 10 — REQUIREMENTS.TXT
═══════════════════════════════════════════════════════════════

streamlit>=1.40.0
yfinance>=0.2.40
pandas>=2.1.0
numpy>=1.26.0
plotly>=5.18.0
scipy>=1.11.0
requests>=2.31.0
python-dotenv>=1.0.0
pytest>=7.4.0

═══════════════════════════════════════════════════════════════

Begin with STEP 1. 
Build completely. Run after each step. Fix errors immediately.
Do not stop to ask. Do not summarize. Just build.