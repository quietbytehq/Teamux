#!/usr/bin/env python3
"""
Teamux v1.0.0 Picture-Based Visual User Guide PDF Generator
"""

import os
import sys
import base64
import subprocess

DOCS_DIR = "/home/faisal/projects/quietbyte/Teamux/docs"
ICON_PATH = "/home/faisal/projects/quietbyte/Teamux/assets/icon.png"
HTML_OUTPUT = os.path.join(DOCS_DIR, "Teamux_Visual_User_Guide_v1.0.0.html")
PDF_OUTPUT = os.path.join(DOCS_DIR, "Teamux_Visual_User_Guide_v1.0.0.pdf")
HOME_PDF = "/home/faisal/Teamux_Visual_User_Guide_v1.0.0.pdf"
GAMES_PDF = "/home/faisal/Games/Teamux_Visual_User_Guide_v1.0.0.pdf"

with open(ICON_PATH, "rb") as f:
    icon_b64 = base64.b64encode(f.read()).decode("utf-8")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Teamux v1.0.0 — Visual User Guide</title>
<style>
  @page {{
    size: A4;
    margin: 13mm 12mm 14mm 12mm;
    @bottom-left {{
      content: "Teamux v1.0.0 — Picture-Based Feature & User Guide";
      font-size: 8pt;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #64748b;
    }}
    @bottom-right {{
      content: "Page " counter(page) " of " counter(pages);
      font-size: 8pt;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #64748b;
    }}
  }}

  * {{ box-sizing: border-box; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.45;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  .page-break {{ page-break-before: always; }}
  .avoid-break {{ page-break-inside: avoid; }}

  /* Cover Header */
  .hero {{
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 55%, #3730a3 100%);
    color: #ffffff;
    border-radius: 12px;
    padding: 18px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
  }}
  .hero h1 {{
    margin: 0 0 4px 0;
    font-size: 21pt;
    color: #ffffff;
    border: none;
    padding: 0;
  }}
  .hero p {{
    margin: 0 0 10px 0;
    font-size: 10.5pt;
    color: #c7d2fe;
  }}
  .hero-badges {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }}
  .hero-badge {{
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 3px 9px;
    border-radius: 99px;
    font-size: 8pt;
    font-weight: 600;
    color: #f8fafc;
  }}
  .hero-logo {{
    width: 78px;
    height: 78px;
    border-radius: 16px;
    background: #fff;
    padding: 4px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.4);
  }}

  /* Section Headings */
  .sec-head {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14pt;
    font-weight: 800;
    color: #1e1b4b;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 5px;
    margin: 12px 0 10px 0;
  }}
  .sec-pill {{
    background: #4f46e5;
    color: #fff;
    font-size: 8pt;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 99px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }}

  /* Callout Number Pins */
  .pin {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #e11d48;
    color: #ffffff;
    font-size: 8pt;
    font-weight: 800;
    flex-shrink: 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.35);
    border: 1.5px solid #ffffff;
  }}
  .pin-inline {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 17px;
    height: 17px;
    border-radius: 50%;
    background: #e11d48;
    color: #ffffff;
    font-size: 8pt;
    font-weight: 800;
    margin-right: 4px;
    vertical-align: middle;
  }}

  /* Two-column UI + Explanation layout */
  .split {{
    display: grid;
    grid-template-columns: 330px 1fr;
    gap: 16px;
    align-items: start;
    margin: 8px 0 12px 0;
  }}
  .split-equal {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 8px 0 12px 0;
  }}

  /* Explain Cards */
  .explain-list {{
    display: flex;
    flex-direction: column;
    gap: 7px;
  }}
  .explain-item {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 7px 10px;
    font-size: 8.8pt;
  }}
  .explain-item strong {{
    color: #0f172a;
  }}
  .tip-box {{
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    border-radius: 6px;
    padding: 8px 11px;
    font-size: 8.8pt;
    color: #1e3a8a;
    margin-top: 8px;
  }}
  .warn-box {{
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    border-radius: 6px;
    padding: 8px 11px;
    font-size: 8.8pt;
    color: #92400e;
    margin-top: 8px;
  }}

  /* =========================================================
     PIXEL-ACCURATE TEAMUX STUDIO WIDGET MOCKUPS
     ========================================================= */
  .studio-card {{
    background: #141418;
    border: 1.5px solid rgba(99, 102, 241, 0.55);
    border-radius: 12px;
    width: 325px;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.35);
    color: #f4f4f5;
    overflow: hidden;
    font-size: 12px;
  }}
  .studio-header {{
    padding: 9px 12px;
    background: #24242a;
    border-bottom: 1px solid #3f3f46;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .studio-title {{
    font-size: 12.5px;
    font-weight: 700;
    color: #c7d2fe;
  }}
  .studio-min {{
    color: #a1a1aa;
    font-size: 15px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .studio-tabs {{
    display: flex;
    background: #1e1e24;
    border-bottom: 1px solid #3f3f46;
  }}
  .studio-tab {{
    flex: 1;
    padding: 7px 4px;
    font-size: 10.5px;
    font-weight: 600;
    text-align: center;
    color: #a1a1aa;
    border-bottom: 2px solid transparent;
  }}
  .studio-tab.active {{
    color: #818cf8;
    border-bottom-color: #6366f1;
    background: rgba(99, 102, 241, 0.12);
  }}
  .studio-body {{
    padding: 11px 12px;
    display: flex;
    flex-direction: column;
    gap: 9px;
  }}
  .t-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11.5px;
  }}
  .t-label {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .sw {{
    width: 36px;
    height: 19px;
    border-radius: 19px;
    background: #3f3f46;
    position: relative;
    flex-shrink: 0;
  }}
  .sw.on {{ background: #6366f1; }}
  .sw::after {{
    content: "";
    position: absolute;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background: #fff;
    top: 3px;
    left: 3px;
  }}
  .sw.on::after {{ left: 20px; }}
  .rng-group {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}
  .rng-lbl {{
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #a1a1aa;
  }}
  .rng-track {{
    height: 5px;
    border-radius: 5px;
    background: #3f3f46;
    position: relative;
  }}
  .rng-fill {{
    height: 100%;
    border-radius: 5px;
    background: #6366f1;
    position: relative;
  }}
  .rng-thumb {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #818cf8;
    border: 2px solid #fff;
    position: absolute;
    right: -6px;
    top: -3.5px;
  }}
  .btn-compare {{
    background: #27272a;
    border: 1px solid #3f3f46;
    color: #e4e4e7;
    padding: 7px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }}
  .btn-reset {{
    background: #1f1f23;
    border: 1px solid #3f3f46;
    color: #a1a1aa;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 10.5px;
    font-weight: 600;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
  }}
  .hint-box {{
    font-size: 10px;
    color: #94a3b8;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(51, 65, 85, 0.8);
    border-radius: 6px;
    padding: 6px 8px;
    line-height: 1.35;
  }}

  /* Theme Cards inside Studio Mockup */
  .theme-card {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 5px 8px;
    background: rgba(36, 36, 42, 0.85);
    border: 1px solid rgba(63, 63, 70, 0.6);
    border-radius: 7px;
  }}
  .theme-card.active {{
    background: rgba(99, 102, 241, 0.2);
    border-color: #818cf8;
  }}
  .theme-title {{ font-size: 11px; font-weight: 700; color: #f4f4f5; }}
  .theme-desc {{ font-size: 9px; color: #a1a1aa; }}
  .theme-badge {{
    font-size: 8.5px;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 8px;
    background: #4f46e5;
    color: #fff;
    margin-left: 4px;
  }}
  .swatches {{ display: flex; gap: 3px; }}
  .dot {{
    width: 11px;
    height: 11px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.3);
  }}

  /* Network Tab Mockup */
  .net-select {{
    width: 100%;
    background: #24242a;
    border: 1px solid #3f3f46;
    color: #f4f4f5;
    padding: 5px 8px;
    border-radius: 6px;
    font-size: 11px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .net-dash {{
    background: #18181b;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .net-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
  }}
  .net-stat {{
    background: #27272a;
    padding: 5px 7px;
    border-radius: 6px;
  }}
  .net-lbl {{ font-size: 9px; color: #a1a1aa; }}
  .net-val {{ font-size: 11.5px; font-weight: 700; color: #f4f4f5; }}
  .st-badge {{
    font-size: 9px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 8px;
    color: #fff;
  }}
  .st-good {{ background: #16a34a; }}
  .st-crit {{ background: #dc2626; }}

  /* Simulated Teams Window (Page 1) */
  .teams-mock {{
    background: #1f1f23;
    border-radius: 10px;
    border: 1px solid #334155;
    padding: 10px;
    position: relative;
    height: 285px;
    overflow: hidden;
    color: #e2e8f0;
  }}
  .teams-topbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #141418;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 8.5pt;
    margin-bottom: 8px;
  }}
  .call-banner-mock {{
    background: rgba(15, 23, 42, 0.95);
    border: 1.5px solid #22c55e;
    border-radius: 20px;
    padding: 4px 12px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 8pt;
    font-weight: 600;
    color: #fff;
  }}
  .call-pill-btn {{
    background: #22c55e;
    color: #0f172a;
    font-weight: 800;
    padding: 1px 7px;
    border-radius: 10px;
    font-size: 7.5pt;
  }}
  .video-grid-mock {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    height: 195px;
  }}
  .participant-box {{
    background: linear-gradient(145deg, #27272a, #18181b);
    border-radius: 8px;
    border: 1px solid #3f3f46;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
  }}
  .avatar-circle {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #4f46e5;
    color: #fff;
    font-weight: 800;
    font-size: 14pt;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .studio-pill-mock {{
    position: absolute;
    bottom: 12px;
    right: 12px;
    background: rgba(30, 27, 75, 0.95);
    border: 1.5px solid #818cf8;
    color: #fff;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 9pt;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }}
  .pill-net-tag {{
    background: rgba(255,255,255,0.18);
    padding: 1px 6px;
    border-radius: 8px;
    font-size: 7.5pt;
  }}

  /* Before / After Camera Mockup */
  .cam-compare {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 8px;
  }}
  .cam-frame {{
    border-radius: 8px;
    padding: 10px;
    text-align: center;
    border: 1px solid #cbd5e1;
  }}
  .cam-raw {{
    background: linear-gradient(180deg, #334155 0%, #1e293b 100%);
    color: #cbd5e1;
  }}
  .cam-studio {{
    background: radial-gradient(circle at 50% 42%, #475569 0%, #1e1b4b 75%, #09090b 100%);
    color: #f8fafc;
    border-color: #6366f1;
  }}
  .cam-face {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    margin: 6px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18pt;
  }}

  /* Theme Preview Mini Gallery */
  .theme-gallery {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 8px;
  }}
  .mini-app {{
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #cbd5e1;
    font-size: 8pt;
  }}
  .mini-app-bar {{
    padding: 4px 7px;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .mini-app-body {{
    display: grid;
    grid-template-columns: 34% 66%;
    height: 54px;
  }}
  .mini-side {{ padding: 5px; font-size: 7pt; }}
  .mini-main {{ padding: 5px; display: flex; flex-direction: column; justify-content: space-between; }}
  .mini-btn {{
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 6.5pt;
    font-weight: 700;
    align-self: flex-end;
  }}

  /* Audio-First Video Slate Mockup */
  .audio-slate {{
    background: #0f172a;
    border: 2px solid #ef4444;
    border-radius: 10px;
    height: 125px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 10px;
  }}

  /* Settings Window Mockup */
  .settings-mock {{
    background: #1e1e24;
    color: #f4f4f5;
    border-radius: 10px;
    padding: 12px;
    border: 1px solid #3f3f46;
    font-size: 8.5pt;
  }}
  .settings-sec {{
    background: #27272d;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 9px 11px;
    margin-bottom: 8px;
  }}
  .settings-sec h4 {{
    margin: 0 0 6px 0;
    color: #a5b4fc;
    font-size: 9pt;
    border-bottom: 1px solid #3f3f46;
    padding-bottom: 4px;
  }}
  .chk-row {{
    display: flex;
    align-items: center;
    gap: 7px;
    margin-bottom: 5px;
  }}
  .chk-box {{
    width: 14px;
    height: 14px;
    border-radius: 3px;
    background: #6366f1;
    color: #fff;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 9pt;
    font-weight: 800;
    flex-shrink: 0;
  }}

  /* Tier Flow Cards */
  .tier-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin: 8px 0;
  }}
  .tier-card {{
    border-radius: 8px;
    padding: 8px;
    border: 1px solid #cbd5e1;
    background: #f8fafc;
    font-size: 8.2pt;
  }}
  .tier-head {{
    font-weight: 800;
    font-size: 9pt;
    margin-bottom: 3px;
  }}

  /* Table */
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin: 8px 0;
  }}
  th, td {{
    padding: 6px 8px;
    border-bottom: 1px solid #e2e8f0;
    text-align: left;
  }}
  th {{
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
  }}
  tr:nth-child(even) td {{ background: #f8fafc; }}
</style>
</head>
<body>

<!-- ==================== PAGE 1: COVER & OVERVIEW ==================== -->
<div class="hero">
  <div>
    <h1>Teamux v1.0.0 — Visual User Guide</h1>
    <p>Picture-Based Guide to Camera Studio, App Themes &amp; Auto/Manual Bandwidth Control</p>
    <div class="hero-badges">
      <span class="hero-badge">✨ Studio Camera</span>
      <span class="hero-badge">🎭 6 Custom Themes</span>
      <span class="hero-badge">🌐 Auto &amp; Manual Bandwidth</span>
      <span class="hero-badge">🪟 Windows &amp; 🐧 Linux</span>
    </div>
  </div>
  <img class="hero-logo" src="data:image/png;base64,{icon_b64}" alt="Teamux">
</div>

<div class="sec-head"><span class="sec-pill">Overview</span> Where Everything Lives Inside Teamux</div>
<p>
  Teamux uses your regular <strong>Microsoft Teams</strong> account—all your chats, channels, and meetings are identical.
  On top of Teams, Teamux adds a floating <strong>Studio controller</strong> and an <strong>Active Call Banner</strong> right inside your window:
</p>

<div class="teams-mock avoid-break">
  <div class="teams-topbar">
    <span><strong>Microsoft Teams (Teamux)</strong> — Weekly Branch Sync</span>
    <div class="call-banner-mock">
      <span class="pin">1</span>
      <span>🟢 Active Call in Progress</span>
      <span class="call-pill-btn">RETURN TO MEETING</span>
    </div>
    <span>🔴 Leave</span>
  </div>

  <div class="video-grid-mock">
    <div class="participant-box">
      <div class="avatar-circle">A</div>
      <div style="margin-top:6px; font-size:8.5pt; font-weight:600;">Aleena (Branch Office)</div>
      <div style="font-size:7.5pt; color:#94a3b8;">🎤 Speaking...</div>
    </div>
    <div class="participant-box" style="border-color:#6366f1;">
      <div class="avatar-circle" style="background:#0ea5e9;">You</div>
      <div style="margin-top:6px; font-size:8.5pt; font-weight:600;">Your Camera (Studio Enhanced)</div>
      <div style="font-size:7.5pt; color:#a5b4fc;">✨ Beauty + Light Active</div>
    </div>
  </div>

  <div class="studio-pill-mock">
    <span class="pin">2</span>
    <span>✨ Studio</span>
    <span class="pill-net-tag">720p</span>
  </div>
</div>

<div class="split-equal" style="margin-top:10px;">
  <div class="explain-item">
    <span class="pin-inline">1</span><strong>Top Call &amp; Network Banner:</strong><br>
    Appears automatically during calls. Turns <strong>Green</strong> normally, <strong>Amber</strong> in Eco mode, and <strong>Red</strong> when Audio-First Protection engages. Click it anytime to jump straight back to your meeting screen.
  </div>
  <div class="explain-item">
    <span class="pin-inline">2</span><strong>Floating Studio Pill (Bottom-Right):</strong><br>
    Shows your current video quality badge (<code>720p</code>, <code>480p</code>, <code>360p</code>, or <code>Voice Only</code>). <strong>Click this pill</strong> anytime to open the 4-tab Studio Panel (Retouch, Tone, Themes, Network).
  </div>
</div>

<div class="split-equal">
  <div class="explain-item">
    <strong>⚙️ Preferences Shortcut (<code>Ctrl + ,</code>):</strong><br>
    Press <code>Ctrl + ,</code> (or right-click the System Tray icon &rarr; <em>Preferences</em>) to set your default Bandwidth Mode before joining a call.
  </div>
  <div class="explain-item">
    <strong>🚪 Quick Clean Exit (Double-Close):</strong><br>
    Click the window close button (<code>X</code>) <strong>twice within 2.5 seconds</strong> to force an instant, clean shutdown with zero background hanging.
  </div>
</div>

<!-- ==================== PAGE 2: CAMERA STUDIO - RETOUCH ==================== -->
<div class="page-break"></div>
<div class="sec-head"><span class="sec-pill">Camera Feature 1</span> Studio Retouch &amp; Hold-to-Compare</div>
<p>
  Click the floating <strong>✨ Studio</strong> pill in the bottom-right corner and stay on the <strong>✨ Retouch</strong> tab to improve how you look on camera—even on basic laptop webcams or in dimly lit offices.
</p>

<div class="split avoid-break">
  <!-- Studio Card Mockup: Retouch -->
  <div class="studio-card">
    <div class="studio-header">
      <div class="studio-title">✨ Teamux Studio</div>
      <div class="studio-min"><span class="pin">5</span> &minus;</div>
    </div>
    <div class="studio-tabs">
      <div class="studio-tab active">✨ Retouch</div>
      <div class="studio-tab">🎨 Tone</div>
      <div class="studio-tab">🎭 Themes</div>
      <div class="studio-tab">🌐 Network</div>
    </div>
    <div class="studio-body">
      <div class="t-row">
        <div class="t-label"><span class="pin">1</span><span>Beauty Filter</span></div>
        <div class="sw on"></div>
      </div>
      <div class="rng-group">
        <div class="rng-lbl"><span>Smoothness</span><span>55%</span></div>
        <div class="rng-track"><div class="rng-fill" style="width:55%;"><div class="rng-thumb"></div></div></div>
      </div>
      <div class="t-row">
        <div class="t-label"><span class="pin">2</span><span>Studio Lighting</span></div>
        <div class="sw on"></div>
      </div>
      <div class="t-row">
        <div class="t-label"><span class="pin">3</span><span>Portrait Focus (Vignette)</span></div>
        <div class="sw on"></div>
      </div>
      <div class="hint-box">💡 Custom BG &amp; Blur: Supported natively in Teams meeting under More &gt; Video effects.</div>
      <div class="btn-compare"><span class="pin">4</span><span>👁️ Hold to Compare</span></div>
    </div>
  </div>

  <!-- Explanations -->
  <div class="explain-list">
    <div class="explain-item">
      <span class="pin-inline">1</span><strong>Beauty Filter &amp; Smoothness (10%–100%):</strong><br>
      Turn this ON to softly smooth skin texture and reduce webcam graininess. Drag the <strong>Smoothness</strong> slider right for a stronger softening effect, or left for a subtle natural look.
    </div>
    <div class="explain-item">
      <span class="pin-inline">2</span><strong>Studio Lighting:</strong><br>
      Brightens dark shadows on your face automatically. Very helpful if you are sitting in a dim room or without a desk lamp.
    </div>
    <div class="explain-item">
      <span class="pin-inline">3</span><strong>Portrait Focus (Vignette):</strong><br>
      Adds a gentle dark fade around the outer edges of your video frame so attention stays centered on you.
    </div>
    <div class="explain-item">
      <span class="pin-inline">4</span><strong>👁️ Hold to Compare:</strong><br>
      Press and <strong>hold down</strong> this button to temporarily view your raw, unedited webcam feed. Let go to snap right back to your Studio settings.
    </div>
    <div class="explain-item">
      <span class="pin-inline">5</span><strong>Minimize (&minus;):</strong><br>
      Collapses the panel back into the small <code>✨ Studio</code> pill so it never blocks your meeting view. Your settings stay active!
    </div>
  </div>
</div>

<div class="cam-compare avoid-break">
  <div class="cam-frame cam-raw">
    <div style="font-weight:700; font-size:9pt;">BEFORE: Raw Webcam</div>
    <div class="cam-face" style="background:#475569;">😐</div>
    <div style="font-size:8pt; color:#94a3b8;">Dark shadows, flat lighting, webcam grain visible</div>
  </div>
  <div class="cam-frame cam-studio">
    <div style="font-weight:700; font-size:9pt; color:#a5b4fc;">AFTER: Studio Retouch + Lighting + Vignette</div>
    <div class="cam-face" style="background:#6366f1; box-shadow:0 0 18px rgba(129,140,248,0.6);">😊</div>
    <div style="font-size:8pt; color:#e0e7ff;">Brighter face, smooth skin tone, soft focused background border</div>
  </div>
</div>

<div class="tip-box">
  <strong>🔒 100% Private &amp; Saved Automatically:</strong> All camera effects run locally on your computer and are remembered for your next meeting. Everyone in the Teams call—and meeting recordings—sees your enhanced video.
</div>

<!-- ==================== PAGE 3: CAMERA STUDIO - TONE & COLOR ==================== -->
<div class="page-break"></div>
<div class="sec-head"><span class="sec-pill">Camera Feature 2</span> Tone &amp; Color Grading</div>
<p>
  Click the <strong>🎨 Tone</strong> tab at the top of the Studio panel to fix washed-out colors, harsh office fluorescent lighting, or bright windows behind you.
</p>

<div class="split avoid-break">
  <!-- Studio Card Mockup: Tone -->
  <div class="studio-card">
    <div class="studio-header">
      <div class="studio-title">✨ Teamux Studio</div>
      <div class="studio-min">&minus;</div>
    </div>
    <div class="studio-tabs">
      <div class="studio-tab">✨ Retouch</div>
      <div class="studio-tab active">🎨 Tone</div>
      <div class="studio-tab">🎭 Themes</div>
      <div class="studio-tab">🌐 Network</div>
    </div>
    <div class="studio-body">
      <div class="t-row">
        <div class="t-label"><span class="pin">1</span><span>Grayscale (Black &amp; White)</span></div>
        <div class="sw"></div>
      </div>
      <div class="rng-group">
        <div class="rng-lbl"><span><span class="pin-inline">2</span>Contrast</span><span>110%</span></div>
        <div class="rng-track"><div class="rng-fill" style="width:60%;"><div class="rng-thumb"></div></div></div>
      </div>
      <div class="rng-group">
        <div class="rng-lbl"><span><span class="pin-inline">3</span>Saturation</span><span>115%</span></div>
        <div class="rng-track"><div class="rng-fill" style="width:58%;"><div class="rng-thumb"></div></div></div>
      </div>
      <div class="rng-group">
        <div class="rng-lbl"><span><span class="pin-inline">4</span>Shadow Lift</span><span>+15</span></div>
        <div class="rng-track"><div class="rng-fill" style="width:65%;"><div class="rng-thumb"></div></div></div>
      </div>
      <div class="rng-group">
        <div class="rng-lbl"><span><span class="pin-inline">5</span>Ambience (Warm Glow)</span><span>25%</span></div>
        <div class="rng-track"><div class="rng-fill" style="width:25%;"><div class="rng-thumb"></div></div></div>
      </div>
      <div class="btn-reset"><span class="pin">6</span><span>↺ Reset Tone Adjustments</span></div>
      <div class="btn-compare"><span>👁️ Hold to Compare</span></div>
    </div>
  </div>

  <!-- Explanations -->
  <div class="explain-list">
    <div class="explain-item">
      <span class="pin-inline">1</span><strong>Grayscale (Black &amp; White):</strong><br>
      Switches your camera to a clean black-and-white look with one click (automatically disables the Saturation slider while active).
    </div>
    <div class="explain-item">
      <span class="pin-inline">2</span><strong>Contrast (50%–150%):</strong><br>
      Makes darks deeper and whites crisper. Slide to ~110% if your webcam looks hazy or washed out.
    </div>
    <div class="explain-item">
      <span class="pin-inline">3</span><strong>Saturation (0%–200%):</strong><br>
      Controls color richness. Increase slightly (110%–125%) for healthier natural color on dull webcams.
    </div>
    <div class="explain-item">
      <span class="pin-inline">4</span><strong>Shadow Lift (-50 to +50):</strong><br>
      Specifically brightens dark areas of your face without over-brightening the window or lights behind you.
    </div>
    <div class="explain-item">
      <span class="pin-inline">5</span><strong>Ambience / Warm Glow (0%–100%):</strong><br>
      Adds a warm golden tone to cancel out cold, bluish office LED or fluorescent lighting.
    </div>
    <div class="explain-item">
      <span class="pin-inline">6</span><strong>↺ Reset Tone Adjustments:</strong><br>
      Restores all 5 tone controls back to factory defaults immediately.
    </div>
  </div>
</div>

<!-- ==================== PAGE 4: APP THEMES ENGINE ==================== -->
<div class="page-break"></div>
<div class="sec-head"><span class="sec-pill">Appearance</span> Custom App Themes Engine (7 Styles)</div>
<p>
  Click the <strong>🎭 Themes</strong> tab to restyle the entire Microsoft Teams window (sidebars, chat bubbles, buttons, and backgrounds) in real time. Just click any theme card to switch—no restart required!
</p>

<div class="split avoid-break">
  <!-- Studio Card Mockup: Themes -->
  <div class="studio-card">
    <div class="studio-header">
      <div class="studio-title">✨ Teamux Studio</div>
      <div class="studio-min">&minus;</div>
    </div>
    <div class="studio-tabs">
      <div class="studio-tab">✨ Retouch</div>
      <div class="studio-tab">🎨 Tone</div>
      <div class="studio-tab active">🎭 Themes</div>
      <div class="studio-tab">🌐 Network</div>
    </div>
    <div class="studio-body" style="gap:6px;">
      <div style="font-size:10px; color:#a1a1aa;">Select an app theme to customize the look of Teams:</div>
      <div class="theme-card">
        <div><div class="theme-title">🖥️ Teams Default</div><div class="theme-desc">Microsoft Teams native appearance</div></div>
        <div class="swatches"><span class="dot" style="background:#201f1f"></span><span class="dot" style="background:#2d2c2c"></span><span class="dot" style="background:#6264a7"></span></div>
      </div>
      <div class="theme-card active">
        <div><div class="theme-title">🌌 OLED Midnight <span class="theme-badge">Active</span></div><div class="theme-desc">True pitch black with neon electric blue</div></div>
        <div class="swatches"><span class="dot" style="background:#000000"></span><span class="dot" style="background:#121212"></span><span class="dot" style="background:#38bdf8"></span></div>
      </div>
      <div class="theme-card">
        <div><div class="theme-title">☕ Catppuccin Mocha</div><div class="theme-desc">Soothing developer pastel &amp; mauve</div></div>
        <div class="swatches"><span class="dot" style="background:#1e1e2e"></span><span class="dot" style="background:#313244"></span><span class="dot" style="background:#cba6f7"></span></div>
      </div>
      <div class="theme-card">
        <div><div class="theme-title">❄️ Nord Frost</div><div class="theme-desc">Arctic slates &amp; crisp polar cyan</div></div>
        <div class="swatches"><span class="dot" style="background:#2e3440"></span><span class="dot" style="background:#3b4252"></span><span class="dot" style="background:#88c0d0"></span></div>
      </div>
      <div class="theme-card">
        <div><div class="theme-title">🌆 Tokyo Night</div><div class="theme-desc">Deep navy twilight &amp; neon cyan/magenta</div></div>
        <div class="swatches"><span class="dot" style="background:#1a1b26"></span><span class="dot" style="background:#24283b"></span><span class="dot" style="background:#7dcfff"></span></div>
      </div>
      <div class="theme-card">
        <div><div class="theme-title">🧛 Dracula</div><div class="theme-desc">Vampire dark slate &amp; vibrant neon pink</div></div>
        <div class="swatches"><span class="dot" style="background:#282a36"></span><span class="dot" style="background:#44475a"></span><span class="dot" style="background:#ff79c6"></span></div>
      </div>
      <div class="theme-card">
        <div><div class="theme-title">🌸 Rosé Pine</div><div class="theme-desc">Cozy warm dusk &amp; delicate rose gold</div></div>
        <div class="swatches"><span class="dot" style="background:#191724"></span><span class="dot" style="background:#26233a"></span><span class="dot" style="background:#ebbcba"></span></div>
      </div>
    </div>
  </div>

  <div class="explain-list">
    <div class="explain-item">
      <strong>Step 1:</strong> Click <strong>✨ Studio</strong> &rarr; <strong>🎭 Themes</strong>.
    </div>
    <div class="explain-item">
      <strong>Step 2:</strong> Click any theme card. Teams updates <strong>instantly</strong> and remembers your choice every time you reopen Teamux.
    </div>
    <div class="explain-item">
      <strong>Which Theme Should I Pick?</strong>
      <ul style="margin:4px 0 0 16px; padding:0;">
        <li><strong>🌌 OLED Midnight:</strong> Pure black background—saves laptop battery and eliminates screen glare.</li>
        <li><strong>☕ Catppuccin / 🌸 Rosé Pine:</strong> Soft warm colors to reduce eye strain during 8-hour workdays.</li>
        <li><strong>❄️ Nord / 🌆 Tokyo Night / 🧛 Dracula:</strong> Crisp high-contrast palettes for sharp text readability.</li>
        <li><strong>🖥️ Teams Default:</strong> Reverts back to standard Microsoft Teams colors anytime.</li>
      </ul>
    </div>
  </div>
</div>

<div style="font-weight:700; font-size:9.5pt; color:#1e1b4b; margin-top:6px;">Visual Theme Preview Gallery (How Teams Looks in Each Theme):</div>
<div class="theme-gallery avoid-break">
  <div class="mini-app" style="border-color:#262626;">
    <div class="mini-app-bar" style="background:#080808; color:#fff;"><span>🌌 OLED Midnight</span><span style="color:#38bdf8;">●</span></div>
    <div class="mini-app-body">
      <div class="mini-side" style="background:#080808; color:#a3a3a3;"># General<br># Branch</div>
      <div class="mini-main" style="background:#000000; color:#fff;"><span>Hi team!</span><span class="mini-btn" style="background:#38bdf8; color:#000;">Join</span></div>
    </div>
  </div>
  <div class="mini-app" style="border-color:#313244;">
    <div class="mini-app-bar" style="background:#181825; color:#cdd6f4;"><span>☕ Catppuccin</span><span style="color:#cba6f7;">●</span></div>
    <div class="mini-app-body">
      <div class="mini-side" style="background:#181825; color:#a6adc8;"># General<br># Branch</div>
      <div class="mini-main" style="background:#1e1e2e; color:#cdd6f4;"><span>Hi team!</span><span class="mini-btn" style="background:#cba6f7; color:#111;">Join</span></div>
    </div>
  </div>
  <div class="mini-app" style="border-color:#434c5e;">
    <div class="mini-app-bar" style="background:#242933; color:#eceff4;"><span>❄️ Nord Frost</span><span style="color:#88c0d0;">●</span></div>
    <div class="mini-app-body">
      <div class="mini-side" style="background:#242933; color:#d8dee9;"># General<br># Branch</div>
      <div class="mini-main" style="background:#2e3440; color:#eceff4;"><span>Hi team!</span><span class="mini-btn" style="background:#88c0d0; color:#111;">Join</span></div>
    </div>
  </div>
  <div class="mini-app" style="border-color:#292e42;">
    <div class="mini-app-bar" style="background:#16161e; color:#c0caf5;"><span>🌆 Tokyo Night</span><span style="color:#7dcfff;">●</span></div>
    <div class="mini-app-body">
      <div class="mini-side" style="background:#16161e; color:#787c99;"># General<br># Branch</div>
      <div class="mini-main" style="background:#1a1b26; color:#c0caf5;"><span>Hi team!</span><span class="mini-btn" style="background:#7dcfff; color:#111;">Join</span></div>
    </div>
  </div>
  <div class="mini-app" style="border-color:#44475a;">
    <div class="mini-app-bar" style="background:#1e1f29; color:#f8f8f2;"><span>🧛 Dracula</span><span style="color:#ff79c6;">●</span></div>
    <div class="mini-app-body">
      <div class="mini-side" style="background:#1e1f29; color:#d6d6d4;"># General<br># Branch</div>
      <div class="mini-main" style="background:#282a36; color:#f8f8f2;"><span>Hi team!</span><span class="mini-btn" style="background:#ff79c6; color:#111;">Join</span></div>
    </div>
  </div>
  <div class="mini-app" style="border-color:#403d52;">
    <div class="mini-app-bar" style="background:#14121e; color:#e0def4;"><span>🌸 Rosé Pine</span><span style="color:#ebbcba;">●</span></div>
    <div class="mini-app-body">
      <div class="mini-side" style="background:#14121e; color:#908caa;"># General<br># Branch</div>
      <div class="mini-main" style="background:#191724; color:#e0def4;"><span>Hi team!</span><span class="mini-btn" style="background:#ebbcba; color:#111;">Join</span></div>
    </div>
  </div>
</div>

<!-- ==================== PAGE 5: BANDWIDTH CONTROL - AUTO MODE ==================== -->
<div class="page-break"></div>
<div class="sec-head"><span class="sec-pill">Bandwidth Control</span> Auto Mode (Adaptive Network Guardian)</div>
<p>
  On slow branch-office internet links, high-definition video uses up all available upload speed—causing robotic audio and dropped calls. Teamux gives you <strong>Auto Mode</strong> (automatic protection) and <strong>Manual Mode</strong> (lock a fixed speed).
</p>

<div class="split avoid-break">
  <!-- Studio Card Mockup: Network -->
  <div class="studio-card">
    <div class="studio-header">
      <div class="studio-title">✨ Teamux Studio</div>
      <div class="studio-min">&minus;</div>
    </div>
    <div class="studio-tabs">
      <div class="studio-tab">✨ Retouch</div>
      <div class="studio-tab">🎨 Tone</div>
      <div class="studio-tab">🎭 Themes</div>
      <div class="studio-tab active">🌐 Network</div>
    </div>
    <div class="studio-body">
      <div class="t-row">
        <div class="t-label"><span class="pin">1</span><span>Adaptive Guardian</span></div>
        <div class="sw on"></div>
      </div>
      <div class="rng-group">
        <div class="rng-lbl"><span><span class="pin-inline">2</span>Bandwidth Profile</span></div>
        <div class="net-select"><span>Auto (Dynamic Guardian)</span><span>&#9662;</span></div>
      </div>
      <div class="net-dash">
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:10.5px; font-weight:700;">
          <span><span class="pin-inline">3</span>Live WebRTC Telemetry</span>
          <span class="st-badge st-good">Optimal</span>
        </div>
        <div class="net-grid">
          <div class="net-stat"><div class="net-lbl">Latency (RTT)</div><div class="net-val">42 ms</div></div>
          <div class="net-stat"><div class="net-lbl">Packet Loss</div><div class="net-val">0%</div></div>
          <div class="net-stat"><div class="net-lbl">Est. Bandwidth</div><div class="net-val">2400 kbps</div></div>
          <div class="net-stat"><div class="net-lbl">Active Video Stream</div><div class="net-val">🚀 720p</div></div>
        </div>
      </div>
      <div class="hint-box">🛡️ When branch network is constrained, video throttles automatically to guarantee 100% voice clarity.</div>
    </div>
  </div>

  <!-- Explanations -->
  <div class="explain-list">
    <div class="explain-item">
      <span class="pin-inline">1</span><strong>Adaptive Guardian Switch (Default: ON):</strong><br>
      Enables automatic internet monitoring. Teamux checks your connection health every <strong>2.5 seconds</strong> during a call.
    </div>
    <div class="explain-item">
      <span class="pin-inline">2</span><strong>Bandwidth Profile Dropdown:</strong><br>
      Leave on <strong>Auto (Dynamic Guardian)</strong> for automatic adjustments, or open this dropdown to switch to <strong>Manual Mode</strong> (720p, 480p, 360p, or Audio-First).
    </div>
    <div class="explain-item">
      <span class="pin-inline">3</span><strong>Live WebRTC Telemetry Dashboard:</strong><br>
      Shows your live call health at a glance:
      <ul style="margin:3px 0 0 15px; padding:0;">
        <li><strong>Latency (RTT):</strong> Connection delay in milliseconds (lower is better).</li>
        <li><strong>Packet Loss:</strong> Percentage of lost data (turns red if &gt; 5%).</li>
        <li><strong>Est. Bandwidth:</strong> Available upload speed in kbps.</li>
        <li><strong>Active Video Stream:</strong> The quality tier currently being sent.</li>
      </ul>
    </div>
  </div>
</div>

<div style="font-weight:700; font-size:9.5pt; color:#1e1b4b; margin-top:6px;">How Auto Mode Steps Down &amp; Recovers Automatically:</div>
<div class="tier-row avoid-break">
  <div class="tier-card" style="border-top:4px solid #2563eb;">
    <div class="tier-head" style="color:#1d4ed8;">🚀 1. Full HD (720p)</div>
    <div><strong>Speed:</strong> ~2.0 Mbps (30 FPS)</div>
    <div><strong>When:</strong> Ping &lt; 130ms, Loss &lt; 2%</div>
    <div style="color:#475569; margin-top:3px;">Normal crystal-clear HD video.</div>
  </div>
  <div class="tier-card" style="border-top:4px solid #10b981;">
    <div class="tier-head" style="color:#047857;">⚖️ 2. Balanced (480p)</div>
    <div><strong>Speed:</strong> ~500 kbps (20 FPS)</div>
    <div><strong>When:</strong> Ping 130–260ms or Loss 2–6%</div>
    <div style="color:#475569; margin-top:3px;">Uses <strong>75% less data</strong> while keeping faces sharp.</div>
  </div>
  <div class="tier-card" style="border-top:4px solid #f59e0b;">
    <div class="tier-head" style="color:#b45309;">📉 3. Eco Saver (360p)</div>
    <div><strong>Speed:</strong> ~250 kbps (15 FPS)</div>
    <div><strong>When:</strong> Ping 260–500ms or Loss 6–15%</div>
    <div style="color:#475569; margin-top:3px;">Uses <strong>87% less data</strong> for congested links.</div>
  </div>
  <div class="tier-card" style="border-top:4px solid #dc2626; background:#fef2f2;">
    <div class="tier-head" style="color:#b91c1c;">🔴 4. Audio-First</div>
    <div><strong>Speed:</strong> ~0 kbps video (1 FPS)</div>
    <div><strong>When:</strong> Ping &gt; 500ms or Loss &gt; 15%</div>
    <div style="color:#7f1d1d; margin-top:3px;">Pauses video so <strong>100% of internet goes to voice!</strong></div>
  </div>
</div>

<div class="tip-box">
  <strong>🔄 Smart Auto-Recovery (No Flickering):</strong> When your internet gets slow, Teamux drops quality <em>immediately</em> to save your voice call. When your internet improves, it waits for <strong>3 clean checks in a row (~7.5 seconds)</strong> before turning HD video back on so your screen doesn't flicker back and forth.
</div>

<!-- ==================== PAGE 6: AUDIO-FIRST & MANUAL MODE ==================== -->
<div class="page-break"></div>
<div class="sec-head"><span class="sec-pill">Audio Protection &amp; Manual Mode</span> Audio-First Screen &amp; Manual Presets</div>

<p>
  When your branch internet becomes severely congested (or if you manually choose <strong>Audio-First Priority</strong>), Teamux replaces your camera video with a clean status card so other people in the meeting know your voice is still active:
</p>

<div class="split-equal avoid-break">
  <div>
    <div style="font-weight:700; font-size:8.8pt; margin-bottom:4px; color:#b91c1c;">What Meeting Attendees See on Your Video Tile:</div>
    <div class="audio-slate">
      <div style="color:#ef4444; font-weight:800; font-size:12pt; margin-bottom:5px;">🔴 Audio-First Mode Active</div>
      <div style="color:#94a3b8; font-size:8.5pt;">Video upload paused to protect voice audio quality.</div>
      <div style="color:#94a3b8; font-size:8.5pt;">Resuming automatically when network clears.</div>
    </div>
  </div>
  <div>
    <div style="font-weight:700; font-size:8.8pt; margin-bottom:4px; color:#b91c1c;">What You See on Your Screen:</div>
    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:10px; height:125px; display:flex; flex-direction:column; justify-content:space-between;">
      <div class="call-banner-mock" style="border-color:#ef4444; width:100%; justify-content:space-between;">
        <span>🔴 Audio-First Protection Active (Low Bandwidth)</span>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:8pt; color:#475569;">Studio Pill turns red:</span>
        <div class="studio-pill-mock" style="position:static; padding:4px 10px;">
          <span>✨ Studio</span>
          <span class="pill-net-tag" style="background:#dc2626;">Voice Only</span>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="sec-head" style="margin-top:14px;"><span class="sec-pill">Manual Mode</span> How to Lock Bandwidth Speed Manually (2 Ways)</div>
<p>
  If you work from a site that is <strong>always</strong> on slow internet, you don't have to wait for Auto Mode to react—you can manually lock your video speed either <strong>during a call</strong> or <strong>permanently in Preferences</strong>:
</p>

<div class="split-equal avoid-break">
  <!-- Way 1: In-Meeting -->
  <div class="explain-item" style="background:#fff; border-color:#cbd5e1;">
    <div style="font-weight:800; color:#1e1b4b; font-size:9.5pt; margin-bottom:6px;">Option A: Change Live Inside a Meeting</div>
    <ol style="margin:0 0 8px 16px; padding:0; line-height:1.5;">
      <li>Click the <strong>✨ Studio</strong> pill &rarr; <strong>🌐 Network</strong> tab.</li>
      <li>Click the <strong>Bandwidth Profile</strong> dropdown.</li>
      <li>Pick any fixed preset:
        <ul style="margin:3px 0 3px 14px; padding:0;">
          <li><code>Auto (Dynamic Guardian)</code> — Recommended default</li>
          <li><code>720p Full HD (~2.0 Mbps)</code> — Force max HD</li>
          <li><code>480p Balanced (~500 kbps)</code> — Good for shared office Wi-Fi</li>
          <li><code>360p Eco Saver (~250 kbps)</code> — Best for slow branch lines</li>
          <li><code>Audio-First Priority (~30 kbps)</code> — Voice only, camera paused</li>
        </ul>
      </li>
    </ol>
    <div style="font-size:8pt; color:#475569;">Takes effect immediately without leaving the call!</div>
  </div>

  <!-- Way 2: Preferences Window -->
  <div class="settings-mock">
    <div style="font-weight:800; color:#c7d2fe; font-size:9.5pt; margin-bottom:6px;">Option B: Set Permanently in Preferences (<code>Ctrl + ,</code>)</div>
    <div class="settings-sec">
      <h4>Network &amp; Bandwidth Guardian</h4>
      <div class="chk-row">
        <span class="chk-box">&#10003;</span>
        <span>Adaptive Network Guardian (Auto-Throttle video when connection slows)</span>
      </div>
      <div style="margin-top:7px;">
        <div style="color:#a1a1aa; font-size:8pt; margin-bottom:3px;">Default Video Bandwidth Mode:</div>
        <div class="net-select" style="background:#18181b;">
          <span>Eco Bandwidth Saver (360p @ 15 FPS / ~250 kbps)</span>
          <span>&#9662;</span>
        </div>
      </div>
    </div>
    <div style="display:flex; justify-content:flex-end; gap:6px; margin-top:6px;">
      <span style="background:#3f3f46; padding:4px 10px; border-radius:5px;">Cancel</span>
      <span style="background:#4f46e5; padding:4px 10px; border-radius:5px; font-weight:700;">Save &amp; Apply</span>
    </div>
  </div>
</div>

<!-- ==================== PAGE 7: CHEAT SHEET ==================== -->
<div class="page-break"></div>
<div class="sec-head"><span class="sec-pill">Quick Reference</span> Everyday Cheat Sheet</div>

<table>
  <thead>
    <tr>
      <th>What You Want To Do</th>
      <th>Where To Click</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Smooth skin, brighten dark webcam, or focus portrait</strong></td>
      <td>Floating <strong>✨ Studio</strong> pill &rarr; <strong>✨ Retouch</strong> tab</td>
    </tr>
    <tr>
      <td><strong>Compare your edited camera vs. raw camera</strong></td>
      <td>Press &amp; hold <strong>👁️ Hold to Compare</strong> at bottom of Studio</td>
    </tr>
    <tr>
      <td><strong>Fix washed-out colors or switch to Black &amp; White</strong></td>
      <td>Floating <strong>✨ Studio</strong> pill &rarr; <strong>🎨 Tone</strong> tab</td>
    </tr>
    <tr>
      <td><strong>Change Teams to OLED Black, Catppuccin, Nord, etc.</strong></td>
      <td>Floating <strong>✨ Studio</strong> pill &rarr; <strong>🎭 Themes</strong> tab &rarr; Click theme</td>
    </tr>
    <tr>
      <td><strong>Check live ping, packet loss, or internet speed in a call</strong></td>
      <td>Floating <strong>✨ Studio</strong> pill &rarr; <strong>🌐 Network</strong> tab</td>
    </tr>
    <tr>
      <td><strong>Switch between Auto and Manual bandwidth mode</strong></td>
      <td><strong>🌐 Network</strong> tab &rarr; <strong>Bandwidth Profile</strong> dropdown (or <code>Ctrl + ,</code>)</td>
    </tr>
    <tr>
      <td><strong>Jump back to an active call window</strong></td>
      <td>Click the top <strong>RETURN TO MEETING</strong> banner</td>
    </tr>
    <tr>
      <td><strong>Force instant app exit with no hanging</strong></td>
      <td>Click window <strong>X</strong> twice within 2.5 seconds (or Tray &rarr; <strong>Quit Teamux</strong>)</td>
    </tr>
  </tbody>
</table>

<div class="warn-box avoid-break">
  <strong>🏢 Recommended Settings for Slow Branch Offices:</strong><br>
  If a branch office has slow or shared internet (&lt; 2 Mbps upload), open <strong>Preferences (<code>Ctrl + ,</code>)</strong>, keep <strong>Adaptive Network Guardian</strong> checked, and set Default Video Bandwidth Mode to <strong>Auto Adaptive</strong> (or lock <strong>360p Eco Saver</strong> for consistent low data usage).
</div>

<div class="tip-box avoid-break" style="margin-top:12px;">
  <strong>📥 Official Downloads &amp; Support:</strong><br>
  &bull; <strong>Releases Page:</strong> https://github.com/quietbytehq/teamux/releases/tag/v1.0.0<br>
  &bull; <strong>Windows Portable (.exe):</strong> No installation or admin rights needed—just double-click to run.<br>
  &bull; <strong>Linux AppImage:</strong> Mark executable (<code>chmod +x</code>) and launch directly.
</div>

<div style="margin-top:18px; padding:10px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; font-size:8pt; color:#64748b; text-align:center;">
  <strong>Disclaimer:</strong> Teamux is an unofficial open-source project by Quiet Byte and is not affiliated with or endorsed by Microsoft. Microsoft Teams is a trademark of Microsoft Corporation.
</div>

</body>
</html>
"""

with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML generated: {HTML_OUTPUT}")

cmd = [
    "/snap/bin/chromium",
    "--headless",
    "--no-sandbox",
    "--disable-gpu",
    f"--print-to-pdf={PDF_OUTPUT}",
    "--print-to-pdf-no-header",
    HTML_OUTPUT,
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Error generating PDF:", res.stderr)
    sys.exit(1)

print(f"PDF generated: {PDF_OUTPUT}")
subprocess.run(["cp", PDF_OUTPUT, HOME_PDF], check=True)
print(f"Copied to: {HOME_PDF}")
if os.path.exists("/home/faisal/Games"):
    subprocess.run(["cp", PDF_OUTPUT, GAMES_PDF], check=True)
    print(f"Copied to: {GAMES_PDF}")
