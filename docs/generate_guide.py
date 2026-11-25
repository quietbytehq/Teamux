#!/usr/bin/env python3
"""
Teamux v1.0.0 Official User Guide & Picture-Based Feature Manual PDF Generator
Authored by Quiet Byte (2026)
"""

import os
import sys
import base64
import subprocess

DOCS_DIR = "/home/faisal/projects/quietbyte/Teamux/docs"
ICON_PATH = "/home/faisal/projects/quietbyte/Teamux/assets/icon.png"
HTML_OUTPUT = os.path.join(DOCS_DIR, "Teamux_User_Guide_v1.0.0.html")
PDF_OUTPUT = os.path.join(DOCS_DIR, "Teamux_User_Guide_v1.0.0.pdf")
USER_PDF_COPY = "/home/faisal/Teamux_User_Guide_v1.0.0.pdf"
GAMES_PDF_COPY = "/home/faisal/Games/Teamux_User_Guide_v1.0.0.pdf"

with open(ICON_PATH, "rb") as f:
    icon_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Teamux v1.0.0 — Official User Guide &amp; Feature Manual</title>
<style>
  @page {{
    size: A4;
    margin: 10mm 11mm 11mm 11mm;
    @bottom-right {{
      content: "Page " counter(page) " of " counter(pages);
      font-size: 8pt;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #64748b;
    }}
    @bottom-left {{
      content: "Teamux v1.0.0 — Official User Guide (Quiet Byte)";
      font-size: 8pt;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #64748b;
    }}
  }}

  * {{ box-sizing: border-box; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.33;
    font-size: 8.8pt;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  .avoid-break {{ page-break-inside: avoid; }}

  /* Cover / Header Section */
  .cover-header {{
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #312e81 100%);
    color: #ffffff;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .cover-info {{ max-width: 74%; }}
  .cover-title {{
    font-size: 22pt;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0 0 3px 0;
    color: #ffffff;
  }}
  .cover-subtitle {{
    font-size: 11pt;
    font-weight: 400;
    color: #c7d2fe;
    margin: 0 0 10px 0;
    line-height: 1.3;
  }}
  .cover-meta {{
    font-size: 8pt;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }}
  .cover-meta span {{
    background: rgba(255, 255, 255, 0.14);
    padding: 3px 8px;
    border-radius: 6px;
    color: #f8fafc;
    font-weight: 500;
  }}
  .cover-logo {{
    width: 82px;
    height: 82px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    background: #ffffff;
    padding: 4px;
  }}

  /* Typography */
  h1, h2, h3, h4 {{
    color: #0f172a;
    font-weight: 700;
    margin-top: 7px;
    margin-bottom: 3px;
    page-break-after: avoid;
  }}
  h1 {{
    font-size: 13.5pt;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 3px;
    color: #1e1b4b;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  h2 {{
    font-size: 10.8pt;
    color: #312e81;
    margin-top: 8px;
  }}
  p {{ margin: 0 0 4px 0; }}
  ul, ol {{ margin: 3px 0 4px 0; padding-left: 16px; }}
  li {{ margin-bottom: 1.5px; }}

  /* Callout Boxes */
  .callout {{
    padding: 8px 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 9pt;
    line-height: 1.4;
  }}
  .callout-info {{ background: #eff6ff; border-left: 4px solid #3b82f6; color: #1e40af; }}
  .callout-warning {{ background: #fffbeb; border-left: 4px solid #f59e0b; color: #92400e; }}

  /* Step Boxes */
  .step-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 9px 12px;
    margin-bottom: 8px;
  }}
  .step-title {{
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 10pt;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 4px;
  }}
  .step-badge {{
    background: #4f46e5;
    color: #ffffff;
    font-size: 8pt;
    font-weight: 800;
    width: 19px;
    height: 19px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  /* Feature Grid */
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin: 8px 0;
  }}
  .card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 9px 11px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  }}
  .card-title {{
    font-size: 10pt;
    font-weight: 700;
    color: #1e1b4b;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .card-body {{ font-size: 8.8pt; color: #475569; line-height: 1.4; }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 8.6pt;
  }}
  th, td {{
    padding: 3.5px 7px;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
  }}
  th {{
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 700;
    font-size: 8pt;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }}
  tr:nth-child(even) td {{ background: #f8fafc; }}

  /* Code Blocks */
  code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 8.3pt;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 4px;
    color: #334155;
  }}
  pre {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 8.2pt;
    background: #0f172a;
    color: #e2e8f0;
    padding: 7px 10px;
    border-radius: 6px;
    margin: 5px 0;
    line-height: 1.35;
    white-space: pre-wrap;
  }}

  /* Status Badges */
  .badge {{
    display: inline-block;
    padding: 2px 6px;
    border-radius: 10px;
    font-size: 7.8pt;
    font-weight: 700;
    color: white;
    white-space: nowrap;
  }}
  .badge-720p {{ background: #2563eb; }}
  .badge-480p {{ background: #059669; }}
  .badge-360p {{ background: #d97706; }}
  .badge-audio {{ background: #dc2626; }}

  /* Callout Pins for Picture-Based UI Diagrams */
  .pin {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 17px;
    height: 17px;
    border-radius: 50%;
    background: #e11d48;
    color: #ffffff;
    font-size: 7.8pt;
    font-weight: 800;
    flex-shrink: 0;
    border: 1.5px solid #ffffff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.35);
  }}
  .pin-inline {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #e11d48;
    color: #ffffff;
    font-size: 7.5pt;
    font-weight: 800;
    margin-right: 4px;
    vertical-align: middle;
  }}

  /* Visual UI Split Layout */
  .ui-split {{
    display: grid;
    grid-template-columns: 305px 1fr;
    gap: 12px;
    align-items: start;
    margin: 7px 0 10px 0;
  }}
  .explain-stack {{
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}
  .explain-item {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 7px;
    padding: 6px 9px;
    font-size: 8.6pt;
    line-height: 1.38;
  }}

  /* Pixel-Accurate Teamux Studio Mockups */
  .studio-card {{
    background: #141418;
    border: 1.5px solid rgba(99, 102, 241, 0.55);
    border-radius: 10px;
    width: 305px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.25);
    color: #f4f4f5;
    overflow: hidden;
    font-size: 11px;
  }}
  .studio-header {{
    padding: 7px 11px;
    background: #24242a;
    border-bottom: 1px solid #3f3f46;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .studio-title {{ font-size: 11.5px; font-weight: 700; color: #c7d2fe; }}
  .studio-min {{ color: #a1a1aa; font-size: 14px; font-weight: 700; display: flex; align-items: center; gap: 4px; }}
  .studio-tabs {{
    display: flex;
    background: #1e1e24;
    border-bottom: 1px solid #3f3f46;
  }}
  .studio-tab {{
    flex: 1;
    padding: 6px 3px;
    font-size: 10px;
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
    padding: 7px 9px;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}
  .t-row {{ display: flex; align-items: center; justify-content: space-between; font-size: 11px; }}
  .t-label {{ display: flex; align-items: center; gap: 5px; }}
  .sw {{
    width: 34px; height: 18px; border-radius: 18px; background: #3f3f46; position: relative; flex-shrink: 0;
  }}
  .sw.on {{ background: #6366f1; }}
  .sw::after {{
    content: ""; position: absolute; width: 12px; height: 12px; border-radius: 50%; background: #fff; top: 3px; left: 3px;
  }}
  .sw.on::after {{ left: 19px; }}
  .rng-group {{ display: flex; flex-direction: column; gap: 3px; }}
  .rng-lbl {{ display: flex; justify-content: space-between; font-size: 10.5px; color: #a1a1aa; }}
  .rng-track {{ height: 4.5px; border-radius: 5px; background: #3f3f46; position: relative; }}
  .rng-fill {{ height: 100%; border-radius: 5px; background: #6366f1; position: relative; }}
  .rng-thumb {{
    width: 11px; height: 11px; border-radius: 50%; background: #818cf8; border: 2px solid #fff;
    position: absolute; right: -5px; top: -3.2px;
  }}
  .btn-compare {{
    background: #27272a; border: 1px solid #3f3f46; color: #e4e4e7;
    padding: 6px 8px; border-radius: 6px; font-size: 10.5px; font-weight: 600;
    display: flex; align-items: center; justify-content: center; gap: 5px;
  }}
  .btn-reset {{
    background: #1f1f23; border: 1px solid #3f3f46; color: #a1a1aa;
    padding: 4px 8px; border-radius: 6px; font-size: 10px; font-weight: 600;
    display: flex; align-items: center; justify-content: center; gap: 5px;
  }}
  .hint-box-dark {{
    font-size: 9.5px; color: #94a3b8; background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(51, 65, 85, 0.8); border-radius: 5px; padding: 5px 7px; line-height: 1.3;
  }}
  .net-select {{
    width: 100%; background: #24242a; border: 1px solid #3f3f46; color: #f4f4f5;
    padding: 4px 7px; border-radius: 5px; font-size: 10.5px;
    display: flex; justify-content: space-between; align-items: center;
  }}
  .net-dash {{
    background: #18181b; border: 1px solid #3f3f46; border-radius: 7px; padding: 7px;
    display: flex; flex-direction: column; gap: 5px;
  }}
  .net-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4px; }}
  .net-stat {{ background: #27272a; padding: 4px 6px; border-radius: 5px; }}
  .net-lbl {{ font-size: 8.5px; color: #a1a1aa; }}
  .net-val {{ font-size: 11px; font-weight: 700; color: #f4f4f5; }}
  .st-badge {{ font-size: 8.5px; font-weight: 700; padding: 1.5px 5px; border-radius: 7px; color: #fff; background: #16a34a; }}

  /* Theme Cards inside Mockup */
  .theme-card {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 3px 6px; background: rgba(36, 36, 42, 0.85);
    border: 1px solid rgba(63, 63, 70, 0.6); border-radius: 6px;
  }}
  .theme-card.active {{ background: rgba(99, 102, 241, 0.2); border-color: #818cf8; }}
  .theme-title {{ font-size: 10.5px; font-weight: 700; color: #f4f4f5; }}
  .theme-desc {{ font-size: 8.5px; color: #a1a1aa; }}
  .theme-badge {{ font-size: 8px; font-weight: 700; padding: 1px 4px; border-radius: 7px; background: #4f46e5; color: #fff; margin-left: 3px; }}
  .swatches {{ display: flex; gap: 3px; }}
  .dot {{ width: 10px; height: 10px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.3); }}

  /* Simulated Teams Window & Visuals */
  .teams-mock {{
    background: #1f1f23; border-radius: 9px; border: 1px solid #334155;
    padding: 8px; position: relative; height: 170px; color: #e2e8f0; margin: 7px 0;
  }}
  .teams-topbar {{
    display: flex; justify-content: space-between; align-items: center;
    background: #141418; padding: 4px 9px; border-radius: 5px; font-size: 8pt; margin-bottom: 6px;
  }}
  .call-banner-mock {{
    background: rgba(15, 23, 42, 0.95); border: 1.5px solid #22c55e; border-radius: 16px;
    padding: 2px 9px; display: inline-flex; align-items: center; gap: 6px; font-size: 7.8pt; font-weight: 600; color: #fff;
  }}
  .call-pill-btn {{
    background: #22c55e; color: #0f172a; font-weight: 800; padding: 1px 6px; border-radius: 8px; font-size: 7pt;
  }}
  .video-grid-mock {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7px; height: 110px; }}
  .participant-box {{
    background: linear-gradient(145deg, #27272a, #18181b); border-radius: 7px; border: 1px solid #3f3f46;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
  }}
  .avatar-circle {{
    width: 34px; height: 34px; border-radius: 50%; background: #4f46e5; color: #fff;
    font-weight: 800; font-size: 11pt; display: flex; align-items: center; justify-content: center;
  }}
  .studio-pill-mock {{
    position: absolute; bottom: 10px; right: 10px;
    background: rgba(30, 27, 75, 0.95); border: 1.5px solid #818cf8; color: #fff;
    padding: 4px 10px; border-radius: 16px; font-size: 8.5pt; font-weight: 700;
    display: flex; align-items: center; gap: 5px; box-shadow: 0 3px 10px rgba(0,0,0,0.5);
  }}
  .pill-net-tag {{ background: rgba(255,255,255,0.18); padding: 1px 5px; border-radius: 6px; font-size: 7pt; }}

  /* Audio Slate + Banner Visual */
  .audio-slate {{
    background: #0f172a; border: 2px solid #ef4444; border-radius: 8px;
    height: 92px; display: flex; flex-direction: column; align-items: center; justify-content: center;
    text-align: center; padding: 8px;
  }}

  /* Preferences Mockup */
  .settings-mock {{
    background: #1e1e24; color: #f4f4f5; border-radius: 8px; padding: 9px;
    border: 1px solid #3f3f46; font-size: 8.2pt;
  }}
  .settings-sec {{
    background: #27272d; border: 1px solid #3f3f46; border-radius: 6px; padding: 7px 9px;
  }}
  .chk-row {{ display: flex; align-items: center; gap: 6px; margin-bottom: 4px; }}
  .chk-box {{
    width: 13px; height: 13px; border-radius: 3px; background: #6366f1; color: #fff;
    display: inline-flex; align-items: center; justify-content: center; font-size: 8pt; font-weight: 800; flex-shrink: 0;
  }}

  /* Theme Gallery */
  .theme-gallery {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px; margin: 6px 0; }}
  .mini-app {{ border-radius: 7px; overflow: hidden; border: 1px solid #cbd5e1; font-size: 7.5pt; }}
  .mini-app-bar {{ padding: 3px 6px; font-weight: 700; display: flex; justify-content: space-between; align-items: center; }}
  .mini-app-body {{ display: grid; grid-template-columns: 35% 65%; height: 42px; }}
  .mini-side {{ padding: 4px; font-size: 6.5pt; }}
  .mini-main {{ padding: 4px; display: flex; flex-direction: column; justify-content: space-between; }}
  .mini-btn {{ display: inline-block; padding: 1.5px 5px; border-radius: 3px; font-size: 6.5pt; font-weight: 700; align-self: flex-end; }}

  /* Before / After Camera Mockup */
  .cam-compare {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 6px 0; }}
  .cam-frame {{ border-radius: 7px; padding: 7px; text-align: center; border: 1px solid #cbd5e1; display: flex; align-items: center; gap: 10px; }}
  .cam-raw {{ background: linear-gradient(180deg, #334155 0%, #1e293b 100%); color: #cbd5e1; }}
  .cam-studio {{ background: radial-gradient(circle at 30% 50%, #475569 0%, #1e1b4b 75%, #09090b 100%); color: #f8fafc; border-color: #6366f1; }}
  .cam-face {{ width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14pt; flex-shrink: 0; }}

  /* Footer Disclaimer */
  .disclaimer-box {{
    margin-top: 6px; padding: 6px 10px; border-radius: 7px;
    background: #f8fafc; border: 1px solid #e2e8f0;
    font-size: 7.5pt; color: #64748b; text-align: center; line-height: 1.3;
  }}
</style>
</head>
<body>

<!-- COVER HEADER -->
<div class="cover-header">
  <div class="cover-info">
    <div class="cover-title">Teamux v1.0.0</div>
    <div class="cover-subtitle">Official User Guide &amp; Visual Feature Manual</div>
    <div class="cover-meta">
      <span>Release: v1.0.0 (Production)</span>
      <span>Platforms: Linux (x64) &amp; Windows (x64)</span>
      <span>Publisher: Quiet Byte</span>
      <span>License: Apache-2.0</span>
    </div>
  </div>
  <img class="cover-logo" src="data:image/png;base64,{icon_b64}" alt="Teamux Logo">
</div>

<!-- SECTION 1: INTRODUCTION & VISUAL MAP -->
<h1><span>1.</span> Introduction, Core Highlights &amp; Interface Map</h1>
<p>
  <strong>Teamux</strong> is an unofficial, high-performance desktop client for Microsoft Teams engineered for demanding workflows, low-bandwidth branch offices, and modern Linux and Windows desktops. You sign in with your regular Microsoft Teams account—all chats, channels, and meetings remain identical.
</p>

<div class="grid-2 avoid-break">
  <div class="card">
    <div class="card-title">🛡️ Adaptive Network Guardian</div>
    <div class="card-body">Tracks latency, packet loss, and bandwidth every 2.5s. Auto-scales video (720p &rarr; 480p &rarr; 360p) or engages <strong>Audio-First Mode</strong> (0 kbps video) so voice audio never drops.</div>
  </div>
  <div class="card">
    <div class="card-title">🧊 Zero-Freeze &amp; Instant Exit</div>
    <div class="card-body">Single-instance camera lifecycle, display-synced frame callbacks, top-frame isolation, a double-close escape hatch (<code>X</code> twice in 2.5s), and a 1.5s forced exit watchdog.</div>
  </div>
  <div class="card">
    <div class="card-title">✨ In-Meeting Studio Beauty Cam</div>
    <div class="card-body">Built-in webcam enhancements inside Teams: skin smoothing, studio lighting booster, portrait vignette, tone grading (contrast, saturation, shadow lift, warm glow), and grayscale.</div>
  </div>
  <div class="card">
    <div class="card-title">🎭 Custom Themes Engine</div>
    <div class="card-body">Restyles Teams in real time with 7 themes: Teams Default, OLED Midnight, Catppuccin Mocha, Nord Frost, Tokyo Night, Dracula, and Rosé Pine.</div>
  </div>
</div>

<!-- Visual Map of Teams Window -->
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
      <div style="margin-top:4px; font-size:8pt; font-weight:600;">Aleena (Branch Office)</div>
      <div style="font-size:7pt; color:#94a3b8;">🎤 Speaking...</div>
    </div>
    <div class="participant-box" style="border-color:#6366f1;">
      <div class="avatar-circle" style="background:#0ea5e9;">You</div>
      <div style="margin-top:4px; font-size:8pt; font-weight:600;">Your Camera (Studio Active)</div>
      <div style="font-size:7pt; color:#a5b4fc;">✨ Beauty + Studio Light ON</div>
    </div>
  </div>
  <div class="studio-pill-mock">
    <span class="pin">2</span>
    <span>✨ Studio</span>
    <span class="pill-net-tag">720p</span>
  </div>
</div>

<div class="grid-2 avoid-break" style="margin-top:4px;">
  <div class="explain-item"><span class="pin-inline">1</span><strong>Top Call &amp; Network Banner:</strong> Appears during calls (Green = Normal, Amber = Eco, Red = Audio-First). Click anytime to jump back to your meeting.</div>
  <div class="explain-item"><span class="pin-inline">2</span><strong>Floating Studio Pill (Bottom-Right):</strong> Shows your live video tier (<code>720p</code>, <code>480p</code>, <code>360p</code>, <code>Voice Only</code>). Click to open the 4-tab Studio panel.</div>
</div>

<!-- SECTION 2: INSTALLATION -->
<h1><span>2.</span> Step-by-Step Installation &amp; Setup</h1>

<div class="grid-2 avoid-break">
  <div class="step-box" style="margin-bottom:0;">
    <div class="step-title"><span class="step-badge">🐧</span> Linux (AppImage / .deb / .tar.gz)</div>
    <p><strong>Universal AppImage (No root required):</strong></p>
    <pre>chmod +x teamux-v1.0.0-linux-x86_64.AppImage
./teamux-v1.0.0-linux-x86_64.AppImage</pre>
    <p><strong>Ubuntu / Debian (.deb):</strong></p>
    <pre>sudo apt install ./teamux-v1.0.0-linux-amd64.deb</pre>
  </div>
  <div class="step-box" style="margin-bottom:0;">
    <div class="step-title"><span class="step-badge">🪟</span> Windows (Portable .exe / .zip)</div>
    <p><strong>1. Portable Single-File (.exe):</strong> Download <code>teamux-v1.0.0-windows-portable-x64.exe</code> and double-click to launch immediately. <strong>No installer or admin rights required.</strong></p>
    <p style="margin-top:6px;"><strong>2. Standalone Zip (.zip):</strong> Download <code>teamux-v1.0.0-windows-x64.zip</code>, extract anywhere (e.g. <code>C:\\Apps\\Teamux</code>), and run <code>Teamux.exe</code>.</p>
  </div>
</div>

<!-- SECTION 3: SIGNING IN & NAVIGATION -->
<h1><span>3.</span> Signing In, System Tray &amp; Clean Exit</h1>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">1</span> Teams Environment &amp; MFA Login</div>
  <p>Supports both <strong>Work / School (New Teams v2 — teams.cloud.microsoft)</strong> and <strong>Personal (Teams Live — teams.live.com)</strong>, including Microsoft Authenticator, FIDO2 keys, and SSO. Switch editions anytime via <strong>Preferences (<code>Ctrl + ,</code>)</strong>.</p>
</div>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">2</span> System Tray Controls &amp; Double-Close Escape Hatch</div>
  <ul>
    <li><strong>System Tray Menu:</strong> Right-click the tray icon for <code>Show/Hide</code>, <code>Unread Messages</code>, <code>Reload Teams</code>, <code>Preferences</code>, and <code>Quit Teamux</code>.</li>
    <li><strong>⚡ Double-Close Escape Hatch:</strong> Click the window close button (<code>X</code>) <strong>twice within 2.5 seconds</strong> to bypass tray behavior and terminate all processes immediately (backed by a 1.5s fail-safe shutdown timer).</li>
  </ul>
</div>

<!-- SECTION 4: BANDWIDTH CONTROL (AUTO & MANUAL) -->
<h1><span>4.</span> Bandwidth Control: Auto &amp; Manual Modes (🌐 Network Tab)</h1>
<p>
  On slow branch-office internet links, high-definition video can choke your upload speed—causing robotic audio and dropped calls. Teamux gives you both <strong>Auto Mode</strong> (Adaptive Network Guardian) and <strong>Manual Mode</strong> (lock a fixed speed).
</p>

<div class="ui-split avoid-break">
  <!-- Studio Network Mockup -->
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
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:10px; font-weight:700;">
          <span><span class="pin-inline">3</span>Live WebRTC Telemetry</span>
          <span class="st-badge">Optimal</span>
        </div>
        <div class="net-grid">
          <div class="net-stat"><div class="net-lbl">Latency (RTT)</div><div class="net-val">42 ms</div></div>
          <div class="net-stat"><div class="net-lbl">Packet Loss</div><div class="net-val">0%</div></div>
          <div class="net-stat"><div class="net-lbl">Est. Bandwidth</div><div class="net-val">2400 kbps</div></div>
          <div class="net-stat"><div class="net-lbl">Active Video Stream</div><div class="net-val">🚀 720p</div></div>
        </div>
      </div>
      <div class="hint-box-dark">🛡️ When branch network is constrained, video throttles automatically to guarantee 100% voice clarity.</div>
    </div>
  </div>

  <div class="explain-stack">
    <div class="explain-item">
      <span class="pin-inline">1</span><strong>Adaptive Guardian Toggle (Auto Mode):</strong><br>
      When ON (default), Teamux measures your connection every <strong>2.5 seconds</strong> and adjusts video quality automatically without dropping the call.
    </div>
    <div class="explain-item">
      <span class="pin-inline">2</span><strong>Bandwidth Profile Dropdown (Auto vs. Manual):</strong><br>
      Keep on <strong>Auto (Dynamic Guardian)</strong> for automatic protection, or pick a fixed preset to lock your speed manually:
      <code>720p Full HD</code>, <code>480p Balanced</code>, <code>360p Eco Saver</code>, or <code>Audio-First Priority</code>.
    </div>
    <div class="explain-item">
      <span class="pin-inline">3</span><strong>Live WebRTC Telemetry Card:</strong><br>
      Shows real-time <strong>Latency (RTT ms)</strong>, <strong>Packet Loss (%)</strong> (turns red if &gt;5%), <strong>Est. Bandwidth (kbps)</strong>, and the <strong>Active Video Stream</strong> tier currently transmitting.
    </div>
  </div>
</div>

<h2>Auto Mode: The 4 Dynamic Quality Tiers &amp; Audio-First Recovery</h2>
<table class="avoid-break">
  <thead>
    <tr>
      <th>Quality Tier</th>
      <th>Resolution &amp; FPS</th>
      <th>Upload Bitrate</th>
      <th>Network Triggers</th>
      <th>Guardian Action</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span class="badge badge-720p">720p Full HD</span></td>
      <td>1280 &times; 720 @ 30 FPS</td>
      <td>~2,000 kbps</td>
      <td>Ping &lt; 130 ms, Loss &lt; 2%</td>
      <td>Optimal network: full high-definition video output.</td>
    </tr>
    <tr>
      <td><span class="badge badge-480p">480p Balanced</span></td>
      <td>854 &times; 480 @ 20 FPS</td>
      <td>~500 kbps</td>
      <td>Ping 130–260 ms, Loss 2–6%</td>
      <td>Cuts upload bandwidth by 75% while keeping video sharp.</td>
    </tr>
    <tr>
      <td><span class="badge badge-360p">360p Eco Saver</span></td>
      <td>640 &times; 360 @ 15 FPS</td>
      <td>~250 kbps</td>
      <td>Ping 260–500 ms, Loss 6–15%</td>
      <td>Deep 87% bandwidth savings for congested office links.</td>
    </tr>
    <tr>
      <td><span class="badge badge-audio">Audio-First Priority</span></td>
      <td>Static Slate @ 1 FPS</td>
      <td>~0 kbps (Paused)</td>
      <td>Ping &gt; 500 ms, Loss &gt; 15%</td>
      <td><strong>Voice Protection:</strong> Pauses video so voice is 100% clear. Auto-recovers after 3 healthy checks (~7.5s).</td>
    </tr>
  </tbody>
</table>

<div class="grid-2 avoid-break">
  <div>
    <div style="font-weight:700; font-size:8.5pt; color:#b91c1c; margin-bottom:4px;">What Attendees See in Audio-First Mode:</div>
    <div class="audio-slate">
      <div style="color:#ef4444; font-weight:800; font-size:10.5pt; margin-bottom:3px;">🔴 Audio-First Mode Active</div>
      <div style="color:#94a3b8; font-size:8pt;">Video upload paused to protect voice audio quality.</div>
      <div style="color:#94a3b8; font-size:8pt;">Resuming automatically when network clears.</div>
    </div>
  </div>
  <div class="settings-mock">
    <div style="font-weight:700; color:#c7d2fe; font-size:8.5pt; margin-bottom:5px;">Manual Mode in Preferences (<code>Ctrl + ,</code>) &rarr; Save &amp; Apply:</div>
    <div class="settings-sec">
      <div class="chk-row"><span class="chk-box">&#10003;</span><span>Adaptive Network Guardian (Auto-Throttle video)</span></div>
      <div style="color:#a1a1aa; font-size:7.8pt; margin:4px 0 2px 0;">Default Video Bandwidth Mode:</div>
      <div class="net-select" style="background:#18181b;"><span>Eco Bandwidth Saver (360p @ 15 FPS / ~250 kbps)</span><span>&#9662;</span></div>
    </div>
  </div>
</div>

<!-- SECTION 5: CAMERA STUDIO (RETOUCH & TONE) -->
<h1><span>5.</span> In-Meeting Studio Camera Controller (✨ Retouch &amp; 🎨 Tone)</h1>
<p>Click the floating <strong>✨ Studio</strong> pill during any call or camera preview to enhance your video locally (all processing stays on your PC—nothing is sent to external servers).</p>

<!-- Retouch Tab Visual -->
<div class="ui-split avoid-break">
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
      <div class="t-row"><div class="t-label"><span class="pin">1</span><span>Beauty Filter</span></div><div class="sw on"></div></div>
      <div class="rng-group">
        <div class="rng-lbl"><span>Smoothness</span><span>55%</span></div>
        <div class="rng-track"><div class="rng-fill" style="width:55%;"><div class="rng-thumb"></div></div></div>
      </div>
      <div class="t-row"><div class="t-label"><span class="pin">2</span><span>Studio Lighting</span></div><div class="sw on"></div></div>
      <div class="t-row"><div class="t-label"><span class="pin">3</span><span>Portrait Focus (Vignette)</span></div><div class="sw on"></div></div>
      <div class="hint-box-dark">💡 Custom BG &amp; Blur: Supported natively in Teams meeting under More &gt; Video effects.</div>
      <div class="btn-compare"><span class="pin">4</span><span>👁️ Hold to Compare</span></div>
    </div>
  </div>

  <div class="explain-stack">
    <div class="explain-item"><span class="pin-inline">1</span><strong>Beauty Filter &amp; Smoothness (10%–100%):</strong> Softly smooths skin tone and reduces webcam grain. Slide right for stronger smoothing.</div>
    <div class="explain-item"><span class="pin-inline">2</span><strong>Studio Lighting:</strong> Brightens dark shadows on your face automatically in dim offices.</div>
    <div class="explain-item"><span class="pin-inline">3</span><strong>Portrait Focus (Vignette):</strong> Softly darkens outer frame edges so focus stays centered on you.</div>
    <div class="explain-item"><span class="pin-inline">4</span><strong>👁️ Hold to Compare:</strong> Hold down to preview your raw unedited camera; release to snap back to your Studio look.</div>
    <div class="explain-item"><span class="pin-inline">5</span><strong>Minimize (&minus;):</strong> Collapses back to the small <code>✨ Studio</code> pill while keeping all effects active.</div>
  </div>
</div>

<div class="cam-compare avoid-break">
  <div class="cam-frame cam-raw">
    <div class="cam-face" style="background:#475569;">😐</div>
    <div style="text-align:left;"><div style="font-weight:700; font-size:8.5pt;">BEFORE: Raw Webcam</div><div style="font-size:7.8pt; color:#94a3b8;">Dark shadows, flat lighting, visible grain</div></div>
  </div>
  <div class="cam-frame cam-studio">
    <div class="cam-face" style="background:#6366f1;">😊</div>
    <div style="text-align:left;"><div style="font-weight:700; font-size:8.5pt; color:#a5b4fc;">AFTER: Studio Retouch + Lighting + Vignette</div><div style="font-size:7.8pt; color:#e0e7ff;">Brighter face, smooth skin, focused edges</div></div>
  </div>
</div>

<!-- Tone Tab Visual -->
<div class="ui-split avoid-break" style="margin-top:8px;">
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
      <div class="t-row"><div class="t-label"><span class="pin">1</span><span>Grayscale (Black &amp; White)</span></div><div class="sw"></div></div>
      <div class="rng-group"><div class="rng-lbl"><span><span class="pin-inline">2</span>Contrast</span><span>110%</span></div><div class="rng-track"><div class="rng-fill" style="width:60%;"><div class="rng-thumb"></div></div></div></div>
      <div class="rng-group"><div class="rng-lbl"><span><span class="pin-inline">3</span>Saturation</span><span>115%</span></div><div class="rng-track"><div class="rng-fill" style="width:58%;"><div class="rng-thumb"></div></div></div></div>
      <div class="rng-group"><div class="rng-lbl"><span><span class="pin-inline">4</span>Shadow Lift</span><span>+15</span></div><div class="rng-track"><div class="rng-fill" style="width:65%;"><div class="rng-thumb"></div></div></div></div>
      <div class="rng-group"><div class="rng-lbl"><span><span class="pin-inline">5</span>Ambience (Warm Glow)</span><span>25%</span></div><div class="rng-track"><div class="rng-fill" style="width:25%;"><div class="rng-thumb"></div></div></div></div>
      <div class="btn-reset"><span class="pin">6</span><span>↺ Reset Tone Adjustments</span></div>
    </div>
  </div>

  <div class="explain-stack">
    <div class="explain-item"><span class="pin-inline">1</span><strong>Grayscale (Black &amp; White):</strong> One-click crisp monochrome stream.</div>
    <div class="explain-item"><span class="pin-inline">2</span><strong>Contrast (50%–150%):</strong> Deepens blacks and removes hazy webcam look.</div>
    <div class="explain-item"><span class="pin-inline">3</span><strong>Saturation (0%–200%):</strong> Enriches washed-out webcam colors.</div>
    <div class="explain-item"><span class="pin-inline">4</span><strong>Shadow Lift (-50 to +50):</strong> Brightens your face when sitting in front of a bright window.</div>
    <div class="explain-item"><span class="pin-inline">5</span><strong>Ambience / Warm Glow (0%–100%):</strong> Adds a warm tint to balance cold office fluorescent lights.</div>
    <div class="explain-item"><span class="pin-inline">6</span><strong>↺ Reset Tone Adjustments:</strong> Resets all tone controls back to neutral defaults.</div>
  </div>
</div>

<!-- SECTION 6: CUSTOM THEMES ENGINE -->
<h1 style="page-break-after: avoid;"><span>6.</span> Custom App Themes Engine (🎭 Themes Tab)</h1>
<p style="page-break-after: avoid;">Click <strong>✨ Studio</strong> &rarr; <strong>🎭 Themes</strong> and click any theme card to restyle Microsoft Teams immediately—no restart required. Your selection is saved automatically.</p>

<div class="ui-split avoid-break">
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
    <div class="studio-body" style="gap:5px;">
      <div class="theme-card"><div><div class="theme-title">🖥️ Teams Default</div><div class="theme-desc">Microsoft Teams native appearance</div></div><div class="swatches"><span class="dot" style="background:#201f1f"></span><span class="dot" style="background:#2d2c2c"></span><span class="dot" style="background:#6264a7"></span></div></div>
      <div class="theme-card active"><div><div class="theme-title">🌌 OLED Midnight <span class="theme-badge">Active</span></div><div class="theme-desc">True pitch black with neon electric blue</div></div><div class="swatches"><span class="dot" style="background:#000000"></span><span class="dot" style="background:#121212"></span><span class="dot" style="background:#38bdf8"></span></div></div>
      <div class="theme-card"><div><div class="theme-title">☕ Catppuccin Mocha</div><div class="theme-desc">Soothing developer pastel &amp; mauve</div></div><div class="swatches"><span class="dot" style="background:#1e1e2e"></span><span class="dot" style="background:#313244"></span><span class="dot" style="background:#cba6f7"></span></div></div>
      <div class="theme-card"><div><div class="theme-title">❄️ Nord Frost</div><div class="theme-desc">Arctic slates &amp; crisp polar cyan</div></div><div class="swatches"><span class="dot" style="background:#2e3440"></span><span class="dot" style="background:#3b4252"></span><span class="dot" style="background:#88c0d0"></span></div></div>
      <div class="theme-card"><div><div class="theme-title">🌆 Tokyo Night</div><div class="theme-desc">Deep navy twilight &amp; neon cyan/magenta</div></div><div class="swatches"><span class="dot" style="background:#1a1b26"></span><span class="dot" style="background:#24283b"></span><span class="dot" style="background:#7dcfff"></span></div></div>
      <div class="theme-card"><div><div class="theme-title">🧛 Dracula</div><div class="theme-desc">Vampire dark slate &amp; vibrant neon pink</div></div><div class="swatches"><span class="dot" style="background:#282a36"></span><span class="dot" style="background:#44475a"></span><span class="dot" style="background:#ff79c6"></span></div></div>
      <div class="theme-card"><div><div class="theme-title">🌸 Rosé Pine</div><div class="theme-desc">Cozy warm dusk &amp; delicate rose gold</div></div><div class="swatches"><span class="dot" style="background:#191724"></span><span class="dot" style="background:#26233a"></span><span class="dot" style="background:#ebbcba"></span></div></div>
    </div>
  </div>

  <div>
    <div class="explain-item" style="margin-bottom:6px;">
      <strong>Visual Preview Gallery:</strong> See how the Teams sidebar, chat area, and buttons look in each custom theme:
    </div>
    <div class="theme-gallery">
      <div class="mini-app" style="border-color:#262626;"><div class="mini-app-bar" style="background:#080808; color:#fff;"><span>🌌 OLED</span><span style="color:#38bdf8;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#080808; color:#a3a3a3;"># General</div><div class="mini-main" style="background:#000; color:#fff;"><span>Chat</span><span class="mini-btn" style="background:#38bdf8; color:#000;">Join</span></div></div></div>
      <div class="mini-app" style="border-color:#313244;"><div class="mini-app-bar" style="background:#181825; color:#cdd6f4;"><span>☕ Mocha</span><span style="color:#cba6f7;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#181825; color:#a6adc8;"># General</div><div class="mini-main" style="background:#1e1e2e; color:#cdd6f4;"><span>Chat</span><span class="mini-btn" style="background:#cba6f7; color:#111;">Join</span></div></div></div>
      <div class="mini-app" style="border-color:#434c5e;"><div class="mini-app-bar" style="background:#242933; color:#eceff4;"><span>❄️ Nord</span><span style="color:#88c0d0;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#242933; color:#d8dee9;"># General</div><div class="mini-main" style="background:#2e3440; color:#eceff4;"><span>Chat</span><span class="mini-btn" style="background:#88c0d0; color:#111;">Join</span></div></div></div>
      <div class="mini-app" style="border-color:#292e42;"><div class="mini-app-bar" style="background:#16161e; color:#c0caf5;"><span>🌆 Tokyo</span><span style="color:#7dcfff;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#16161e; color:#787c99;"># General</div><div class="mini-main" style="background:#1a1b26; color:#c0caf5;"><span>Chat</span><span class="mini-btn" style="background:#7dcfff; color:#111;">Join</span></div></div></div>
      <div class="mini-app" style="border-color:#44475a;"><div class="mini-app-bar" style="background:#1e1f29; color:#f8f8f2;"><span>🧛 Dracula</span><span style="color:#ff79c6;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#1e1f29; color:#d6d6d4;"># General</div><div class="mini-main" style="background:#282a36; color:#f8f8f2;"><span>Chat</span><span class="mini-btn" style="background:#ff79c6; color:#111;">Join</span></div></div></div>
      <div class="mini-app" style="border-color:#403d52;"><div class="mini-app-bar" style="background:#14121e; color:#e0def4;"><span>🌸 Rosé</span><span style="color:#ebbcba;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#14121e; color:#908caa;"># General</div><div class="mini-main" style="background:#191724; color:#e0def4;"><span>Chat</span><span class="mini-btn" style="background:#ebbcba; color:#111;">Join</span></div></div></div>
    </div>
    <div class="callout callout-info" style="margin-top:6px;">
      <strong>Battery &amp; Comfort Tip:</strong> Use <strong>🌌 OLED Midnight</strong> on OLED laptops for maximum battery life, or <strong>☕ Catppuccin Mocha / 🌸 Rosé Pine</strong> to reduce eye fatigue.
    </div>
  </div>
</div>

<!-- SECTION 7: SCREEN SHARING & PREFERENCES -->
<h1><span>7.</span> Screen Sharing &amp; Preferences Reference (<code>Ctrl + ,</code>)</h1>
<p>
  <strong>Linux Wayland &amp; PipeWire:</strong> Click <strong>Share</strong> in a meeting to open the native portal picker showing live thumbnails of monitors and windows at 30 FPS. <strong>Windows 10 &amp; 11:</strong> Click <strong>Share</strong> and select any monitor or application window.
</p>

<table class="avoid-break">
  <thead>
    <tr>
      <th>Setting Name</th>
      <th>Description</th>
      <th>Default</th>
      <th>Recommended Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><strong>Adaptive Guardian</strong></td><td>Auto-throttle video bitrate when network slows</td><td><code>true</code></td><td>Keep enabled for all remote &amp; branch offices.</td></tr>
    <tr><td><strong>Bandwidth Profile</strong></td><td>Auto, 720p, 480p, 360p Eco, or Audio-Only</td><td><code>Auto</code></td><td>Lock <code>360p</code> for permanently slow links (&lt;1 Mbps).</td></tr>
    <tr><td><strong>Teams Environment</strong></td><td>Work/School v2 vs. Personal (Teams Live)</td><td><code>Work/School v2</code></td><td>Keep <code>Work/School v2</code> for company accounts.</td></tr>
    <tr><td><strong>Keep running in tray</strong></td><td>Keep running in background on window close</td><td><code>false</code></td><td>Leave disabled for immediate clean exit.</td></tr>
    <tr><td><strong>Minimize to tray</strong></td><td>Minimize window directly to system tray</td><td><code>true</code></td><td>Useful for background call &amp; chat notifications.</td></tr>
    <tr><td><strong>Hardware Acceleration</strong></td><td>GPU rasterization &amp; VA-API video decode</td><td><code>true</code></td><td>Keep enabled for low CPU usage.</td></tr>
  </tbody>
</table>

<!-- SECTION 8: TROUBLESHOOTING -->
<h1><span>8.</span> Troubleshooting &amp; FAQs</h1>
<div class="grid-2 avoid-break">
  <div class="step-box" style="margin-bottom:0;">
    <div class="step-title">Q: Camera shows black screen?</div>
    <p><strong>Windows:</strong> Settings &rarr; Privacy &amp; Security &rarr; Camera &rarr; Allow desktop apps.<br><strong>Linux:</strong> Run <code>sudo usermod -a -G video $USER</code> and ensure OBS/Zoom isn't locking <code>/dev/video0</code>.</p>
  </div>
  <div class="step-box" style="margin-bottom:0;">
    <div class="step-title">Q: Wayland screen share black screen?</div>
    <p>Verify PipeWire &amp; portal: <code>systemctl --user status pipewire</code> and install <code>xdg-desktop-portal-gnome</code> (or <code>-kde</code>).</p>
  </div>
  <div class="step-box" style="margin-bottom:0;">
    <div class="step-title">Q: App hangs on close?</div>
    <p>Click <strong>X twice within 2.5 seconds</strong> (Double-Close Escape Hatch) or right-click Tray &rarr; <strong>Quit Teamux</strong>.</p>
  </div>
  <div class="step-box" style="margin-bottom:0;">
    <div class="step-title">Q: Downloads &amp; Support?</div>
    <p>Releases: <code>github.com/quietbytehq/teamux/releases</code><br>Email: <code>hello@quietbytehq.uk</code></p>
  </div>
</div>

<div class="disclaimer-box avoid-break">
  <strong>Legal Disclaimer:</strong> Teamux is an independent open-source project and is not affiliated with, endorsed, or sponsored by Microsoft Corporation. Microsoft, Microsoft Teams, and Windows are trademarks of Microsoft Corporation. Licensed under Apache-2.0. Published by <strong>Quiet Byte</strong>.
</div>

</body>
</html>
"""

with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML guide generated at: {HTML_OUTPUT}")

cmd = [
    "/snap/bin/chromium",
    "--headless",
    "--no-sandbox",
    "--disable-gpu",
    f"--print-to-pdf={PDF_OUTPUT}",
    "--no-pdf-header-footer",
    HTML_OUTPUT
]

print("Rendering PDF via Chromium...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print(f"Chromium PDF render error: {res.stderr}")
    sys.exit(1)

print(f"PDF successfully rendered to: {PDF_OUTPUT}")
subprocess.run(["cp", PDF_OUTPUT, USER_PDF_COPY], check=True)
print(f"Copied PDF to: {USER_PDF_COPY}")
if os.path.exists("/home/faisal/Games"):
    subprocess.run(["cp", PDF_OUTPUT, GAMES_PDF_COPY], check=True)
    print(f"Copied PDF to: {GAMES_PDF_COPY}")
