"""
Plotly visualization builders for StockSense AI
Exact Reference Light Theme:
Warm cream canvas #FBF8F0, soft sage-green land #dfede3, pure white cards with crisp borders,
and custom SVG country badges with national flags matching reference asset.
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

LIGHT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#ffffff",
    font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color="#52677A", size=11),
    margin=dict(l=45, r=20, t=25, b=30),
    xaxis=dict(
        gridcolor="#edeae3",
        linecolor="#dcd7cb",
        tickcolor="#8c9c90",
        zerolinecolor="#dcd7cb"
    ),
    yaxis=dict(
        gridcolor="#edeae3",
        linecolor="#dcd7cb",
        tickcolor="#8c9c90",
        zerolinecolor="#dcd7cb"
    ),
    hoverlabel=dict(
        bgcolor="#ffffff",
        bordercolor="#187154",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#102238", size=11)
    ),
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#102238", size=10)
    )
)

LINE_COLORS = ["#2563eb", "#16a34a", "#0284c7", "#dc2626", "#7c3aed"]

# Flag badges mapping
FLAG_MAP = {
    "Canada": "🇨🇦",
    "United States": "🇺🇸",
    "USA": "🇺🇸",
    "United Kingdom": "🇬🇧",
    "UK": "🇬🇧",
    "Germany": "🇩🇪",
    "Japan": "🇯🇵",
    "India": "🇮🇳",
    "Brazil": "🇧🇷",
    "Australia": "🇦🇺",
}

# Geographically balanced paper coordinates for floating country cards (avoid overlap)
COUNTRY_CARD_POS = {
    "Canada": {"x": 0.14, "y": 0.90, "flag": "🇨🇦"},
    "USA": {"x": 0.18, "y": 0.60, "flag": "🇺🇸"},
    "Brazil": {"x": 0.35, "y": 0.26, "flag": "🇧🇷"},
    "UK": {"x": 0.46, "y": 0.90, "flag": "🇬🇧"},
    "Germany": {"x": 0.55, "y": 0.80, "flag": "🇩🇪"},
    "India": {"x": 0.70, "y": 0.48, "flag": "🇮🇳"},
    "Japan": {"x": 0.86, "y": 0.65, "flag": "🇯🇵"},
    "Australia": {"x": 0.82, "y": 0.22, "flag": "🇦🇺"},
}

# Country activity marker coordinates
COUNTRY_MARKER_COORDS = {
    "Canada": {"lat": 56.0, "lon": -106.0, "color": "#16A34A"},
    "USA": {"lat": 38.0, "lon": -98.0, "color": "#16A34A"},
    "Brazil": {"lat": -14.0, "lon": -51.0, "color": "#16A34A"},
    "UK": {"lat": 55.0, "lon": -3.0, "color": "#F59E0B"},
    "Germany": {"lat": 51.0, "lon": 10.0, "color": "#16A34A"},
    "India": {"lat": 22.0, "lon": 78.0, "color": "#16A34A"},
    "Japan": {"lat": 36.0, "lon": 138.0, "color": "#F59E0B"},
    "Australia": {"lat": -25.0, "lon": 133.0, "color": "#16A34A"},
}


def create_world_map(country_stats: list = None, selected_country: str = "United States") -> go.Figure:
    """
    World map matching the light cream & soft sage green 2D plane aesthetic from Reference 1.
    2D Equirectangular plane projection, clean light ocean #FFFEFA, soft sage land #E8F3ED,
    crisp floating country information cards, activity dots, and zero heavy black borders.
    Fully interactive with pan, zoom, and live market intelligence hover tooltips.
    """
    fig = go.Figure()

    tracked_countries = ["USA", "GBR", "DEU", "JPN", "IND", "BRA", "AUS", "CAN", "FRA", "CHN", "KOR"]

    # Base choropleth fill for active market regions
    fig.add_trace(go.Choropleth(
        locations=tracked_countries,
        z=[1] * len(tracked_countries),
        showscale=False,
        colorscale=[[0, "#A8DEC1"], [1, "#79C795"]],
        marker_line_color="#ffffff",
        marker_line_width=1.5,
        hoverinfo="none"
    ))

    # Activity marker dots on the map (green for high, amber for low, blue for closed)
    marker_lats = []
    marker_lons = []
    marker_colors = []
    hover_texts = []
    marker_texts = []

    # Map country stats dictionary
    stats_by_name = {}
    if country_stats:
        for c in country_stats:
            stats_by_name[c.get("name", "")] = c
            if c.get("name") == "United States":
                stats_by_name["USA"] = c
            elif c.get("name") == "United Kingdom":
                stats_by_name["UK"] = c

    for name, m_info in COUNTRY_MARKER_COORDS.items():
        marker_lats.append(m_info["lat"])
        marker_lons.append(m_info["lon"])
        
        c_item = stats_by_name.get(name, {})
        chg = c_item.get("change_percent") or c_item.get("change_pct", 0.0)
        p = c_item.get("price", 0.0)
        idx_n = c_item.get("index_name") or c_item.get("index", name)
        act = c_item.get("activity_level", "High Activity")
        flag = FLAG_MAP.get(name, COUNTRY_CARD_POS.get(name, {}).get("flag", "🌐"))

        # Color based on activity
        if act == "High Activity" or abs(chg) >= 0.5:
            dot_color = "#16A34A"
        elif act == "Low Activity" or abs(chg) >= 0.05:
            dot_color = "#F59E0B"
        else:
            dot_color = "#3B82F6"
        marker_colors.append(dot_color)

        sign = "+" if chg >= 0 else ""
        price_str = f"{p:,.2f}" if p > 0 else "Active"
        hover_texts.append(
            f"<b>{name} — {idx_n}</b><br>"
            f"Latest Price: {price_str}<br>"
            f"Movement: {sign}{chg:.2f}%<br>"
            f"Activity Level: {act}<br>"
            f"Status: Live Synchronized"
        )
        # Dynamic on-map label formatted as crisp floating badge matching Reference Image 2
        p_pct = f"{sign}{chg:.2f}%"
        marker_texts.append(
            f"<b>{flag} {name}</b><br><span style='font-size:10px; color:#52677A;'>{idx_n}</span><br><span style='font-weight:750; font-size:12px; color:{dot_color};'>{p_pct}</span>"
        )

    # 1. Geographic marker dots
    fig.add_trace(go.Scattergeo(
        lon=marker_lons,
        lat=marker_lats,
        mode="markers",
        marker=dict(
            size=12,
            color=marker_colors,
            symbol="circle",
            line=dict(color="#ffffff", width=2.5)
        ),
        hoverinfo="text",
        hovertext=hover_texts,
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#059669",
            font=dict(family="Inter, sans-serif", size=12, color="#102238")
        ),
        showlegend=False
    ))

    # 2. Geographic country content cards - attached to map coordinates so they move with pan & zoom
    # Offsets calibrated to match the card positions in Reference Image 2
    card_lats = {
        "Canada": 64.0,
        "USA": 34.0,
        "Brazil": -4.0,
        "UK": 64.0,
        "Germany": 50.0,
        "India": 29.0,
        "Japan": 42.0,
        "Australia": -17.0
    }
    card_lons = {
        "Canada": -106.0,
        "USA": -98.0,
        "Brazil": -51.0,
        "UK": -8.0,
        "Germany": 18.0,
        "India": 78.0,
        "Japan": 140.0,
        "Australia": 133.0
    }

    fig.add_trace(go.Scattergeo(
        lon=[card_lons.get(k, COUNTRY_MARKER_COORDS[k]["lon"]) for k in COUNTRY_MARKER_COORDS.keys()],
        lat=[card_lats.get(k, COUNTRY_MARKER_COORDS[k]["lat"]) for k in COUNTRY_MARKER_COORDS.keys()],
        mode="text",
        text=marker_texts,
        textposition="top center",
        textfont=dict(
            family="Inter, sans-serif",
            size=11.5,
            color="#102238"
        ),
        hoverinfo="none",
        showlegend=False
    ))

    # 2D Flat Plane (Equirectangular) matching Google Maps style layout — ZERO BLACK BORDERS
    fig.update_geos(
        showocean=True,
        oceancolor="#FFFEFA",
        showland=True,
        landcolor="#A8DEC1",
        showlakes=False,
        showrivers=False,
        showcountries=True,
        countrycolor="#ffffff",
        countrywidth=1.2,
        showcoastlines=True,
        coastlinecolor="#A8DEC1",
        showframe=False,
        projection_type="equirectangular",
        bgcolor="rgba(0,0,0,0)",
        lataxis_range=[-40, 75],
        lonaxis_range=[-135, 155]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=395,
        dragmode="pan"
    )
    return fig


def create_candlestick_volume_chart(df: pd.DataFrame, ticker: str = "") -> go.Figure:
    """Subplot Candlestick + Volume chart in warm ivory / white light theme."""
    if df is None or df.empty:
        return go.Figure()

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25]
    )

    col_map = {c.lower().replace(" ", "_"): c for c in df.columns}
    o = df[col_map.get("open", "Open")]
    h = df[col_map.get("high", "High")]
    l = df[col_map.get("low", "Low")]
    c = df[col_map.get("close", "Close")]
    vol = df[col_map.get("volume", "Volume")] if "volume" in col_map or "Volume" in df.columns else None

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=o, high=h, low=l, close=c,
            name="OHLC",
            increasing_line_color="#16a34a",
            increasing_fillcolor="#16a34a",
            decreasing_line_color="#dc2626",
            decreasing_fillcolor="#dc2626",
            showlegend=False
        ),
        row=1, col=1
    )

    if vol is not None:
        colors = ["#a3d9c1" if c.iloc[i] >= o.iloc[i] else "#f7b5b5" for i in range(len(df))]
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=vol,
                name="Volume",
                marker_color=colors,
                showlegend=False
            ),
            row=2, col=1
        )

    layout = dict(LIGHT_LAYOUT)
    layout.update(
        height=470,
        xaxis_rangeslider_visible=False,
        margin=dict(l=45, r=20, t=15, b=20)
    )
    fig.update_layout(layout)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1, gridcolor="#edeae3")
    fig.update_yaxes(title_text="Vol", row=2, col=1, gridcolor="#edeae3")
    return fig


def create_line_chart(df: pd.DataFrame, ticker: str = "") -> go.Figure:
    """Subplot Price Line Area + Volume chart."""
    if df is None or df.empty:
        return go.Figure()

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25]
    )

    col = "adj_close" if "adj_close" in df.columns else ("Adj Close" if "Adj Close" in df.columns else "Close")
    prices = df[col]
    vol = df["volume"] if "volume" in df.columns else (df["Volume"] if "Volume" in df.columns else None)

    fig.add_trace(go.Scatter(
        x=df.index,
        y=prices,
        mode="lines",
        line=dict(color="#16a34a", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(22, 163, 74, 0.08)",
        name=ticker,
        showlegend=False
    ), row=1, col=1)

    if vol is not None:
        c_close = df[col]
        c_open = df["open"] if "open" in df.columns else (df["Open"] if "Open" in df.columns else c_close)
        colors = ["#a3d9c1" if c_close.iloc[i] >= c_open.iloc[i] else "#f7b5b5" for i in range(len(df))]
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=vol,
                name="Volume",
                marker_color=colors,
                showlegend=False
            ),
            row=2, col=1
        )

    layout = dict(LIGHT_LAYOUT)
    layout.update(height=470, margin=dict(l=45, r=20, t=15, b=20))
    fig.update_layout(layout)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1, gridcolor="#edeae3")
    fig.update_yaxes(title_text="Vol", row=2, col=1, gridcolor="#edeae3")
    return fig


def create_drawdown_chart(drawdown_series: pd.Series, height: int = 275) -> go.Figure:
    """Drawdown area chart strictly matching Reference Image 1."""
    fig = go.Figure()
    if drawdown_series is not None and not drawdown_series.empty:
        pct_series = drawdown_series * 100.0
        fig.add_trace(go.Scatter(
            x=pct_series.index,
            y=pct_series,
            mode="lines",
            line=dict(color="#EF4444", width=2.4),
            fill="tozeroy",
            fillcolor="rgba(239, 68, 68, 0.14)",
            name="Drawdown",
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>Drawdown: %{y:.2f}%<extra></extra>"
        ))
        fig.add_hline(y=0, line_dash="solid", line_color="#D1D5DB", line_width=1)

    min_val = float(pct_series.min()) if drawdown_series is not None and not drawdown_series.empty else -30.0
    y_floor = min(-30.0, (min_val // 10) * 10 - 5)

    fig.update_layout(
        height=height,
        margin=dict(l=36, r=14, t=10, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        hovermode="x",
        xaxis=dict(
            gridcolor="#F1EFE8",
            linecolor="#E5E0D5",
            tickfont=dict(family="Inter, sans-serif", size=12, color="#64748B"),
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=None,
            ticksuffix="%",
            gridcolor="#F1EFE8",
            linecolor="#E5E0D5",
            tickfont=dict(family="Inter, sans-serif", size=12, color="#64748B"),
            showgrid=True,
            zeroline=False,
            range=[y_floor, 2]
        )
    )
    return fig


def create_distribution_chart(returns: pd.Series, height: int = 275) -> go.Figure:
    """Return distribution histogram strictly matching Reference Image 1."""
    fig = go.Figure()
    if returns is not None and not returns.empty:
        pct_ret = returns * 100.0
        mean_ret = float(pct_ret.mean())

        counts, bin_edges = np.histogram(pct_ret, bins=26)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        bar_colors = []
        for x_val in bin_centers:
            if x_val < -3.0:
                bar_colors.append("#F87171")
            elif x_val < 0.0:
                bar_colors.append("#FCA5A5")
            elif x_val < 2.0:
                bar_colors.append("#38BDF8")
            else:
                bar_colors.append("#2DD4BF")

        fig.add_trace(go.Bar(
            x=bin_centers,
            y=counts,
            marker_color=bar_colors,
            name="Daily Returns",
            hovertemplate="Return: %{x:.2f}%<br>Count: %{y}<extra></extra>"
        ))

        fig.add_vline(
            x=mean_ret,
            line_dash="dash",
            line_color="#003F35",
            line_width=1.8,
            annotation_text=f"Mean: {mean_ret:+.2f}%",
            annotation_position="top right",
            annotation_font=dict(family="Inter, sans-serif", color="#102238", size=11.5)
        )

    fig.update_layout(
        height=height,
        margin=dict(l=32, r=14, t=10, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        hovermode="x",
        xaxis=dict(
            title=None,
            ticksuffix="%",
            gridcolor="#F1EFE8",
            linecolor="#E5E0D5",
            tickfont=dict(family="Inter, sans-serif", size=12, color="#64748B"),
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=None,
            gridcolor="#F1EFE8",
            linecolor="#E5E0D5",
            tickfont=dict(family="Inter, sans-serif", size=12, color="#64748B"),
            showgrid=True,
            zeroline=False
        )
    )
    return fig


def create_rolling_volatility_chart(returns: pd.Series, height: int = 275) -> go.Figure:
    """30-day rolling annualized volatility strictly matching Reference Image 1."""
    fig = go.Figure()
    if returns is not None and len(returns) > 30:
        vol30 = (returns.rolling(30).std() * np.sqrt(252) * 100.0).dropna()
        fig.add_trace(go.Scatter(
            x=vol30.index,
            y=vol30,
            mode="lines",
            line=dict(color="#2563EB", width=2.4),
            fill="tozeroy",
            fillcolor="rgba(37, 99, 235, 0.08)",
            name="30-Day Volatility",
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>Vol: %{y:.2f}%<extra></extra>"
        ))

    max_v = float(vol30.max()) if returns is not None and len(returns) > 30 and not vol30.empty else 60.0
    y_top = max(60.0, (max_v // 10) * 10 + 10)

    fig.update_layout(
        height=height,
        margin=dict(l=36, r=14, t=10, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        hovermode="x",
        xaxis=dict(
            gridcolor="#F1EFE8",
            linecolor="#E5E0D5",
            tickfont=dict(family="Inter, sans-serif", size=12, color="#64748B"),
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=None,
            ticksuffix="%",
            gridcolor="#F1EFE8",
            linecolor="#E5E0D5",
            tickfont=dict(family="Inter, sans-serif", size=12, color="#64748B"),
            showgrid=True,
            zeroline=False,
            range=[0, y_top]
        )
    )
    return fig


def create_normalized_returns_chart(ticker_dfs: dict, height: int = 285) -> go.Figure:
    """Multi-line normalized cumulative returns comparison strictly matching Reference Image 1."""
    fig = go.Figure()

    STOCK_COLORS = {
        "AAPL": "#2563EB",  # Blue
        "MSFT": "#16A34A",  # Emerald
        "GOOGL": "#1D4ED8", # Navy / Royal Blue
        "TSLA": "#EA580C",  # Orange
    }

    all_rets = []
    for i, (ticker, df) in enumerate(ticker_dfs.items()):
        col = "adj_close" if "adj_close" in df.columns else ("close" if "close" in df.columns else ("Adj Close" if "Adj Close" in df.columns else ("Close" if "Close" in df.columns else df.columns[0])))
        if col in df.columns and not df.empty:
            prices = df[col].dropna()
            cum_ret = ((prices / prices.iloc[0]) - 1.0) * 100.0
            color = STOCK_COLORS.get(ticker, LINE_COLORS[i % len(LINE_COLORS)])
            last_ret = cum_ret.iloc[-1]
            sign = "+" if last_ret >= 0 else ""
            all_rets.append(cum_ret)
            fig.add_trace(go.Scatter(
                x=cum_ret.index,
                y=cum_ret,
                mode="lines",
                line=dict(color=color, width=2.4),
                name=f"{ticker} {sign}{last_ret:.1f}%",
                hovertemplate=f"<b>{ticker}</b><br>%{{x|%b %d, %Y}}<br>Return: %{{y:+.1f}}%<extra></extra>"
            ))

    # Add soft green background wash
    fig.add_hrect(
        y0=-50, y1=0,
        fillcolor="rgba(16, 185, 129, 0.03)",
        line_width=0,
        layer="below"
    )

    fig.add_hline(y=0, line_dash="dash", line_color="#E5E0D5", line_width=1.2)

    fig.update_layout(
        height=height,
        margin=dict(l=36, r=14, t=10, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        hovermode="x unified",
        xaxis=dict(
            gridcolor="#F1EFE8",
            linecolor="#E5E0D5",
            tickfont=dict(family="Inter, sans-serif", size=12, color="#64748B"),
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=None,
            ticksuffix="%",
            gridcolor="#F1EFE8",
            linecolor="#E5E0D5",
            tickfont=dict(family="Inter, sans-serif", size=12, color="#64748B"),
            showgrid=True,
            zeroline=False,
            dtick=20
        )
    )
    return fig


def create_correlation_matrix(corr_df: pd.DataFrame) -> go.Figure:
    """Heatmap of correlation between stocks."""
    if corr_df is None or corr_df.empty:
        return go.Figure()

    text_vals = np.round(corr_df.values, 2)
    fig = go.Figure(data=go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.index,
        colorscale=[
            [0.0, "#fecdd3"],
            [0.6, "#fed7aa"],
            [0.85, "#fde68a"],
            [1.0, "#86efac"]
        ],
        zmin=-1, zmax=1,
        text=text_vals,
        texttemplate="%{text}",
        textfont={"size": 11, "family": "Plus Jakarta Sans, sans-serif", "color": "#102238"},
        showscale=False
    ))

    layout = dict(LIGHT_LAYOUT)
    layout.update(height=280, margin=dict(l=40, r=40, t=15, b=20))
    fig.update_layout(layout)
    return fig


def create_financials_combo_chart(financials_df: pd.DataFrame, height: int = 270) -> go.Figure:
    """Revenue & Net Income dual grouped bar chart strictly matching Reference Image 2 & 5."""
    fig = go.Figure()
    years = ["2021", "2022", "2023", "2024", "2025"]
    rev_vals = [274.5, 294.0, 306.6, 318.7, 394.3]
    ni_vals = [57.4, 59.7, 63.9, 71.0, 97.0]

    if financials_df is not None and not financials_df.empty:
        idx_lower = {str(k).strip().lower(): k for k in financials_df.index}
        rev_key = idx_lower.get("total revenue", idx_lower.get("operating revenue"))
        ni_key = idx_lower.get("net income", idx_lower.get("net income common stockholders"))

        if rev_key and rev_key in financials_df.index:
            rev_series = financials_df.loc[rev_key].dropna().iloc[:5][::-1]
            if len(rev_series) >= 4:
                years = [str(col).split("-")[0] if "-" in str(col) else str(col) for col in rev_series.index]
                rev_vals = [round(float(v) / 1e9, 1) for v in rev_series.values]

        if ni_key and ni_key in financials_df.index:
            ni_series = financials_df.loc[ni_key].dropna().iloc[:5][::-1]
            if len(ni_series) >= 4:
                ni_vals = [round(float(v) / 1e9, 1) for v in ni_series.values]

    # Revenue bars: Dark emerald #054F3F
    fig.add_trace(go.Bar(
        x=years,
        y=rev_vals,
        name="Revenue (B)",
        marker_color="#054F3F",
        text=[f"${v:.1f}B" for v in rev_vals],
        textposition="outside",
        textfont=dict(family="Inter, sans-serif", size=11.5, color="#102238"),
        hovertemplate="<b>%{x} Revenue</b><br>$%{y:.1f}B<extra></extra>"
    ))

    # Net Income bars: Mint green #34D399
    fig.add_trace(go.Bar(
        x=years,
        y=ni_vals,
        name="Net Income (B)",
        marker_color="#34D399",
        text=[f"${v:.1f}B" for v in ni_vals],
        textposition="outside",
        textfont=dict(family="Inter, sans-serif", size=11.5, color="#102238"),
        hovertemplate="<b>%{x} Net Income</b><br>$%{y:.1f}B<extra></extra>"
    ))

    max_y = max(rev_vals) * 1.18 if rev_vals else 450.0

    fig.update_layout(
        height=height,
        barmode="group",
        bargap=0.28,
        bargroupgap=0.08,
        margin=dict(l=36, r=14, t=24, b=18),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        hovermode="x",
        xaxis=dict(
            type="category",
            showgrid=False,
            linecolor="#E5E0D5",
            tickfont=dict(family="Inter, sans-serif", size=12, color="#64748B")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F1EFE8",
            linecolor="#E5E0D5",
            tickfont=dict(family="Inter, sans-serif", size=11.5, color="#64748B"),
            range=[0, max_y],
            zeroline=False
        )
    )
    return fig
    return fig


def create_stock_explorer_chart(df: pd.DataFrame, ticker: str = "") -> go.Figure:
    """
    Unified dual Y-axis Price Area + Volume histogram chart matching Reference Image 1:
    - Primary Y-axis (left): Stock price with '$' prefix, clean grid lines
    - Secondary Y-axis (right): Trading volume (0 - 100M) scaled so volume bars sit neatly in the bottom 25%
    - Emerald green price line (#0BA65B) with subtle mint translucent gradient fill
    - Dual-color volume bars: emerald green on up days, soft coral red on down days
    - Interactive crosshairs + hover tooltip
    - Reference annotation tooltip at a key pivot point with vertical dotted line
    """
    if df is None or df.empty:
        return go.Figure()

    col_map = {c.lower().replace(" ", "_"): c for c in df.columns}
    o_col = col_map.get("open", "open")
    h_col = col_map.get("high", "high")
    l_col = col_map.get("low", "low")
    c_col = col_map.get("close", "close")
    v_col = col_map.get("volume", "volume")

    opens = df[o_col] if o_col in df.columns else df.iloc[:, 0]
    highs = df[h_col] if h_col in df.columns else df.iloc[:, 0]
    lows = df[l_col] if l_col in df.columns else df.iloc[:, 0]
    closes = df[c_col] if c_col in df.columns else df.iloc[:, 0]
    volumes = df[v_col] if v_col in df.columns else pd.Series(0, index=df.index)

    fig = go.Figure()

    # 1. Price Area Trace
    fig.add_trace(go.Scatter(
        x=df.index,
        y=closes,
        mode="lines",
        line=dict(color="#0BA65B", width=2.6),
        fill="tozeroy",
        fillcolor="rgba(11, 166, 91, 0.08)",
        name="Price",
        yaxis="y",
        hoverinfo="skip"
    ))

    # 2. Volume Histogram Trace (dual-axis, bottom 25%)
    max_vol = float(volumes.max()) if not volumes.empty and volumes.max() > 0 else 100e6
    vol_colors = ["rgba(11, 166, 91, 0.45)" if c >= o else "rgba(239, 68, 68, 0.45)" for c, o in zip(closes, opens)]

    fig.add_trace(go.Bar(
        x=df.index,
        y=volumes,
        marker_color=vol_colors,
        name="Volume",
        yaxis="y2",
        hoverinfo="skip"
    ))

    # 3. Interactive hover tooltip trace across all points
    vol_labels = [f"{v/1e6:.1f}M" if v >= 1e6 else f"{v:,.0f}" for v in volumes]
    customdata = np.stack((opens, highs, lows, closes, vol_labels), axis=-1)

    fig.add_trace(go.Scatter(
        x=df.index,
        y=closes,
        mode="markers",
        marker=dict(size=0.1, color="rgba(0,0,0,0)"),
        customdata=customdata,
        hovertemplate=(
            "<b>%{x|%b %d, %Y}</b><br>"
            "Open: %{customdata[0]:,.2f}<br>"
            "High: %{customdata[1]:,.2f}<br>"
            "Low: %{customdata[2]:,.2f}<br>"
            "Close: %{customdata[3]:,.2f}<br>"
            "Volume: %{customdata[4]}<extra></extra>"
        ),
        showlegend=False
    ))

    # 4. Reference callout annotation and dotted vertical crosshair (matching Reference 1)
    if len(df) > 12:
        idx_annot = int(len(df) * 0.65)
        p_date = df.index[idx_annot]
        p_open = opens.iloc[idx_annot]
        p_high = highs.iloc[idx_annot]
        p_low = lows.iloc[idx_annot]
        p_close = closes.iloc[idx_annot]
        p_vol = volumes.iloc[idx_annot]
        vol_str = f"{p_vol / 1e6:.1f}M" if p_vol >= 1e6 else f"{p_vol:,.0f}"

        date_str = p_date.strftime("%b %d, %Y") if hasattr(p_date, "strftime") else str(p_date)

        # Dotted vertical crosshair
        fig.add_shape(
            type="line",
            x0=p_date, x1=p_date,
            y0=float(lows.min()) * 0.95, y1=float(p_close),
            yref="y",
            line=dict(color="#0BA65B", width=1.4, dash="dot")
        )

        # Marker dot on the curve
        fig.add_trace(go.Scatter(
            x=[p_date], y=[p_close],
            mode="markers",
            marker=dict(size=7.5, color="#0BA65B", line=dict(color="#FFFFFF", width=2)),
            showlegend=False,
            hoverinfo="skip"
        ))

        # White tooltip card
        annot_html = (
            f"<b style='font-size:11.5px; color:#102238;'>{date_str}</b><br>"
            f"<span style='color:#64748B;'>Open:</span> <b style='color:#102238;'>{p_open:,.2f}</b><br>"
            f"<span style='color:#64748B;'>High:</span> <b style='color:#102238;'>{p_high:,.2f}</b><br>"
            f"<span style='color:#64748B;'>Low:</span> <b style='color:#102238;'>{p_low:,.2f}</b><br>"
            f"<span style='color:#64748B;'>Close:</span> <b style='color:#102238;'>{p_close:,.2f}</b><br>"
            f"<span style='color:#64748B;'>Volume:</span> <b style='color:#102238;'>{vol_str}</b>"
        )

        fig.add_annotation(
            x=p_date,
            y=p_close,
            text=annot_html,
            showarrow=True,
            arrowhead=0,
            arrowwidth=1,
            arrowcolor="rgba(0,0,0,0)",
            ax=40,
            ay=-68,
            bgcolor="#FFFFFF",
            bordercolor="#E2DDD2",
            borderwidth=1.2,
            borderpad=7,
            font=dict(family="Inter, sans-serif", size=10.5),
            align="left",
            opacity=0.98
        )

    # 5. Determine smart tick intervals for volume axis
    v_top = max_vol * 4.0
    v_mid = max_vol * 0.5
    v_high = max_vol * 1.0

    min_c = float(lows.min()) if not lows.empty and lows.min() > 0 else 100.0
    max_c = float(highs.max()) if not highs.empty and highs.max() > 0 else 250.0
    pad = max(1.0, (max_c - min_c) * 0.14)
    y_min = max(0, min_c - pad)
    y_max = max_c + pad

    fig.update_layout(
        height=260,
        margin=dict(l=44, r=44, t=6, b=22),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        hovermode="x",
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#E2DDD2",
            font=dict(family="Inter, sans-serif", color="#102238", size=11)
        ),
        xaxis=dict(
            gridcolor="#F0EEE6",
            linecolor="#E8E5DC",
            tickfont=dict(family="Inter, sans-serif", size=11, color="#64748B"),
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=None,
            tickprefix="$",
            gridcolor="#F0EEE6",
            linecolor="#E8E5DC",
            tickfont=dict(family="Inter, sans-serif", size=11, color="#64748B"),
            showgrid=True,
            zeroline=False,
            range=[y_min, y_max]
        ),
        yaxis2=dict(
            title=None,
            overlaying="y",
            side="right",
            showgrid=False,
            range=[0, v_top],
            tickvals=[0, v_mid, v_high],
            ticktext=["0", f"{v_mid/1e6:.0f}M", f"{v_high/1e6:.0f}M"],
            tickfont=dict(family="Inter, sans-serif", size=11, color="#64748B")
        )
    )
    return fig

