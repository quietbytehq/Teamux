#!/usr/bin/env python3
"""
Teamux v2.0.0 Official User Guide & Picture-Based Feature Manual PDF Generator
Authored by Quiet Byte (2026)
"""

import os
import sys
import base64
import subprocess

DOCS_DIR = "/home/faisal/projects/quietbyte/Teamux/docs"
ICON_PATH = "/home/faisal/projects/quietbyte/Teamux/assets/icon.png"
HTML_OUTPUT = os.path.join(DOCS_DIR, "Teamux_User_Guide_v2.0.0.html")
PDF_OUTPUT = os.path.join(DOCS_DIR, "Teamux_User_Guide_v2.0.0.pdf")
USER_PDF_COPY = "/home/faisal/Teamux_User_Guide_v2.0.0.pdf"
GAMES_PDF_COPY = "/home/faisal/Games/Teamux_User_Guide_v2.0.0.pdf"

with open(ICON_PATH, "rb") as f:
    icon_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Teamux v2.0.0 — Official User Guide &amp; Feature Manual</title>
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
      content: "Teamux v2.0.0 — Official User Guide (Quiet Byte)";
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
    line-height: 1.32;
    font-size: 8.7pt;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  .avoid-break {{ page-break-inside: avoid; }}

  .cover-header {{
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #312e81 100%);
    color: #ffffff;
    border-radius: 12px;
    padding: 15px 20px;
    margin-bottom: 10px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .cover-info {{ max-width: 75%; }}
  .cover-title {{ font-size: 21pt; font-weight: 800; letter-spacing: -0.5px; margin: 0 0 2px 0; color: #ffffff; }}
  .cover-subtitle {{ font-size: 10.5pt; font-weight: 400; color: #c7d2fe; margin: 0 0 8px 0; }}
  .cover-meta {{ font-size: 7.8pt; display: flex; gap: 6px; flex-wrap: wrap; }}
  .cover-meta span {{ background: rgba(255,255,255,0.14); padding: 2.5px 7px; border-radius: 5px; color: #f8fafc; font-weight: 500; }}
  .cover-logo {{ width: 76px; height: 76px; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.4); background: #fff; padding: 3px; }}

  h1, h2, h3, h4 {{ color: #0f172a; font-weight: 700; margin-top: 7px; margin-bottom: 3px; page-break-after: avoid; }}
  h1 {{ font-size: 13pt; border-bottom: 2px solid #e2e8f0; padding-bottom: 3px; color: #1e1b4b; display: flex; align-items: center; gap: 6px; }}
  h2 {{ font-size: 10.4pt; color: #312e81; margin-top: 7px; }}
  p {{ margin: 0 0 4px 0; }}
  ul, ol {{ margin: 2px 0 4px 0; padding-left: 16px; }}
  li {{ margin-bottom: 1px; }}

  .callout {{ padding: 6px 10px; border-radius: 7px; margin: 6px 0; font-size: 8.6pt; line-height: 1.35; }}
  .callout-info {{ background: #eff6ff; border-left: 4px solid #3b82f6; color: #1e40af; }}

  .step-box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 7px; padding: 7px 10px; margin-bottom: 6px; }}
  .step-title {{ display: flex; align-items: center; gap: 6px; font-size: 9.5pt; font-weight: 700; color: #1e293b; margin-bottom: 3px; }}
  .step-badge {{ background: #4f46e5; color: #fff; font-size: 7.5pt; font-weight: 800; width: 18px; height: 18px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; }}

  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7px; margin: 6px 0; }}
  .card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 7px; padding: 7px 10px; }}
  .card-title {{ font-size: 9.5pt; font-weight: 700; color: #1e1b4b; margin-bottom: 2px; display: flex; align-items: center; gap: 5px; }}
  .card-body {{ font-size: 8.4pt; color: #475569; line-height: 1.35; }}

  table {{ width: 100%; border-collapse: collapse; margin: 6px 0; font-size: 8.3pt; }}
  th, td {{ padding: 3.5px 6px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
  th {{ background: #f1f5f9; color: #1e293b; font-weight: 700; font-size: 7.8pt; text-transform: uppercase; letter-spacing: 0.3px; }}
  tr:nth-child(even) td {{ background: #f8fafc; }}

  code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 8pt; background: #f1f5f9; padding: 1px 4px; border-radius: 3px; color: #334155; }}
  pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 7.8pt; background: #0f172a; color: #e2e8f0; padding: 5px 8px; border-radius: 5px; margin: 4px 0; line-height: 1.3; white-space: pre-wrap; }}

  .badge {{ display: inline-block; padding: 1.5px 6px; border-radius: 9px; font-size: 7.5pt; font-weight: 700; color: white; white-space: nowrap; }}
  .badge-720p {{ background: #2563eb; }}
  .badge-480p {{ background: #059669; }}
  .badge-360p {{ background: #d97706; }}
  .badge-audio {{ background: #dc2626; }}

  .pin {{ display: inline-flex; align-items: center; justify-content: center; width: 16px; height: 16px; border-radius: 50%; background: #e11d48; color: #fff; font-size: 7.4pt; font-weight: 800; flex-shrink: 0; border: 1.5px solid #fff; }}
  .pin-inline {{ display: inline-flex; align-items: center; justify-content: center; width: 15px; height: 15px; border-radius: 50%; background: #e11d48; color: #fff; font-size: 7.2pt; font-weight: 800; margin-right: 4px; vertical-align: middle; }}

  .ui-split {{ display: grid; grid-template-columns: 300px 1fr; gap: 11px; align-items: start; margin: 6px 0 8px 0; }}
  .explain-stack {{ display: flex; flex-direction: column; gap: 4.5px; }}
  .explain-item {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 5px 8px; font-size: 8.3pt; line-height: 1.33; }}

  .studio-card {{ background: #141418; border: 1.5px solid rgba(99,102,241,0.55); border-radius: 9px; width: 300px; box-shadow: 0 5px 15px rgba(15,23,42,0.22); color: #f4f4f5; overflow: hidden; font-size: 10.5px; }}
  .studio-header {{ padding: 6px 10px; background: #24242a; border-bottom: 1px solid #3f3f46; display: flex; align-items: center; justify-content: space-between; }}
  .studio-title {{ font-size: 11px; font-weight: 700; color: #c7d2fe; }}
  .studio-min {{ color: #a1a1aa; font-size: 13px; font-weight: 700; display: flex; align-items: center; gap: 4px; }}
  .studio-tabs {{ display: flex; background: #1e1e24; border-bottom: 1px solid #3f3f46; }}
  .studio-tab {{ flex: 1; padding: 5px 3px; font-size: 9.5px; font-weight: 600; text-align: center; color: #a1a1aa; border-bottom: 2px solid transparent; }}
  .studio-tab.active {{ color: #818cf8; border-bottom-color: #6366f1; background: rgba(99,102,241,0.12); }}
  .studio-body {{ padding: 6px 9px; display: flex; flex-direction: column; gap: 4.5px; }}
  .t-row {{ display: flex; align-items: center; justify-content: space-between; font-size: 10.5px; }}
  .t-label {{ display: flex; align-items: center; gap: 5px; }}
  .sw {{ width: 32px; height: 17px; border-radius: 17px; background: #3f3f46; position: relative; flex-shrink: 0; }}
  .sw.on {{ background: #6366f1; }}
  .sw::after {{ content: ""; position: absolute; width: 11px; height: 11px; border-radius: 50%; background: #fff; top: 3px; left: 3px; }}
  .sw.on::after {{ left: 18px; }}
  .rng-group {{ display: flex; flex-direction: column; gap: 2px; }}
  .rng-lbl {{ display: flex; justify-content: space-between; font-size: 10px; color: #a1a1aa; }}
  .rng-track {{ height: 4px; border-radius: 4px; background: #3f3f46; position: relative; }}
  .rng-fill {{ height: 100%; border-radius: 4px; background: #6366f1; position: relative; }}
  .rng-thumb {{ width: 10px; height: 10px; border-radius: 50%; background: #818cf8; border: 1.5px solid #fff; position: absolute; right: -5px; top: -3px; }}
  .btn-compare {{ background: #27272a; border: 1px solid #3f3f46; color: #e4e4e7; padding: 5px 7px; border-radius: 5px; font-size: 10px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 5px; }}
  .btn-reset {{ background: #1f1f23; border: 1px solid #3f3f46; color: #a1a1aa; padding: 4px 7px; border-radius: 5px; font-size: 9.5px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 4px; }}
  .div-mic {{ border-top: 1px solid #3f3f46; padding-top: 4px; font-size: 9.5px; font-weight: 700; color: #818cf8; }}
  .net-select {{ width: 100%; background: #24242a; border: 1px solid #3f3f46; color: #f4f4f5; padding: 4px 7px; border-radius: 5px; font-size: 10px; display: flex; justify-content: space-between; align-items: center; }}
  .net-dash {{ background: #18181b; border: 1px solid #3f3f46; border-radius: 6px; padding: 6px; display: flex; flex-direction: column; gap: 4px; }}
  .net-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4px; }}
  .net-stat {{ background: #27272a; padding: 4px 6px; border-radius: 4px; }}
  .net-lbl {{ font-size: 8px; color: #a1a1aa; }}
  .net-val {{ font-size: 10.5px; font-weight: 700; color: #f4f4f5; }}
  .st-badge {{ font-size: 8px; font-weight: 700; padding: 1.5px 5px; border-radius: 6px; color: #fff; background: #16a34a; }}

  .theme-card {{ display: flex; align-items: center; justify-content: space-between; padding: 3px 6px; background: rgba(36,36,42,0.85); border: 1px solid rgba(63,63,70,0.6); border-radius: 5px; }}
  .theme-card.active {{ background: rgba(99,102,241,0.2); border-color: #818cf8; }}
  .theme-title {{ font-size: 10px; font-weight: 700; color: #f4f4f5; }}
  .theme-desc {{ font-size: 8px; color: #a1a1aa; }}
  .theme-badge {{ font-size: 7.5px; font-weight: 700; padding: 1px 4px; border-radius: 6px; background: #4f46e5; color: #fff; margin-left: 3px; }}
  .swatches {{ display: flex; gap: 3px; }}
  .dot {{ width: 9px; height: 9px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.3); }}

  .teams-mock {{ background: #1f1f23; border-radius: 8px; border: 1px solid #334155; padding: 7px; position: relative; height: 150px; color: #e2e8f0; margin: 6px 0; }}
  .teams-topbar {{ display: flex; justify-content: space-between; align-items: center; background: #141418; padding: 3px 8px; border-radius: 5px; font-size: 7.8pt; margin-bottom: 5px; }}
  .call-banner-mock {{ background: rgba(15,23,42,0.95); border: 1.5px solid #22c55e; border-radius: 14px; padding: 2px 8px; display: inline-flex; align-items: center; gap: 5px; font-size: 7.5pt; font-weight: 600; color: #fff; }}
  .call-pill-btn {{ background: #22c55e; color: #0f172a; font-weight: 800; padding: 1px 5px; border-radius: 7px; font-size: 6.8pt; }}
  .video-grid-mock {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6px; height: 96px; }}
  .participant-box {{ background: linear-gradient(145deg, #27272a, #18181b); border-radius: 6px; border: 1px solid #3f3f46; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
  .avatar-circle {{ width: 30px; height: 30px; border-radius: 50%; background: #4f46e5; color: #fff; font-weight: 800; font-size: 10pt; display: flex; align-items: center; justify-content: center; }}
  .studio-pill-mock {{ position: absolute; bottom: 8px; right: 8px; background: rgba(30,27,75,0.95); border: 1.5px solid #818cf8; color: #fff; padding: 3px 9px; border-radius: 14px; font-size: 8pt; font-weight: 700; display: flex; align-items: center; gap: 4px; }}
  .pill-net-tag {{ background: rgba(255,255,255,0.18); padding: 1px 4px; border-radius: 5px; font-size: 6.8pt; }}

  .audio-slate {{ background: #0f172a; border: 2px solid #ef4444; border-radius: 7px; height: 82px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 6px; }}
  .settings-mock {{ background: #1e1e24; color: #f4f4f5; border-radius: 7px; padding: 8px; border: 1px solid #3f3f46; font-size: 7.8pt; }}
  .settings-sec {{ background: #27272d; border: 1px solid #3f3f46; border-radius: 5px; padding: 6px 8px; }}
  .chk-row {{ display: flex; align-items: center; gap: 5px; margin-bottom: 3px; }}
  .chk-box {{ width: 12px; height: 12px; border-radius: 3px; background: #6366f1; color: #fff; display: inline-flex; align-items: center; justify-content: center; font-size: 7.5pt; font-weight: 800; flex-shrink: 0; }}

  .theme-gallery {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 5px 0; }}
  .mini-app {{ border-radius: 6px; overflow: hidden; border: 1px solid #cbd5e1; font-size: 7.2pt; }}
  .mini-app-bar {{ padding: 2.5px 5px; font-weight: 700; display: flex; justify-content: space-between; align-items: center; }}
  .mini-app-body {{ display: grid; grid-template-columns: 35% 65%; height: 36px; }}
  .mini-side {{ padding: 3px; font-size: 6.2pt; }}
  .mini-main {{ padding: 3px; display: flex; flex-direction: column; justify-content: space-between; }}
  .mini-btn {{ display: inline-block; padding: 1px 4px; border-radius: 3px; font-size: 6pt; font-weight: 700; align-self: flex-end; }}

  .disclaimer-box {{ margin-top: 6px; padding: 5px 9px; border-radius: 6px; background: #f8fafc; border: 1px solid #e2e8f0; font-size: 7.3pt; color: #64748b; text-align: center; line-height: 1.25; }}
</style>
</head>
<body>

<div class="cover-header">
  <div class="cover-info">
    <div class="cover-title">Teamux v2.0.0</div>
    <div class="cover-subtitle">Official User Guide &amp; Visual Feature Manual (Low-Hardware, Security &amp; Branch Edition)</div>
    <div class="cover-meta">
      <span>Release: v2.0.0</span>
      <span>Linux (Snap / AppImage / .deb / .pacman) &amp; Windows (x64)</span>
      <span>Publisher: Quiet Byte</span>
      <span>License: Apache-2.0</span>
    </div>
  </div>
  <img class="cover-logo" src="data:image/png;base64,{icon_b64}" alt="Teamux Logo">
</div>

<h1><span>1.</span> What's New in v2.0.0 &amp; Visual Interface Map</h1>
<p>
  <strong>Teamux v2.0.0</strong> connects to your regular Microsoft Teams account with zero feature loss while adding low-hardware performance optimizations, hardened sandboxing, branch-office audio/bandwidth controls, and multi-account profile switching.
</p>

<div class="grid-2 avoid-break">
  <div class="card">
    <div class="card-title">⚡ Low-Hardware &amp; Potato PC Mode</div>
    <div class="card-body">0% CPU camera pass-through when Studio effects are off, hardware-level resolution downscaling, paused render loops in Audio-First/Away modes, and dynamic background throttling when idle.</div>
  </div>
  <div class="card">
    <div class="card-title">🔒 Hardened Security &amp; Privacy Lock</div>
    <div class="card-body">Sandboxed <code>contextIsolation</code> preload, origin-whitelisted permissions, safe external URL checks, and instant <strong>Ctrl+L Privacy Lock</strong> (with optional 4-digit PIN) for shared branch desks.</div>
  </div>
  <div class="card">
    <div class="card-title">🛡️ Adaptive Network &amp; Metered Mode</div>
    <div class="card-body">Auto-scales video (720p &rarr; 480p &rarr; 360p &rarr; Audio-First), includes a <strong>Metered Hotspot Mode</strong> (caps 360p), and tracks live <strong>Data Saved (MB)</strong>.</div>
  </div>
  <div class="card">
    <div class="card-title">🎙️ Studio Cam, Mic &amp; Multi-Account</div>
    <div class="card-body">Beauty, Tone, Mirror Camera, Stepped Away Slate (<code>Ctrl+Shift+V</code>), Noise Gate + Push-to-Talk, 7 App Themes, Loud Ring Alert, and 3 isolated Account Profiles.</div>
  </div>
</div>

<div class="teams-mock avoid-break">
  <div class="teams-topbar">
    <span><strong>Microsoft Teams (Teamux v2.0)</strong> — Weekly Branch Sync</span>
    <div class="call-banner-mock"><span class="pin">1</span><span>🟢 Active Call in Progress</span><span class="call-pill-btn">RETURN TO MEETING</span></div>
    <span>🔴 Leave</span>
  </div>
  <div class="video-grid-mock">
    <div class="participant-box"><div class="avatar-circle">A</div><div style="margin-top:3px; font-size:7.8pt; font-weight:600;">Aleena (Branch Office)</div><div style="font-size:6.8pt; color:#94a3b8;">🎤 Speaking...</div></div>
    <div class="participant-box" style="border-color:#6366f1;"><div class="avatar-circle" style="background:#0ea5e9;">You</div><div style="margin-top:3px; font-size:7.8pt; font-weight:600;">Your Camera (Studio Active)</div><div style="font-size:6.8pt; color:#a5b4fc;">✨ Beauty + Noise Filter ON</div></div>
  </div>
  <div class="studio-pill-mock"><span class="pin">2</span><span>✨ Studio</span><span class="pill-net-tag">720p</span></div>
</div>

<div class="grid-2 avoid-break" style="margin-top:3px;">
  <div class="explain-item"><span class="pin-inline">1</span><strong>Top Call &amp; Network Banner:</strong> Green = Optimal, Amber = Eco, Red = Audio-First. Click anytime to return to your call.</div>
  <div class="explain-item"><span class="pin-inline">2</span><strong>Floating Studio Pill:</strong> Displays your active stream tier. Click to open Retouch, Tone, Themes, and Network tabs.</div>
</div>

<h1><span>2.</span> Installation Across Linux &amp; Windows</h1>
<div class="grid-2 avoid-break">
  <div class="step-box" style="margin-bottom:0;">
    <div class="step-title"><span class="step-badge">🐧</span> Linux (Snap / AppImage / .deb / .pacman / .tar.gz)</div>
    <pre>sudo snap install teamux
# Or AppImage: chmod +x teamux-v2.0.0-linux-x86_64.AppImage
# Or Debian/Ubuntu: sudo apt install ./teamux-v2.0.0-linux-amd64.deb
# Or Arch Linux: sudo pacman -U teamux-v2.0.0-linux-x64.pacman</pre>
  </div>
  <div class="step-box" style="margin-bottom:0;">
    <div class="step-title"><span class="step-badge">🪟</span> Windows (Portable .exe &amp; Standalone .zip)</div>
    <p><strong>1. Portable (.exe):</strong> Double-click <code>teamux-v2.0.0-windows-portable-x64.exe</code> (zero install or admin rights needed).</p>
    <p><strong>2. Zip (.zip):</strong> Extract <code>teamux-v2.0.0-windows-x64.zip</code> and launch <code>Teamux.exe</code>.</p>
  </div>
</div>

<h1><span>3.</span> Bandwidth Control: Auto, Manual &amp; Metered Hotspot (🌐 Network Tab)</h1>
<div class="ui-split avoid-break">
  <div class="studio-card">
    <div class="studio-header"><div class="studio-title">✨ Teamux Studio</div><div class="studio-min">&minus;</div></div>
    <div class="studio-tabs"><div class="studio-tab">✨ Retouch</div><div class="studio-tab">🎨 Tone</div><div class="studio-tab">🎭 Themes</div><div class="studio-tab active">🌐 Network</div></div>
    <div class="studio-body">
      <div class="t-row"><div class="t-label"><span class="pin">1</span><span>Adaptive Guardian</span></div><div class="sw on"></div></div>
      <div class="t-row"><div class="t-label"><span class="pin">2</span><span>Metered Hotspot Mode (Cap 360p)</span></div><div class="sw"></div></div>
      <div class="rng-group"><div class="rng-lbl"><span><span class="pin-inline">3</span>Bandwidth Profile</span></div><div class="net-select"><span>Auto (Dynamic Guardian)</span><span>&#9662;</span></div></div>
      <div class="net-dash">
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:9.5px; font-weight:700;"><span><span class="pin-inline">4</span>Live WebRTC Telemetry</span><span class="st-badge">Optimal</span></div>
        <div class="net-grid">
          <div class="net-stat"><div class="net-lbl">Latency (RTT)</div><div class="net-val">42 ms</div></div>
          <div class="net-stat"><div class="net-lbl">Packet Loss</div><div class="net-val">0%</div></div>
          <div class="net-stat"><div class="net-lbl">Active Stream</div><div class="net-val">🚀 720p</div></div>
          <div class="net-stat"><div class="net-lbl">Data Saved</div><div class="net-val">18.4 MB</div></div>
        </div>
      </div>
    </div>
  </div>

  <div class="explain-stack">
    <div class="explain-item"><span class="pin-inline">1</span><strong>Adaptive Guardian (Auto Mode):</strong> Checks call latency &amp; packet loss every 2.5s and scales quality automatically so voice audio never breaks up.</div>
    <div class="explain-item"><span class="pin-inline">2</span><strong>Metered Hotspot Mode:</strong> Locks video at <code>360p Eco</code> for 4G/LTE branch hotspots while still dropping to Audio-First if ping spikes.</div>
    <div class="explain-item"><span class="pin-inline">3</span><strong>Bandwidth Profile (Auto vs. Manual):</strong> Select <code>Auto</code> or manually lock <code>720p</code>, <code>480p</code>, <code>360p</code>, or <code>Audio-First Priority</code> anytime (also configurable in <code>Ctrl+,</code> Preferences).</div>
    <div class="explain-item"><span class="pin-inline">4</span><strong>Live Telemetry &amp; Data Saved:</strong> Shows live Ping (ms), Loss (%), Active Tier, and total upload megabytes saved during the session.</div>
  </div>
</div>

<table class="avoid-break">
  <thead><tr><th>Quality Tier</th><th>Resolution &amp; FPS</th><th>Bitrate</th><th>Auto Trigger</th><th>Guardian Action</th></tr></thead>
  <tbody>
    <tr><td><span class="badge badge-720p">720p Full HD</span></td><td>1280 &times; 720 @ 30 FPS</td><td>~2,000 kbps</td><td>Ping &lt; 130ms, Loss &lt; 2%</td><td>Full HD video under healthy office internet.</td></tr>
    <tr><td><span class="badge badge-480p">480p Balanced</span></td><td>854 &times; 480 @ 20 FPS</td><td>~500 kbps</td><td>Ping 130–260ms, Loss 2–6%</td><td>75% bandwidth savings while keeping video sharp.</td></tr>
    <tr><td><span class="badge badge-360p">360p Eco Saver</span></td><td>640 &times; 360 @ 15 FPS</td><td>~250 kbps</td><td>Ping 260–500ms, Loss 6–15%</td><td>87% bandwidth savings for congested links.</td></tr>
    <tr><td><span class="badge badge-audio">Audio-First</span></td><td>Static Slate (Paused)</td><td>~0 kbps</td><td>Ping &gt; 500ms, Loss &gt; 15%</td><td><strong>0% CPU Slate:</strong> Pauses video so voice is 100% clear; auto-recovers after 7.5s healthy.</td></tr>
  </tbody>
</table>

<div class="grid-2 avoid-break">
  <div>
    <div style="font-weight:700; font-size:8.2pt; color:#b91c1c; margin-bottom:3px;">What Attendees See in Audio-First Mode:</div>
    <div class="audio-slate"><div style="color:#ef4444; font-weight:800; font-size:10pt;">🔴 Audio-First Mode Active</div><div style="color:#94a3b8; font-size:7.6pt;">Video upload paused to protect voice audio quality. Resuming automatically when network clears.</div></div>
  </div>
  <div class="settings-mock">
    <div style="font-weight:700; color:#c7d2fe; font-size:8.2pt; margin-bottom:4px;">Preferences (<code>Ctrl + ,</code>) — Low-Spec &amp; Manual Mode:</div>
    <div class="settings-sec">
      <div class="chk-row"><span class="chk-box">&#10003;</span><span>Low-Hardware / Potato PC Mode (0% CPU pass-through)</span></div>
      <div class="chk-row"><span class="chk-box">&#10003;</span><span>Adaptive Network Guardian</span></div>
      <div class="net-select" style="background:#18181b; margin-top:3px;"><span>Default: Eco Bandwidth Saver (360p / ~250 kbps)</span><span>&#9662;</span></div>
    </div>
  </div>
</div>

<h1><span>4.</span> Studio Camera, Mirror, Away Slate &amp; Mic Controls (✨ Retouch &amp; 🎨 Tone)</h1>
<div class="ui-split avoid-break">
  <div class="studio-card">
    <div class="studio-header"><div class="studio-title">✨ Teamux Studio</div><div class="studio-min">&minus;</div></div>
    <div class="studio-tabs"><div class="studio-tab active">✨ Retouch</div><div class="studio-tab">🎨 Tone</div><div class="studio-tab">🎭 Themes</div><div class="studio-tab">🌐 Network</div></div>
    <div class="studio-body">
      <div class="t-row"><div class="t-label"><span class="pin">1</span><span>Beauty Filter (55%)</span></div><div class="sw on"></div></div>
      <div class="rng-group"><div class="rng-track"><div class="rng-fill" style="width:55%;"><div class="rng-thumb"></div></div></div></div>
      <div class="t-row"><div class="t-label"><span class="pin">2</span><span>Studio Lighting &amp; Vignette</span></div><div class="sw on"></div></div>
      <div class="t-row"><div class="t-label"><span class="pin">3</span><span>Mirror Camera (Flip)</span></div><div class="sw"></div></div>
      <div class="t-row"><div class="t-label"><span class="pin">4</span><span>Stepped Away Slate (Ctrl+Shift+V)</span></div><div class="sw"></div></div>
      <div class="div-mic">🎙️ Branch Office Mic Controls</div>
      <div class="t-row"><div class="t-label"><span class="pin">5</span><span>Noise Filter (High-Pass 90Hz)</span></div><div class="sw on"></div></div>
      <div class="t-row"><div class="t-label"><span class="pin">6</span><span>Push-to-Talk (Hold Ctrl+Space)</span></div><div class="sw"></div></div>
      <div class="btn-compare"><span>👁️ Hold to Compare</span></div>
    </div>
  </div>

  <div class="explain-stack">
    <div class="explain-item"><span class="pin-inline">1</span><strong>Beauty Filter &amp; Smoothness:</strong> Softens webcam grain (skipped automatically in Low-Hardware Mode for extra speed).</div>
    <div class="explain-item"><span class="pin-inline">2</span><strong>Studio Lighting &amp; Portrait Vignette:</strong> Brightens dim rooms and focuses attention on your face.</div>
    <div class="explain-item"><span class="pin-inline">3</span><strong>Mirror Camera (Flip):</strong> Flips your camera horizontally—useful when showing whiteboards or notes.</div>
    <div class="explain-item"><span class="pin-inline">4</span><strong>Stepped Away Slate (<code>Ctrl+Shift+V</code>):</strong> Displays a clean <em>"⏸️ Stepped Away"</em> card and pauses rendering (0% CPU) without disconnecting.</div>
    <div class="explain-item"><span class="pin-inline">5</span><strong>Noise Filter (90Hz High-Pass):</strong> Cuts low-frequency office AC, fan, and desk rumble from your mic.</div>
    <div class="explain-item"><span class="pin-inline">6</span><strong>Push-to-Talk (<code>Ctrl+Space</code>):</strong> Keeps mic muted in noisy rooms until you hold <code>Ctrl+Space</code>.</div>
  </div>
</div>

<div class="ui-split avoid-break">
  <div class="studio-card">
    <div class="studio-header"><div class="studio-title">✨ Teamux Studio</div><div class="studio-min">&minus;</div></div>
    <div class="studio-tabs"><div class="studio-tab">✨ Retouch</div><div class="studio-tab active">🎨 Tone</div><div class="studio-tab">🎭 Themes</div><div class="studio-tab">🌐 Network</div></div>
    <div class="studio-body">
      <div class="t-row"><div class="t-label"><span class="pin">1</span><span>Grayscale (Black &amp; White)</span></div><div class="sw"></div></div>
      <div class="rng-group"><div class="rng-lbl"><span><span class="pin-inline">2</span>Contrast</span><span>110%</span></div><div class="rng-track"><div class="rng-fill" style="width:60%;"><div class="rng-thumb"></div></div></div></div>
      <div class="rng-group"><div class="rng-lbl"><span><span class="pin-inline">3</span>Saturation</span><span>115%</span></div><div class="rng-track"><div class="rng-fill" style="width:58%;"><div class="rng-thumb"></div></div></div></div>
      <div class="rng-group"><div class="rng-lbl"><span><span class="pin-inline">4</span>Shadow Lift</span><span>+15</span></div><div class="rng-track"><div class="rng-fill" style="width:65%;"><div class="rng-thumb"></div></div></div></div>
      <div class="rng-group"><div class="rng-lbl"><span><span class="pin-inline">5</span>Ambience (Warm Glow)</span><span>25%</span></div><div class="rng-track"><div class="rng-fill" style="width:25%;"><div class="rng-thumb"></div></div></div></div>
      <div class="btn-reset">↺ Reset Tone Adjustments</div>
    </div>
  </div>
  <div class="explain-stack">
    <div class="explain-item"><span class="pin-inline">1</span><strong>Grayscale:</strong> One-click black &amp; white camera mode.</div>
    <div class="explain-item"><span class="pin-inline">2</span><strong>Contrast (50%–150%):</strong> Removes hazy/flat webcam appearance.</div>
    <div class="explain-item"><span class="pin-inline">3</span><strong>Saturation (0%–200%):</strong> Boosts washed-out colors naturally.</div>
    <div class="explain-item"><span class="pin-inline">4</span><strong>Shadow Lift (-50 to +50):</strong> Brightens your face against bright window backlighting.</div>
    <div class="explain-item"><span class="pin-inline">5</span><strong>Ambience (0%–100%):</strong> Warms up cold fluorescent office lighting.</div>
  </div>
</div>

<h1><span>5.</span> Custom App Themes Engine (🎭 Themes Tab)</h1>
<div class="ui-split avoid-break">
  <div class="studio-card">
    <div class="studio-header"><div class="studio-title">✨ Teamux Studio</div><div class="studio-min">&minus;</div></div>
    <div class="studio-tabs"><div class="studio-tab">✨ Retouch</div><div class="studio-tab">🎨 Tone</div><div class="studio-tab active">🎭 Themes</div><div class="studio-tab">🌐 Network</div></div>
    <div class="studio-body" style="gap:3.5px;">
      <div class="theme-card"><div><div class="theme-title">🖥️ Teams Default</div><div class="theme-desc">Microsoft Teams native appearance</div></div><div class="swatches"><span class="dot" style="background:#201f1f"></span><span class="dot" style="background:#2d2c2c"></span><span class="dot" style="background:#6264a7"></span></div></div>
      <div class="theme-card active"><div><div class="theme-title">🌌 OLED Midnight <span class="theme-badge">Active</span></div><div class="theme-desc">True pitch black &amp; neon blue</div></div><div class="swatches"><span class="dot" style="background:#000"></span><span class="dot" style="background:#121212"></span><span class="dot" style="background:#38bdf8"></span></div></div>
      <div class="theme-card"><div><div class="theme-title">☕ Catppuccin Mocha</div><div class="theme-desc">Soothing pastel &amp; mauve</div></div><div class="swatches"><span class="dot" style="background:#1e1e2e"></span><span class="dot" style="background:#313244"></span><span class="dot" style="background:#cba6f7"></span></div></div>
      <div class="theme-card"><div><div class="theme-title">❄️ Nord Frost</div><div class="theme-desc">Arctic slates &amp; polar cyan</div></div><div class="swatches"><span class="dot" style="background:#2e3440"></span><span class="dot" style="background:#3b4252"></span><span class="dot" style="background:#88c0d0"></span></div></div>
      <div class="theme-card"><div><div class="theme-title">🌆 Tokyo Night</div><div class="theme-desc">Deep navy &amp; neon cyan</div></div><div class="swatches"><span class="dot" style="background:#1a1b26"></span><span class="dot" style="background:#24283b"></span><span class="dot" style="background:#7dcfff"></span></div></div>
      <div class="theme-card"><div><div class="theme-title">🧛 Dracula</div><div class="theme-desc">Dark slate &amp; neon pink</div></div><div class="swatches"><span class="dot" style="background:#282a36"></span><span class="dot" style="background:#44475a"></span><span class="dot" style="background:#ff79c6"></span></div></div>
      <div class="theme-card"><div><div class="theme-title">🌸 Rosé Pine</div><div class="theme-desc">Warm dusk &amp; rose gold</div></div><div class="swatches"><span class="dot" style="background:#191724"></span><span class="dot" style="background:#26233a"></span><span class="dot" style="background:#ebbcba"></span></div></div>
    </div>
  </div>
  <div>
    <div class="theme-gallery">
      <div class="mini-app" style="border-color:#262626;"><div class="mini-app-bar" style="background:#080808; color:#fff;"><span>🌌 OLED</span><span style="color:#38bdf8;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#080808; color:#a3a3a3;"># General</div><div class="mini-main" style="background:#000; color:#fff;"><span>Chat</span><span class="mini-btn" style="background:#38bdf8; color:#000;">Join</span></div></div></div>
      <div class="mini-app" style="border-color:#313244;"><div class="mini-app-bar" style="background:#181825; color:#cdd6f4;"><span>☕ Mocha</span><span style="color:#cba6f7;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#181825; color:#a6adc8;"># General</div><div class="mini-main" style="background:#1e1e2e; color:#cdd6f4;"><span>Chat</span><span class="mini-btn" style="background:#cba6f7; color:#111;">Join</span></div></div></div>
      <div class="mini-app" style="border-color:#434c5e;"><div class="mini-app-bar" style="background:#242933; color:#eceff4;"><span>❄️ Nord</span><span style="color:#88c0d0;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#242933; color:#d8dee9;"># General</div><div class="mini-main" style="background:#2e3440; color:#eceff4;"><span>Chat</span><span class="mini-btn" style="background:#88c0d0; color:#111;">Join</span></div></div></div>
      <div class="mini-app" style="border-color:#292e42;"><div class="mini-app-bar" style="background:#16161e; color:#c0caf5;"><span>🌆 Tokyo</span><span style="color:#7dcfff;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#16161e; color:#787c99;"># General</div><div class="mini-main" style="background:#1a1b26; color:#c0caf5;"><span>Chat</span><span class="mini-btn" style="background:#7dcfff; color:#111;">Join</span></div></div></div>
      <div class="mini-app" style="border-color:#44475a;"><div class="mini-app-bar" style="background:#1e1f29; color:#f8f8f2;"><span>🧛 Dracula</span><span style="color:#ff79c6;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#1e1f29; color:#d6d6d4;"># General</div><div class="mini-main" style="background:#282a36; color:#f8f8f2;"><span>Chat</span><span class="mini-btn" style="background:#ff79c6; color:#111;">Join</span></div></div></div>
      <div class="mini-app" style="border-color:#403d52;"><div class="mini-app-bar" style="background:#14121e; color:#e0def4;"><span>🌸 Rosé</span><span style="color:#ebbcba;">●</span></div><div class="mini-app-body"><div class="mini-side" style="background:#14121e; color:#908caa;"># General</div><div class="mini-main" style="background:#191724; color:#e0def4;"><span>Chat</span><span class="mini-btn" style="background:#ebbcba; color:#111;">Join</span></div></div></div>
    </div>
    <div class="callout callout-info" style="margin-top:5px;">
      <strong>Multi-Account Profiles, Privacy Lock &amp; Updates:</strong> Switch between isolated accounts via <strong>File &rarr; Switch Account Profile</strong>, blur your screen anytime with <strong>Ctrl+L</strong>, and check for new versions via <strong>Help &rarr; Check for Updates</strong>.
    </div>
  </div>
</div>

<h1><span>6.</span> Preferences Reference (<code>Ctrl + ,</code>) &amp; Shortcuts</h1>
<table class="avoid-break">
  <thead><tr><th>Setting / Shortcut</th><th>What It Does</th><th>Default</th></tr></thead>
  <tbody>
    <tr><td><strong>Low-Hardware / Potato PC Mode</strong></td><td>Caps V8 heap to 896MB, lowers cache, enables 0% CPU camera pass-through</td><td><code>false</code></td></tr>
    <tr><td><strong>Active Account Profile</strong></td><td>Isolated sessions for Work 1, Work 2, and Personal without logging out</td><td><code>default</code></td></tr>
    <tr><td><strong>Adaptive Guardian &amp; Bandwidth</strong></td><td>Auto (720p&rarr;480p&rarr;360p&rarr;Audio-First) or lock a manual preset</td><td><code>Auto</code></td></tr>
    <tr><td><strong>Privacy Lock (<code>Ctrl + L</code>)</strong></td><td>Blurs screen behind optional 4-digit PIN when stepping away from desk</td><td>Optional PIN</td></tr>
    <tr><td><strong>Stepped Away Slate (<code>Ctrl+Shift+V</code>)</strong></td><td>Shows static away slate &amp; pauses camera rendering (0% CPU)</td><td>Off</td></tr>
    <tr><td><strong>Loud Office Call Alert</strong></td><td>Plays a clear dual-tone chime when an incoming call rings</td><td><code>false</code></td></tr>
    <tr><td><strong>Double-Close Exit (<code>X</code> &times; 2)</strong></td><td>Click close twice within 2.5s for instant shutdown with 1.5s fail-safe</td><td>Always Active</td></tr>
  </tbody>
</table>

<div class="disclaimer-box avoid-break">
  <strong>Legal Disclaimer:</strong> Teamux is an independent open-source project by Quiet Byte and is not affiliated with or endorsed by Microsoft Corporation. Microsoft Teams &amp; Windows are trademarks of Microsoft Corporation. Licensed under Apache-2.0.
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
