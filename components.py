"""
Global Design Tokens & Reusable UI Component System for StockSense AI
Exact match to Reference Design:
- Colors, Typography, Spacing, Shadows, Radii
- Shared Components: Sidebar, Global Header, Search Bar, KPI Cards, Section Cards, Tabs, Performance Rows, Status Indicators
"""

import html
import os
import re
import datetime
import base64

# ── 1. DESIGN TOKENS ────────────────────────────────────────────────────────
TOKENS = {
    "bg_main": "#FBF8F0",
    "sidebar_bg_start": "#07382d",
    "sidebar_bg_mid": "#052c23",
    "sidebar_bg_end": "#031e18",
    "sidebar_active_start": "#187154",
    "sidebar_active_end": "#1c7c5d",
    "sidebar_text_idle": "#c9ded6",
    "sidebar_text_muted": "#8FAFA2",
    "text_heading": "#102238",
    "text_subheading": "#1b6e53",
    "text_body": "#122b22",
    "text_muted": "#52677A",
    "card_bg": "#FFFFFF",
    "card_border": "#eae5db",
    "card_border_subtle": "#f0ecdf",
    "color_gain": "#16a34a",
    "color_loss": "#dc2626",
    "color_warning": "#f59e0b",
    "color_info": "#3b82f6",
    "color_purple": "#9333ea",
    "color_teal": "#059669",
    "radius_card": "16px",
    "radius_pill": "28px",
    "radius_btn": "12px",
    "shadow_card": "0 2px 8px rgba(0,0,0,0.03)",
    "shadow_card_hover": "0 6px 16px rgba(0,0,0,0.06)",
    "shadow_active_pill": "0 4px 14px rgba(16,92,68,0.45)",
}

def clean_html(raw_html: str) -> str:
    """Strip all leading/trailing whitespace and newlines so Streamlit NEVER parses HTML as code blocks."""
    single_line = raw_html.strip().replace("\r\n", " ").replace("\n", " ")
    return re.sub(r">\s+<", "><", single_line)

def svg_to_data_uri(svg_code: str, width: int = 22, height: int = 22) -> str:
    """Converts raw SVG string into an img with base64 data URI so Streamlit st.html never sanitizes it away."""
    if not svg_code or not svg_code.strip():
        return ""
    # Ensure xmlns is present
    if "xmlns=" not in svg_code:
        svg_code = svg_code.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    b64 = base64.b64encode(svg_code.strip().encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{width}" height="{height}" style="display:block; object-fit:contain;" />'

# ── 2. SVG ICON DICTIONARY (UNIFORM OUTLINE STROKE STYLE) ───────────────────
NAV_ICONS = {
    "Global Overview": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>""",
    "Stock Explorer": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>""",
    "Risk Analytics": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>""",
    "Stock Comparison": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>""",
    "Company Fundamentals": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>""",
    "AI Market Analyst": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8.01" y2="16"></line><line x1="16" y1="16" x2="16.01" y2="16"></line></svg>""",
    "Watchlist": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>""",
    "Datasets": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>""",
    "Data Quality": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><polyline points="9 12 11 14 15 10"></polyline></svg>""",
    "Settings": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>""",
}

# ── 3. ASSET HELPERS ────────────────────────────────────────────────────────
def get_globe_b64() -> str:
    if os.path.exists("globe_base64.txt"):
        try:
            with open("globe_base64.txt", "r") as f:
                return f.read().strip()
        except Exception:
            pass
    return ""

def get_logo_b64() -> str:
    if os.path.exists("logo_base64.txt"):
        try:
            with open("logo_base64.txt", "r") as f:
                return f.read().strip()
        except Exception:
            pass
    return ""

def get_wave_b64() -> str:
    if os.path.exists("wave_base64.txt"):
        try:
            with open("wave_base64.txt", "r") as f:
                return f.read().strip()
        except Exception:
            pass
    return ""

# ── 4. REUSABLE UI BUILDERS ─────────────────────────────────────────────────
def format_number(val, prefix="$", precision=2):
    """Format numeric values into readable strings with optional T/B/M abbreviations."""
    if val is None or val == "N/A" or val == "":
        return "N/A"
    try:
        val = float(val)
    except (ValueError, TypeError):
        return str(val)

    abs_val = abs(val)
    sign = "-" if val < 0 else ""

    if abs_val >= 1e12:
        return f"{sign}{prefix}{abs_val / 1e12:.2f}T"
    elif abs_val >= 1e9:
        return f"{sign}{prefix}{abs_val / 1e9:.2f}B"
    elif abs_val >= 1e6:
        return f"{sign}{prefix}{abs_val / 1e6:.2f}M"
    elif abs_val >= 1e3:
        return f"{sign}{prefix}{abs_val:,.{precision}f}"
    else:
        return f"{sign}{prefix}{abs_val:.{precision}f}"


def format_pct(val, include_plus=True):
    """Format decimal or percentage values into +/-X.XX% format."""
    if val is None or val == "N/A" or val == "":
        return "N/A"
    try:
        val = float(val)
    except (ValueError, TypeError):
        return str(val)

    plus = "+" if (val > 0 and include_plus) else ""
    return f"{plus}{val:.2f}%"


def top_app_bar(show_globe: bool = False) -> str:
    """
    Renders top right header strip: Date badge + Notification Bell + User profile avatar.
    """
    now_str = datetime.datetime.now().strftime("%b %d, %Y %I:%M %p")
    cal_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#52677A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>'
    bell_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#52677A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>'
    user_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>'

    raw = f"""
    <div style="display:flex; justify-content:flex-end; align-items:center; gap:12px; margin-bottom:4px; font-family:'Inter',sans-serif;">
        <div style="display:flex; align-items:center; gap:8px; background:rgba(255,255,255,0.92); border:1px solid #EAE6DE; padding:6px 16px; border-radius:24px; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
            {svg_to_data_uri(cal_svg, 15, 15)}
            <span style="font-size:13.5px; color:#52677A; font-weight:600;">{now_str}</span>
        </div>
        <div style="position:relative; width:36px; height:36px; border-radius:50%; background:#FFFFFF; border:1px solid #EAE6DE; display:flex; align-items:center; justify-content:center; color:#52677A; box-shadow:0 1px 4px rgba(0,0,0,0.03); cursor:pointer;">
            {svg_to_data_uri(bell_svg, 17, 17)}
            <span style="position:absolute; top:4px; right:4px; width:7px; height:7px; border-radius:50%; background:#E5484D; border:1.5px solid #FFFFFF;"></span>
        </div>
        <div style="width:36px; height:36px; border-radius:50%; background:#003F35; display:flex; align-items:center; justify-content:center; color:#ffffff; box-shadow:0 2px 6px rgba(0,63,53,0.3); cursor:pointer;">
            {svg_to_data_uri(user_svg, 18, 18)}
        </div>
    </div>
    """
    return clean_html(raw)


def render_kpi_card(title: str, value: str, subtext: str, icon_svg: str, icon_bg: str, icon_stroke: str, corner_gradient: str, is_live_dot: bool = False) -> str:
    """Renders a single KPI card strictly matching Image 2 reference."""
    if is_live_dot:
        icon_box_wrapper = """
        <div style="width:34px; height:34px; border-radius:50%; background:#00A859; display:flex; align-items:center; justify-content:center; box-shadow:0 0 10px rgba(0,168,89,0.35); flex-shrink:0;">
            <div style="width:11px; height:11px; border-radius:50%; background:#FFFFFF;"></div>
        </div>
        """
    else:
        icon_box_wrapper = f"""
        <div style="width:42px; height:42px; border-radius:12px; background:{icon_bg}; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            {svg_to_data_uri(icon_svg, 22, 22)}
        </div>
        """

    sub_color = '#16A34A' if '+1' in subtext else '#52677A'
    dot_prefix = '<span style="width:7px; height:7px; border-radius:50%; background:#16A34A; display:inline-block; margin-right:6px;"></span>' if '+1' in subtext else ''

    raw = f"""
    <div class="kpi-interactive-card" style="flex:1; min-width:0; height:128px; background:rgba(255,255,255,0.92); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); border:1px solid #EAE6DE; border-radius:18px; padding:16px 18px; box-shadow:0 2px 10px rgba(0,0,0,0.025); position:relative; overflow:hidden; display:flex; flex-direction:column; justify-content:space-between; z-index:3; transition:all 0.25s ease;">
        <div style="position:absolute; bottom:0; right:0; width:130px; height:65px; background:{corner_gradient}; pointer-events:none; border-bottom-right-radius:18px;"></div>
        <div style="display:flex; align-items:center; gap:14px; position:relative; z-index:2;">
            {icon_box_wrapper}
            <div style="font-size:34px; font-weight:800; color:#102238; line-height:1; letter-spacing:-0.03em; font-family:'Inter',sans-serif;">{value}</div>
        </div>
        <div style="position:relative; z-index:2;">
            <div style="font-size:15px; font-weight:700; color:#102238; margin-bottom:2px; font-family:'Inter',sans-serif;">{title}</div>
            <div style="font-size:13px; color:{sub_color}; font-weight:600; display:flex; align-items:center; font-family:'Inter',sans-serif;">
                {dot_prefix}{subtext}
            </div>
        </div>
    </div>
    """
    return clean_html(raw)


def company_header(ticker: str, name: str, price: float, change: float, change_pct: float, 
                   exchange: str = "NASDAQ", country: str = "United States", sector: str = "Technology",
                   as_of_date: str = "Oct 1, 2026 03:04 PM", logo_url: str = None) -> str:
    """Shared company header row."""
    is_pos = (change >= 0) if change is not None else True
    change_color = "#16a34a" if is_pos else "#dc2626"
    sign = "+" if is_pos else ""
    change_str = f"{sign}{change:.2f}" if change is not None else "--"
    pct_str = f"{sign}{change_pct:.2f}%" if change_pct is not None else "--"
    price_str = f"${price:,.2f}" if price is not None else "$--"

    first_char = ticker[0] if ticker else "S"
    logo_img_html = f'<img src="{logo_url}" onerror="this.style.display=\'none\'; this.nextElementSibling.style.display=\'flex\';" style="width:48px;height:48px;border-radius:12px;object-fit:contain;background:#ffffff;padding:4px;border:1px solid #dcd7cb;" />' if logo_url else ""
    fallback_logo_html = f'<div style="display:{"none" if logo_url else "flex"};width:48px;height:48px;border-radius:12px;background:#07382d;color:#ffffff;font-weight:800;font-size:1.35rem;align-items:center;justify-content:center;border:1px solid #052c23;">{first_char}</div>'

    meta_parts = [p for p in [exchange, country, sector] if p]
    meta_str = " · ".join(meta_parts)

    raw = f"""
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.2rem;flex-wrap:wrap;gap:1rem;font-family:'Plus Jakarta Sans','Inter',sans-serif;">
        <div style="display:flex;align-items:center;gap:14px;">
            <div style="position:relative;">{logo_img_html}{fallback_logo_html}</div>
            <div>
                <div style="display:flex;align-items:baseline;gap:10px;">
                    <span style="font-size:2rem;font-weight:800;color:#102238;letter-spacing:-0.03em;">{html.escape(ticker)}</span>
                    <span style="font-size:1.15rem;font-weight:600;color:#52677A;">{html.escape(name)}</span>
                </div>
                <div style="font-size:0.76rem;color:#52677A;margin-top:2px;">{html.escape(meta_str)}</div>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:2.2rem;font-weight:800;color:#102238;line-height:1;letter-spacing:-0.03em;">{price_str}</div>
            <div style="font-size:1.02rem;font-weight:700;color:{change_color};margin-top:4px;">{change_str} ({pct_str})</div>
            <div style="font-size:0.72rem;color:#52677A;margin-top:3px;">As of {html.escape(as_of_date)}</div>
        </div>
    </div>
    """
    return clean_html(raw)


def metric_card(label, value, badge_text=None, badge_color=None, info_icon=False):
    """Secondary page standard metric card."""
    badge_styles = {
        "green": "background:#dcfce7;color:#16a34a;",
        "red":   "background:#fee2e2;color:#dc2626;",
        "amber": "background:#fef3c7;color:#d97706;",
        "blue":  "background:#dbeafe;color:#2563eb;",
    }
    badge_html = ""
    if badge_text and badge_color:
        s = badge_styles.get(badge_color, badge_styles["green"])
        badge_html = f'<div style="margin-top:8px;"><span style="{s}padding:3px 9px;border-radius:5px;font-size:0.72rem;font-weight:700;">{badge_text}</span></div>'
    
    info_html = ""
    if info_icon:
        info_html = '<span style="float:right;color:#52677A;font-size:0.85rem;cursor:help;" title="Details">ⓘ</span>'
    
    raw = f"""
    <div style="background:#ffffff;border:1px solid #eae5db;border-radius:16px;padding:18px 20px;height:100%;box-shadow:0 1px 4px rgba(0,0,0,0.04);font-family:'Plus Jakarta Sans','Inter',sans-serif;">
        {info_html}
        <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;color:#52677A;margin-bottom:8px;font-weight:700;">{label}</div>
        <div style="font-size:1.9rem;font-weight:800;color:#102238;line-height:1.1;letter-spacing:-0.03em;">{value}</div>
        {badge_html}
    </div>
    """
    return clean_html(raw)


def stat_grid(stats: dict, columns: int = 4) -> str:
    """Returns an HTML responsive grid of label:value pairs."""
    items_html = []
    for label, val in stats.items():
        items_html.append(
            f'<div style="background:#ffffff;border:1px solid #eae5db;border-radius:10px;padding:12px 16px;box-shadow:0 1px 3px rgba(0,0,0,0.03);font-family:\'Plus Jakarta Sans\',sans-serif;">'
            f'<div style="color:#52677A;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;font-weight:700;">{html.escape(label)}</div>'
            f'<div style="color:#102238;font-size:1.18rem;font-weight:800;">{html.escape(str(val))}</div>'
            f'</div>'
        )
    grid_css = f"display:grid;grid-template-columns:repeat({columns}, 1fr);gap:12px;margin-top:14px;"
    raw = f'<div style="{grid_css}">{"".join(items_html)}</div>'
    return clean_html(raw)


def sparkline_svg(prices: list, width: int = 80, height: int = 28) -> str:
    """Returns inline SVG sparkline polyline."""
    if not prices or len(prices) < 2:
        return f'<svg width="{width}" height="{height}"><line x1="0" y1="{height/2}" x2="{width}" y2="{height/2}" stroke="#dcd7cb" stroke-width="1.5"/></svg>'

    clean_prices = [p for p in prices if p is not None and not (isinstance(p, float) and p != p)]
    if len(clean_prices) < 2:
        return f'<svg width="{width}" height="{height}"><line x1="0" y1="{height/2}" x2="{width}" y2="{height/2}" stroke="#dcd7cb" stroke-width="1.5"/></svg>'

    min_p = min(clean_prices)
    max_p = max(clean_prices)
    p_range = max_p - min_p if max_p != min_p else 1.0

    pad = 3
    h_eff = height - (pad * 2)
    w_eff = width - (pad * 2)
    n = len(clean_prices)

    points = []
    for i, p in enumerate(clean_prices):
        x = pad + (i / (n - 1)) * w_eff
        y = pad + h_eff - ((p - min_p) / p_range) * h_eff
        points.append(f"{x:.1f},{y:.1f}")

    points_str = " ".join(points)
    is_positive = clean_prices[-1] >= clean_prices[0]
    stroke_color = "#16a34a" if is_positive else "#dc2626"

    return f'<svg width="{width}" height="{height}" style="overflow:visible;display:inline-block;vertical-align:middle;"><polyline fill="none" stroke="{stroke_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" points="{points_str}" /></svg>'


def validation_row(label: str, passed: bool, info: str = "") -> str:
    """Returns styled row for Data Quality page."""
    icon = "✓" if passed else "✗"
    color = "#16a34a" if passed else "#dc2626"
    bg = "#dcfce7" if passed else "#fee2e2"
    info_html = f'<span style="color:#52677A;font-size:0.78rem;margin-left:8px;">{html.escape(info)}</span>' if info else ""
    raw = f"""
    <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 18px;background:#ffffff;border:1px solid #eae5db;border-radius:10px;margin-bottom:8px;box-shadow:0 1px 3px rgba(0,0,0,0.02);font-family:'Plus Jakarta Sans','Inter',sans-serif;">
        <div style="display:flex;align-items:center;gap:12px;">
            <span style="display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:{bg};color:{color};font-weight:bold;font-size:0.85rem;">{icon}</span>
            <span style="color:#102238;font-size:0.88rem;font-weight:600;">{html.escape(label)}</span>
        </div>
        <div>
            {info_html}
            <span style="color:{color};font-weight:700;font-size:0.82rem;">{"Passed" if passed else "Failed"}</span>
        </div>
    </div>
    """
    return clean_html(raw)


def provider_badge(provider: str = "yfinance", status: str = "OK") -> str:
    """Returns green/red dot + provider name pill."""
    is_ok = status.upper() in ["OK", "CONNECTED", "LIVE"]
    dot_color = "#16a34a" if is_ok else "#dc2626"
    raw = f"""
    <div style="display:inline-flex;align-items:center;gap:7px;padding:4px 12px;background:#ffffff;border:1px solid #eae5db;border-radius:20px;font-size:0.75rem;color:#52677A;font-family:'Plus Jakarta Sans',sans-serif;">
        <span style="width:7px;height:7px;border-radius:50%;background-color:{dot_color};display:inline-block;"></span>
        <span style="font-weight:700;color:#102238;">{html.escape(provider)}</span>
        <span style="color:#c5bfb2;">•</span>
        <span style="color:{dot_color};font-weight:700;">{html.escape(status)}</span>
    </div>
    """
    return clean_html(raw)
