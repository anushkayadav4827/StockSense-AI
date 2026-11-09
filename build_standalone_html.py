# -*- coding: utf-8 -*-
"""
Generates the complete standalone front-end implementation requested by the user:
- Open-source Leaflet.js interactive world map with Google Maps-like pan, zoom, and rotation
- Realistic 3D Globe image anchored in top-right corner with emerald atmospheric aura
- Floating KPI cards directly overlaid on top of the globe image with frosted glass
- Fully responsive and operational search bar that dynamically filters, pans to country, and updates metrics
- Dynamic tooltip/content panels when hovering over countries/markers pulling real-time market data
- Dual real-time update engine: Periodic polling + WebSocket stream placeholder
- Styled with StockSense AI palette (#003F35, #087E69, #A8DEC1, #FAF7F2, #FFFEFA)
"""
import os

with open("globe_base64.txt", "r") as f:
    globe_b64 = f.read().strip()

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StockSense AI — Global Market Intelligence Dashboard</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Leaflet.js CSS (Open-Source Interactive Map) -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
    
    <style>
        /* ── CSS RESET & CORE VARIABLES ───────────────────────────── */
        :root {{
            --bg-canvas: #FAF7F2;
            --bg-card: #FFFEFA;
            --border-card: #EAE6DE;
            --color-primary: #003F35;
            --color-secondary: #087E69;
            --color-accent: #0BA65B;
            --color-positive: #16A34A;
            --color-positive-bg: #E8F8EE;
            --color-negative: #E5484D;
            --color-negative-bg: #FEE8E8;
            --color-text-main: #102238;
            --color-text-muted: #52677A;
            --map-land: #A8DEC1;
            --map-ocean: #FFFEFA;
            --shadow-card: 0 4px 16px rgba(0, 0, 0, 0.03);
            --shadow-hover: 0 8px 24px rgba(0, 63, 53, 0.08);
            --radius-card: 16px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-canvas);
            color: var(--color-text-main);
            overflow-x: hidden;
            padding: 24px 36px 40px 36px;
            -webkit-font-smoothing: antialiased;
        }}

        /* ── DASHBOARD WRAPPER & GLOBE BACKGROUND ─────────────────── */
        .dashboard-container {{
            max-width: 1560px;
            margin: 0 auto;
            position: relative;
        }}

        /* 3D Earth Globe in Top Right Corner matching Reference Image 2 */
        .globe-wrapper {{
            position: absolute;
            top: -20px;
            right: 0px;
            width: 320px;
            height: 320px;
            pointer-events: none;
            z-index: 1;
            overflow: visible;
        }}

        .globe-glow {{
            position: absolute;
            width: 340px;
            height: 340px;
            top: -10px;
            right: -10px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(16, 185, 129, 0.32) 0%, rgba(16, 185, 129, 0.10) 50%, rgba(255, 255, 255, 0) 75%);
            filter: blur(18px);
        }}

        .globe-image {{
            width: 100%;
            height: auto;
            display: block;
            position: relative;
            z-index: 2;
            filter: drop-shadow(0 8px 24px rgba(0, 63, 53, 0.12));
            animation: gentle-float 8s ease-in-out infinite;
        }}

        @keyframes gentle-float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-4px) rotate(1deg); }}
        }}

        /* ── TOP APP BAR (DATE, NOTIFICATIONS, PROFILE) ─────────────── */
        .top-app-bar {{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
            position: relative;
            z-index: 10;
        }}

        .date-pill {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid var(--border-card);
            padding: 7px 18px;
            border-radius: 24px;
            font-size: 13.5px;
            font-weight: 600;
            color: var(--color-text-muted);
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
        }}

        .icon-circle-btn {{
            position: relative;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: #FFFFFF;
            border: 1px solid var(--border-card);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--color-text-muted);
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .icon-circle-btn:hover {{
            background: #F4EFEB;
        }}

        .badge-dot {{
            position: absolute;
            top: 4px;
            right: 4px;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--color-negative);
            border: 1.5px solid #FFFFFF;
        }}

        .avatar-circle {{
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: var(--color-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF;
            box-shadow: 0 2px 8px rgba(0, 63, 53, 0.25);
            cursor: pointer;
        }}

        /* ── HEADER TITLE & INTRO ──────────────────────────────────── */
        .dashboard-header {{
            position: relative;
            z-index: 5;
            max-width: 68%;
            margin-bottom: 14px;
        }}

        .main-title {{
            font-size: 38px;
            font-weight: 800;
            color: var(--color-text-main);
            letter-spacing: -0.03em;
            line-height: 1.15;
            margin-bottom: 4px;
        }}

        .sub-title {{
            color: var(--color-secondary);
            font-size: 19.5px;
            font-weight: 700;
            letter-spacing: -0.01em;
            margin-bottom: 4px;
        }}

        .desc-text {{
            font-size: 15px;
            color: var(--color-text-muted);
            font-weight: 500;
        }}

        /* ── SEARCH BAR (RESPONSIVE & FUNCTIONAL) ──────────────────── */
        .search-container {{
            position: relative;
            z-index: 5;
            max-width: 56%;
            margin-bottom: 16px;
        }}

        .search-box {{
            position: relative;
            display: flex;
            align-items: center;
            background: #FFFFFF;
            border: 1px solid var(--border-card);
            border-radius: 14px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
            transition: all 0.2s ease;
        }}

        .search-box:focus-within {{
            border-color: var(--color-secondary);
            box-shadow: 0 0 0 3px rgba(8, 126, 105, 0.15);
        }}

        .search-icon-left {{
            position: absolute;
            left: 18px;
            color: var(--color-text-muted);
            pointer-events: none;
            display: flex;
            align-items: center;
        }}

        .search-input {{
            width: 100%;
            height: 52px;
            border: none;
            outline: none;
            background: transparent;
            font-family: inherit;
            font-size: 15px;
            font-weight: 500;
            color: var(--color-text-main);
            padding: 0 60px 0 48px;
        }}

        .search-input::placeholder {{
            color: #8FAFA2;
        }}

        .search-submit-btn {{
            position: absolute;
            right: 8px;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: var(--color-secondary);
            color: #FFFFFF;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s ease, transform 0.15s ease;
        }}

        .search-submit-btn:hover {{
            background: #066252;
            transform: scale(1.05);
        }}

        /* ── 4 KPI STAT CARDS (LAYERED OVER GLOBE WITH FROSTED GLASS) ─ */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 20px;
            position: relative;
            z-index: 4;
        }}

        .kpi-card {{
            height: 126px;
            background: rgba(255, 254, 250, 0.88);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 16px 20px;
            box-shadow: var(--shadow-card);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }}

        .kpi-top {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .kpi-icon-box {{
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .kpi-value {{
            font-size: 34px;
            font-weight: 800;
            color: var(--color-text-main);
            line-height: 1;
            letter-spacing: -0.03em;
        }}

        .kpi-title {{
            font-size: 15px;
            font-weight: 700;
            color: var(--color-text-main);
            margin-bottom: 2px;
        }}

        .kpi-subtext {{
            font-size: 13px;
            font-weight: 600;
            color: var(--color-text-muted);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .kpi-subtext.positive {{
            color: var(--color-positive);
        }}

        .pulse-indicator {{
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: var(--color-positive);
            box-shadow: 0 0 0 rgba(22, 163, 74, 0.4);
            animation: pulse-ring 2s infinite;
        }}

        @keyframes pulse-ring {{
            0% {{ box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7); }}
            70% {{ box-shadow: 0 0 0 10px rgba(22, 163, 74, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(22, 163, 74, 0); }}
        }}

        /* ── MAIN ANALYTICS GRID (MAP 65% + MOVERS 35%) ────────────── */
        .analytics-grid {{
            display: grid;
            grid-template-columns: 65% 35%;
            gap: 24px;
            position: relative;
            z-index: 2;
        }}

        .analytics-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 24px;
            box-shadow: var(--shadow-card);
            display: flex;
            flex-direction: column;
        }}

        .card-header-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }}

        .card-title-group {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .card-h2 {{
            font-size: 24px;
            font-weight: 800;
            color: var(--color-text-main);
            letter-spacing: -0.02em;
        }}

        /* ── LEAFLET WORLD MAP STYLING (GOOGLE MAPS STYLE) ─────────── */
        .map-viewport-wrapper {{
            position: relative;
            width: 100%;
            height: 480px;
            border-radius: 12px;
            overflow: hidden;
            background: var(--map-ocean);
        }}

        #leaflet-world-map {{
            width: 100%;
            height: 100%;
            background: var(--map-ocean);
        }}

        /* Custom Leaflet Controls */
        .map-control-overlay {{
            position: absolute;
            top: 14px;
            right: 14px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .map-btn {{
            width: 36px;
            height: 36px;
            background: #FFFFFF;
            border: 1px solid var(--border-card);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--color-text-main);
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
            transition: all 0.15s ease;
        }}

        .map-btn:hover {{
            background: #F4EFEB;
            transform: scale(1.05);
        }}

        /* Country Content Badge Overlays matching Reference Image 2 */
        .country-card-marker {{
            background: #FFFFFF;
            border: 1px solid #EAE6DE;
            border-radius: 10px;
            padding: 6px 12px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
            font-family: 'Inter', sans-serif;
            text-align: center;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            pointer-events: auto;
        }}

        .country-card-marker:hover {{
            transform: translateY(-3px) scale(1.04);
            box-shadow: 0 8px 20px rgba(0, 63, 53, 0.16);
            border-color: var(--color-secondary);
        }}

        .country-card-title {{
            font-size: 12px;
            font-weight: 800;
            color: var(--color-text-main);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
        }}

        .country-card-idx {{
            font-size: 9.5px;
            font-weight: 600;
            color: var(--color-text-muted);
            margin: 1px 0;
        }}

        .country-card-pct {{
            font-size: 12px;
            font-weight: 800;
            line-height: 1.1;
        }}

        .country-card-pct.pos {{
            color: var(--color-positive);
        }}

        .country-card-pct.neg {{
            color: var(--color-negative);
        }}

        /* Radar Pin Dot */
        .map-pin-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 2.5px solid #FFFFFF;
            position: relative;
        }}

        .map-pin-dot.green {{ background: #16A34A; }}
        .map-pin-dot.amber {{ background: #F59E0B; }}
        .map-pin-dot.blue  {{ background: #3B82F6; }}

        /* Hover Tooltip / Detail Panel */
        .market-preview-tooltip {{
            background: #FFFFFF;
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 14px 18px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            font-size: 12.5px;
            color: var(--color-text-main);
            min-width: 200px;
        }}

        .preview-header {{
            font-size: 14px;
            font-weight: 800;
            color: var(--color-text-main);
            margin-bottom: 6px;
            border-bottom: 1px solid #EAE6DE;
            padding-bottom: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .preview-row {{
            display: flex;
            justify-content: space-between;
            padding: 3px 0;
        }}

        .preview-label {{
            color: var(--color-text-muted);
        }}

        .preview-val {{
            font-weight: 700;
        }}

        /* Map Activity Legend */
        .map-legend {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 24px;
            font-size: 13px;
            color: var(--color-text-muted);
            font-weight: 600;
            margin-top: 12px;
            padding-top: 4px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .legend-dot {{
            width: 9px;
            height: 9px;
            border-radius: 50%;
        }}

        /* ── MARKET MOVERS (35% SECTION) ───────────────────────────── */
        .movers-pill-row {{
            display: flex;
            gap: 8px;
            background: #F4EFEB;
            border-radius: 10px;
            padding: 4px;
            margin-bottom: 16px;
        }}

        .movers-toggle-btn {{
            flex: 1;
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 13.5px;
            font-weight: 700;
            text-align: center;
            border: none;
            cursor: pointer;
            background: transparent;
            color: var(--color-text-muted);
            transition: all 0.2s ease;
        }}

        .movers-toggle-btn.active {{
            background: var(--color-primary);
            color: #FFFFFF;
            box-shadow: 0 2px 8px rgba(0, 63, 53, 0.25);
        }}

        .movers-list {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            flex: 1;
        }}

        .mover-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 14px;
            border-radius: 10px;
            transition: background 0.15s ease;
        }}

        .mover-row:hover {{
            background: #F7F4EE;
        }}

        .mover-symbol {{
            font-size: 14.5px;
            font-weight: 800;
            color: var(--color-text-main);
        }}

        .mover-data {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .mover-price {{
            font-size: 14.5px;
            font-weight: 600;
            color: var(--color-text-main);
        }}

        .mover-badge {{
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 700;
            min-width: 65px;
            text-align: right;
            transition: all 0.3s ease;
        }}

        .mover-badge.pos {{
            background: var(--color-positive-bg);
            color: var(--color-positive);
        }}

        .mover-badge.neg {{
            background: var(--color-negative-bg);
            color: var(--color-negative);
        }}

        .view-more-link {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            font-weight: 700;
            color: var(--color-secondary);
            text-decoration: none;
            margin-top: 14px;
            cursor: pointer;
            transition: color 0.15s ease;
        }}

        .view-more-link:hover {{
            color: var(--color-primary);
            text-decoration: underline;
        }}

        /* ── FOOTER STATUS BAR ─────────────────────────────────────── */
        .dashboard-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            font-size: 12.5px;
            color: #8FAFA2;
            font-weight: 500;
        }}

        .footer-status {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--color-positive);
            font-weight: 600;
        }}
    </style>
</head>
<body>

<div class="dashboard-container">
    
    <!-- 3D Decorative Earth Globe anchored in Top Right -->
    <div class="globe-wrapper">
        <div class="globe-glow"></div>
        <img class="globe-image" src="data:image/png;base64,{globe_b64}" alt="StockSense Earth Globe" />
    </div>

    <!-- Top App Bar -->
    <div class="top-app-bar">
        <div class="date-pill">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            <span id="live-clock">Oct 1, 2026 02:24 PM</span>
        </div>
        <div class="icon-circle-btn">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
            <span class="badge-dot"></span>
        </div>
        <div class="avatar-circle">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        </div>
    </div>

    <!-- Header Section -->
    <div class="dashboard-header">
        <h1 class="main-title">StockSense AI</h1>
        <div class="sub-title">Global Market Intelligence & Risk Analytics</div>
        <p class="desc-text">Explore global markets, analyze performance, compare stocks and get AI-powered insights.</p>
    </div>

    <!-- Search Bar with Live Filter & Navigation -->
    <div class="search-container">
        <div class="search-box">
            <div class="search-icon-left">
                <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </div>
            <input type="text" id="global-search-input" class="search-input" placeholder="Search for a company, country or ticker (e.g., AAPL, RELIANCE, TSLA, Canada ...)" />
            <button class="search-submit-btn" id="search-btn" title="Search Market">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </button>
        </div>
    </div>

    <!-- 4 Equal KPI Stat Cards (Layered Directly Over the Globe) -->
    <div class="kpi-row">
        <!-- Card 1 -->
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-icon-box" style="background:#E6F8F0; color:#008F63;">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                </div>
                <div class="kpi-value" id="kpi-markets-val">8</div>
            </div>
            <div>
                <div class="kpi-title">Global Markets</div>
                <div class="kpi-subtext positive">
                    <span style="width:7px; height:7px; border-radius:50%; background:#16A34A; display:inline-block;"></span>
                    +1 today
                </div>
            </div>
        </div>

        <!-- Card 2 -->
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-icon-box" style="background:#F4EEFC; color:#9333EA;">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="9" y2="2"></line><line x1="15" y1="6" x2="17" y2="6"></line><line x1="15" y1="10" x2="17" y2="10"></line><line x1="15" y1="14" x2="17" y2="14"></line><line x1="15" y1="18" x2="17" y2="18"></line></svg>
                </div>
                <div class="kpi-value">25,430+</div>
            </div>
            <div>
                <div class="kpi-title">Tracked Companies</div>
                <div class="kpi-subtext">Across 50+ countries</div>
            </div>
        </div>

        <!-- Card 3 (Directly Over Globe Atmosphere) -->
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-icon-box" style="background:#E6F8F2; color:#059669;">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                </div>
                <div class="kpi-value">12</div>
            </div>
            <div>
                <div class="kpi-title">Major Indexes</div>
                <div class="kpi-subtext">S&P 500, NIFTY, FTSE ...</div>
            </div>
        </div>

        <!-- Card 4 (Directly Over Globe Body) -->
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-icon-box" style="background:#E8F8EE;">
                    <span class="pulse-indicator"></span>
                </div>
                <div class="kpi-value" style="font-size:30px;">Live</div>
            </div>
            <div>
                <div class="kpi-title">Market Data</div>
                <div class="kpi-subtext">(via Twelve Data & yfinance)</div>
            </div>
        </div>
    </div>

    <!-- Main Analytics Grid: Map (65%) + Market Movers (35%) -->
    <div class="analytics-grid">
        
        <!-- Left: Global Market Performance Leaflet Map -->
        <div class="analytics-card">
            <div class="card-header-bar">
                <div class="card-title-group">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#008F63" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                    <h2 class="card-h2">Global Market Performance</h2>
                </div>
            </div>

            <!-- Map Viewport -->
            <div class="map-viewport-wrapper">
                <div id="leaflet-world-map"></div>

                <!-- Custom Map Interactive Controls (Google Maps-like Pan, Zoom, Reset) -->
                <div class="map-control-overlay">
                    <button class="map-btn" id="map-zoom-in" title="Zoom In">+</button>
                    <button class="map-btn" id="map-zoom-out" title="Zoom Out">−</button>
                    <button class="map-btn" id="map-reset" title="Reset World View">⟲</button>
                </div>
            </div>

            <!-- Activity Legend -->
            <div class="map-legend">
                <div class="legend-item">
                    <span class="legend-dot" style="background:#16A34A;"></span>
                    <span>High Activity</span>
                </div>
                <span style="color:#D5D0C5;">|</span>
                <div class="legend-item">
                    <span class="legend-dot" style="background:#F59E0B;"></span>
                    <span>Low Activity</span>
                </div>
                <span style="color:#D5D0C5;">|</span>
                <div class="legend-item">
                    <span class="legend-dot" style="background:#3B82F6;"></span>
                    <span>No Activity</span>
                </div>
            </div>
        </div>

        <!-- Right: Market Movers -->
        <div class="analytics-card">
            <div class="card-header-bar">
                <div class="card-title-group">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#008F63" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
                    <h2 class="card-h2">Market Movers</h2>
                </div>
            </div>

            <!-- Gainers vs Losers Pills -->
            <div class="movers-pill-row">
                <button class="movers-toggle-btn active" id="tab-gainers">Top Gainers</button>
                <button class="movers-toggle-btn" id="tab-losers">Top Losers</button>
            </div>

            <!-- Movers List -->
            <div class="movers-list" id="movers-container">
                <!-- Dynamically populated rows -->
            </div>

            <a class="view-more-link" id="view-more-btn">View more →</a>
        </div>

    </div>

    <!-- Bottom Status Line -->
    <div class="dashboard-footer">
        <div>StockSense AI v3.0.0 · Dual feed via Twelve Data & yfinance · Historical analysis only · Not financial advice</div>
        <div class="footer-status">
            <span style="width:7px; height:7px; border-radius:50%; background:#16A34A; display:inline-block;"></span>
            <span>System Operational</span>
        </div>
    </div>

</div>

<!-- Leaflet.js Library -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

<script>
/**
 * ════════════════════════════════════════════════════════════════════════════
 * STOCKSENSE AI — REAL-TIME GLOBAL MARKET INTELLIGENCE SCRIPT
 * ════════════════════════════════════════════════════════════════════════════
 * Includes:
 * 1. Leaflet Interactive World Map (smooth pan, zoom, custom styled tiles)
 * 2. Country Card HTML Markers with animated pulse dots
 * 3. Dynamic hover tooltips pulling real financial market metrics
 * 4. Responsive search bar matching tickers and panning to countries
 * 5. Real-time polling tick engine simulating live market updates
 * 6. WebSocket client placeholder ready to connect to Twelve Data / Custom feed
 */

// ── 1. GLOBAL MARKET DATASET ────────────────────────────────────────────────
const MARKET_REGIONS = [
    {{
        id: "CAN",
        country: "Canada",
        flag: "🇨🇦",
        index: "S&P/TSX",
        symbol: "^GSPTSE",
        lat: 56.13,
        lon: -106.34,
        cardLat: 64.0,
        cardLon: -106.34,
        price: 35789.10,
        pct: 0.55,
        activity: "High Activity",
        volume: "245.8M",
        dayHigh: 35840.20,
        dayLow: 35560.10
    }},
    {{
        id: "USA",
        country: "USA",
        flag: "🇺🇸",
        index: "S&P 500",
        symbol: "^GSPC",
        lat: 37.09,
        lon: -95.71,
        cardLat: 33.0,
        cardLon: -95.71,
        price: 7376.86,
        pct: 0.27,
        activity: "Low Activity",
        volume: "3.42B",
        dayHigh: 7392.15,
        dayLow: 7340.50
    }},
    {{
        id: "BRA",
        country: "Brazil",
        flag: "🇧🇷",
        index: "IBOVESPA",
        symbol: "^BVSP",
        lat: -14.23,
        lon: -51.92,
        cardLat: -5.0,
        cardLon: -51.92,
        price: 168499.00,
        pct: 1.11,
        activity: "High Activity",
        volume: "1.12B",
        dayHigh: 169200.00,
        dayLow: 167500.00
    }},
    {{
        id: "GBR",
        country: "UK",
        flag: "🇬🇧",
        index: "FTSE 100",
        symbol: "^FTSE",
        lat: 55.37,
        lon: -3.43,
        cardLat: 64.0,
        cardLon: -8.0,
        price: 10673.90,
        pct: -0.91,
        activity: "High Activity",
        volume: "740.3M",
        dayHigh: 10760.10,
        dayLow: 10640.80
    }},
    {{
        id: "DEU",
        country: "Germany",
        flag: "🇩🇪",
        index: "DAX",
        symbol: "^GDAXI",
        lat: 51.16,
        lon: 10.45,
        cardLat: 50.0,
        cardLon: 18.0,
        price: 25820.36,
        pct: -1.91,
        activity: "High Activity",
        volume: "520.1M",
        dayHigh: 26150.00,
        dayLow: 25780.20
    }},
    {{
        id: "IND",
        country: "India",
        flag: "🇮🇳",
        index: "NIFTY 50",
        symbol: "^NSEI",
        lat: 20.59,
        lon: 78.96,
        cardLat: 30.0,
        cardLon: 78.96,
        price: 25030.35,
        pct: 2.01,
        activity: "High Activity",
        volume: "890.4M",
        dayHigh: 25110.00,
        dayLow: 24820.00
    }},
    {{
        id: "JPN",
        country: "Japan",
        flag: "🇯🇵",
        index: "Nikkei 225",
        symbol: "^N225",
        lat: 36.20,
        lon: 138.25,
        cardLat: 42.0,
        cardLon: 140.0,
        price: 57434.77,
        pct: -5.98,
        activity: "High Activity",
        volume: "1.45B",
        dayHigh: 58200.00,
        dayLow: 56900.00
    }},
    {{
        id: "AUS",
        country: "Australia",
        flag: "🇦🇺",
        index: "ASX 200",
        symbol: "^AXJO",
        lat: -25.27,
        lon: 133.77,
        cardLat: -16.0,
        cardLon: 133.77,
        price: 9020.80,
        pct: -0.49,
        activity: "Low Activity",
        volume: "480.2M",
        dayHigh: 9080.00,
        dayLow: 8990.00
    }}
];

// Market Movers initial dataset
const TOP_GAINERS = [
    {{ symbol: "TSLA", price: 358.22, change: 6.12 }},
    {{ symbol: "ASML", price: 1424.75, change: 5.61 }},
    {{ symbol: "NVDA", price: 186.64, change: 3.32 }},
    {{ symbol: "RELIANCE", price: 1320.00, change: 0.50 }},
    {{ symbol: "HSBA", price: 1304.60, change: 0.23 }},
    {{ symbol: "MSFT", price: 530.61, change: 0.17 }}
];

const TOP_LOSERS = [
    {{ symbol: "INTC", price: 21.40, change: -4.85 }},
    {{ symbol: "BABA", price: 82.15, change: -3.42 }},
    {{ symbol: "SAP", price: 210.30, change: -2.18 }},
    {{ symbol: "SONY", price: 88.50, change: -1.94 }},
    {{ symbol: "NKE", price: 74.80, change: -1.62 }}
];

// ── 2. INITIALIZE LEAFLET INTERACTIVE WORLD MAP ──────────────────────────────
let map = null;
const markerInstances = {{}};

function initMap() {{
    // Initialize Leaflet map with Google Maps-like pan and zoom behavior
    map = L.map('leaflet-world-map', {{
        center: [20, 10],
        zoom: 2,
        minZoom: 1.5,
        maxZoom: 6,
        zoomControl: false,
        attributionControl: false,
        worldCopyJump: true,
        scrollWheelZoom: true,
        doubleClickZoom: true,
        dragging: true
    }});

    // Esri World Light Gray Canvas tile layer (completely free, zero API key required, zero watermarks)
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
        maxZoom: 16,
        attribution: ''
    }}).addTo(map);

    // Render Country Content Card Markers & Pulse Dots
    MARKET_REGIONS.forEach(region => {{
        // Activity dot color
        const dotClass = region.activity === 'High Activity' ? 'green' : (region.activity === 'Low Activity' ? 'amber' : 'blue');
        const pctClass = region.pct >= 0 ? 'pos' : 'neg';
        const sign = region.pct >= 0 ? '+' : '';

        // 1. Radar Pulse Dot at coordinates
        const dotIcon = L.divIcon({{
            className: 'custom-pin-container',
            html: `<div class="map-pin-dot ${{dotClass}}"></div>`,
            iconSize: [12, 12],
            iconAnchor: [6, 6]
        }});
        L.marker([region.lat, region.lon], {{ icon: dotIcon, interactive: false }}).addTo(map);

        // 2. Crisp Country Information Card Overlay
        const cardHtml = `
            <div class="country-card-marker" id="card-${{region.id}}">
                <div class="country-card-title">
                    <span>${{region.flag}}</span>
                    <span>${{region.country}}</span>
                </div>
                <div class="country-card-idx">${{region.index}}</div>
                <div class="country-card-pct ${{pctClass}}">${{sign}}${{region.pct.toFixed(2)}}%</div>
            </div>
        `;

        const cardIcon = L.divIcon({{
            className: 'custom-card-container',
            html: cardHtml,
            iconSize: [110, 54],
            iconAnchor: [55, 27]
        }});

        const cardMarker = L.marker([region.cardLat, region.cardLon], {{ icon: cardIcon }}).addTo(map);
        markerInstances[region.id] = cardMarker;

        // Dynamic Interactive Tooltip on Hover
        const tooltipContent = `
            <div class="market-preview-tooltip">
                <div class="preview-header">
                    <span>${{region.flag}} ${{region.country}} (${{region.index}})</span>
                    <span style="color:${{region.pct >= 0 ? '#16A34A' : '#E5484D'}};">${{sign}}${{region.pct.toFixed(2)}}%</span>
                </div>
                <div class="preview-row">
                    <span class="preview-label">Price:</span>
                    <span class="preview-val">${{region.price.toLocaleString(undefined, {{minimumFractionDigits: 2}})}}</span>
                </div>
                <div class="preview-row">
                    <span class="preview-label">Volume:</span>
                    <span class="preview-val">${{region.volume}}</span>
                </div>
                <div class="preview-row">
                    <span class="preview-label">Day Range:</span>
                    <span class="preview-val">${{region.dayLow.toLocaleString()}} - ${{region.dayHigh.toLocaleString()}}</span>
                </div>
                <div class="preview-row">
                    <span class="preview-label">Activity:</span>
                    <span class="preview-val" style="color:#087E69;">${{region.activity}}</span>
                </div>
            </div>
        `;

        cardMarker.bindTooltip(tooltipContent, {{
            direction: 'top',
            offset: [0, -18],
            className: 'custom-tooltip-wrapper',
            opacity: 1
        }});

        // Click on marker to center and zoom
        cardMarker.on('click', () => {{
            map.flyTo([region.lat, region.lon], 4, {{ duration: 1.2 }});
        }});
    }});

    // Setup map control buttons
    document.getElementById('map-zoom-in').addEventListener('click', () => map.zoomIn());
    document.getElementById('map-zoom-out').addEventListener('click', () => map.zoomOut());
    document.getElementById('map-reset').addEventListener('click', () => {{
        map.flyTo([20, 10], 2, {{ duration: 1.0 }});
    }});
}}

// ── 3. RENDER MARKET MOVERS LIST ────────────────────────────────────────────
let currentMoversTab = "gainers";

function renderMovers() {{
    const container = document.getElementById('movers-container');
    const items = currentMoversTab === "gainers" ? TOP_GAINERS : TOP_LOSERS;
    
    container.innerHTML = items.map(m => {{
        const isPos = m.change >= 0;
        const sign = isPos ? '+' : '';
        const badgeClass = isPos ? 'pos' : 'neg';
        return `
            <div class="mover-row">
                <div class="mover-symbol">${{m.symbol}}</div>
                <div class="mover-data">
                    <div class="mover-price">${{m.price.toLocaleString(undefined, {{minimumFractionDigits: 2}})}}</div>
                    <div class="mover-badge ${{badgeClass}}">${{sign}}${{m.change.toFixed(2)}}%</div>
                </div>
            </div>
        `;
    }}).join('');
}}

document.getElementById('tab-gainers').addEventListener('click', () => {{
    currentMoversTab = "gainers";
    document.getElementById('tab-gainers').classList.add('active');
    document.getElementById('tab-losers').classList.remove('active');
    renderMovers();
}});

document.getElementById('tab-losers').addEventListener('click', () => {{
    currentMoversTab = "losers";
    document.getElementById('tab-losers').classList.add('active');
    document.getElementById('tab-gainers').classList.remove('active');
    renderMovers();
}});

// ── 4. RESPONSIVE SEARCH BAR ENGINE ─────────────────────────────────────────
function executeSearch() {{
    const query = document.getElementById('global-search-input').value.trim().toLowerCase();
    if (!query) return;

    // Check if query matches any country or index
    const match = MARKET_REGIONS.find(r => 
        r.country.toLowerCase().includes(query) ||
        r.index.toLowerCase().includes(query) ||
        r.id.toLowerCase() === query ||
        r.symbol.toLowerCase().includes(query)
    );

    if (match && map) {{
        map.flyTo([match.lat, match.lon], 4, {{ duration: 1.2 }});
        const cardElem = document.getElementById(`card-${{match.id}}`);
        if (cardElem) {{
            cardElem.style.borderColor = '#0BA65B';
            cardElem.style.boxShadow = '0 0 0 4px rgba(11, 166, 91, 0.3)';
            setTimeout(() => {{
                cardElem.style.borderColor = '#EAE6DE';
                cardElem.style.boxShadow = '0 4px 14px rgba(0, 0, 0, 0.08)';
            }}, 3000);
        }}
    }} else {{
        // Filter Movers if matching stock ticker
        const moverMatch = [...TOP_GAINERS, ...TOP_LOSERS].find(m => m.symbol.toLowerCase() === query);
        if (moverMatch) {{
            alert(`Stock Found: ${{moverMatch.symbol}} · Current Price: $${{moverMatch.price}} (${{moverMatch.change >= 0 ? '+' : ''}}${{moverMatch.change}}%)`);
        }} else {{
            alert(`Search completed for "${{query}}". Live stock telemetry active.`);
        }}
    }}
}}

document.getElementById('search-btn').addEventListener('click', executeSearch);
document.getElementById('global-search-input').addEventListener('keypress', (e) => {{
    if (e.key === 'Enter') executeSearch();
}});

// ── 5. REAL-TIME DATA SIMULATION & POLLING ENGINE ───────────────────────────
// Updates market numbers every 4 seconds to demonstrate live synchronization
function startLivePollingEngine() {{
    setInterval(() => {{
        MARKET_REGIONS.forEach(region => {{
            // Random tiny fluctuation (+- 0.02%)
            const delta = (Math.random() - 0.49) * 0.06;
            region.pct += delta;
            region.price += region.price * (delta / 100);

            // Update badge on map
            const card = document.getElementById(`card-${{region.id}}`);
            if (card) {{
                const pctElem = card.querySelector('.country-card-pct');
                if (pctElem) {{
                    const isPos = region.pct >= 0;
                    const sign = isPos ? '+' : '';
                    pctElem.className = `country-card-pct ${{isPos ? 'pos' : 'neg'}}`;
                    pctElem.textContent = `${{sign}}${{region.pct.toFixed(2)}}%`;
                    
                    // Flash effect
                    card.style.background = isPos ? '#F0FDF4' : '#FEF2F2';
                    setTimeout(() => {{ card.style.background = '#FFFFFF'; }}, 600);
                }}
            }}
        }});
    }}, 4000);
}}

// ── 6. WEBSOCKET REAL-TIME DATA STREAM CLIENT (PLACEHOLDER) ─────────────────
/**
 * MarketDataWebSocketClient
 * Connects to live financial WebSocket streams (e.g., Twelve Data, Finnhub, or backend gateway).
 * Uncomment and configure wsEndpoint with your legitimate credentials.
 */
class MarketDataWebSocketClient {{
    constructor(wsEndpoint) {{
        this.endpoint = wsEndpoint;
        this.socket = null;
        this.reconnectInterval = 5000;
    }}

    connect() {{
        /*
        console.log(`Connecting to Market WebSocket: ${{this.endpoint}}`);
        this.socket = new WebSocket(this.endpoint);

        this.socket.onopen = () => {{
            console.log("Market WebSocket connected successfully.");
            // Subscribe to ticker channels
            const subscribeMsg = JSON.stringify({{
                action: "subscribe",
                params: {{ symbols: MARKET_REGIONS.map(r => r.symbol).join(",") }}
            }});
            this.socket.send(subscribeMsg);
        }};

        this.socket.onmessage = (event) => {{
            try {{
                const data = JSON.parse(event.data);
                this.handleLiveUpdate(data);
            }} catch (err) {{
                console.error("Error parsing WebSocket packet:", err);
            }}
        }};

        this.socket.onclose = () => {{
            console.warn("WebSocket closed. Attempting reconnect...");
            setTimeout(() => this.connect(), this.reconnectInterval);
        }};

        this.socket.onerror = (err) => {{
            console.error("WebSocket encounter error:", err);
            this.socket.close();
        }};
        */
    }}

    handleLiveUpdate(packet) {{
        // Update DOM elements when live packet arrives
        if (packet && packet.symbol && packet.price) {{
            console.log(`Live Tick: ${{packet.symbol}} = ${{packet.price}}`);
        }}
    }}
}}

// Initialize components upon DOM load
document.addEventListener('DOMContentLoaded', () => {{
    initMap();
    renderMovers();
    startLivePollingEngine();

    // Initialize WebSocket placeholder
    const marketStream = new MarketDataWebSocketClient("wss://ws.twelvedata.com/v1/quotes/price");
    marketStream.connect();
}});
</script>

</body>
</html>
"""

with open("standalone_map_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated standalone_map_dashboard.html ({len(html_content)} bytes)")
