#!/usr/bin/env python3
"""
Teamux v1.0.0 Official User Guide & Feature Manual PDF Generator
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

# Read icon as base64
with open(ICON_PATH, "rb") as f:
    icon_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Teamux v1.0.0 — Official User Guide & Feature Manual</title>
<style>
  @page {{
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
    @bottom-right {{
      content: "Page " counter(page);
      font-size: 9pt;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #64748b;
    }}
    @bottom-left {{
      content: "Teamux v1.0.0 — Official User Guide (Quiet Byte)";
      font-size: 8.5pt;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #64748b;
    }}
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }}

  /* Page Break Helpers */
  .page-break {{
    page-break-before: always;
  }}
  .avoid-break {{
    page-break-inside: avoid;
  }}

  /* Cover / Header Section */
  .cover-header {{
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #312e81 100%);
    color: #ffffff;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .cover-info {{
    max-width: 72%;
  }}
  .cover-title {{
    font-size: 24pt;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0 0 4px 0;
    color: #ffffff;
  }}
  .cover-subtitle {{
    font-size: 12pt;
    font-weight: 400;
    color: #c7d2fe;
    margin: 0 0 12px 0;
    line-height: 1.35;
  }}
  .cover-meta {{
    font-size: 8.5pt;
    color: #94a3b8;
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }}
  .cover-meta span {{
    background: rgba(255, 255, 255, 0.12);
    padding: 3px 8px;
    border-radius: 6px;
    color: #f8fafc;
    font-weight: 500;
  }}
  .cover-logo {{
    width: 96px;
    height: 96px;
    border-radius: 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    background: #ffffff;
    padding: 4px;
  }}

  /* Typography */
  h1, h2, h3, h4 {{
    color: #0f172a;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 8px;
  }}
  h1 {{
    font-size: 16pt;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 6px;
    color: #1e1b4b;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  h2 {{
    font-size: 13pt;
    color: #312e81;
    margin-top: 16px;
  }}
  h3 {{
    font-size: 11pt;
    color: #0f172a;
  }}
  p {{
    margin: 0 0 8px 0;
  }}

  /* Callout Boxes */
  .callout {{
    padding: 10px 14px;
    border-radius: 8px;
    margin: 12px 0;
    font-size: 9.5pt;
    line-height: 1.45;
  }}
  .callout-info {{
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    color: #1e40af;
  }}
  .callout-success {{
    background: #f0fdf4;
    border-left: 4px solid #22c55e;
    color: #15803d;
  }}
  .callout-warning {{
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    color: #b45309;
  }}
  .callout-danger {{
    background: #fef2f2;
    border-left: 4px solid #ef4444;
    color: #b91c1c;
  }}

  /* Step Boxes */
  .step-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 10px;
  }}
  .step-title {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 10.5pt;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 6px;
  }}
  .step-badge {{
    background: #4f46e5;
    color: #ffffff;
    font-size: 8pt;
    font-weight: 800;
    width: 20px;
    height: 20px;
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
    gap: 12px;
    margin: 10px 0;
  }}
  .card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }}
  .card-title {{
    font-size: 10.5pt;
    font-weight: 700;
    color: #1e1b4b;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .card-body {{
    font-size: 9pt;
    color: #475569;
    line-height: 1.45;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9pt;
  }}
  th, td {{
    padding: 7px 10px;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
  }}
  th {{
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 700;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  /* Code Blocks */
  code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    padding: 2px 5px;
    border-radius: 4px;
    color: #475569;
  }}
  pre {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 8.5pt;
    background: #0f172a;
    color: #e2e8f0;
    padding: 9px 12px;
    border-radius: 6px;
    overflow-x: hidden;
    margin: 8px 0;
    line-height: 1.4;
  }}

  /* Status Badges */
  .badge {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 12px;
    font-size: 8pt;
    font-weight: 700;
    color: white;
  }}
  .badge-720p {{ background: #2563eb; }}
  .badge-480p {{ background: #059669; }}
  .badge-360p {{ background: #d97706; }}
  .badge-audio {{ background: #dc2626; }}

  /* Footer Disclaimer */
  .disclaimer-box {{
    margin-top: 24px;
    padding: 10px 14px;
    border-radius: 8px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    font-size: 8pt;
    color: #64748b;
    text-align: center;
    line-height: 1.4;
  }}
</style>
</head>
<body>

<!-- COVER HEADER -->
<div class="cover-header">
  <div class="cover-info">
    <div class="cover-title">Teamux v1.0.0</div>
    <div class="cover-subtitle">Official User Guide & Comprehensive Feature Manual</div>
    <div class="cover-meta">
      <span>Release: v1.0.0 (Production)</span>
      <span>Platforms: Linux (x64) &amp; Windows (x64)</span>
      <span>Publisher: Quiet Byte</span>
      <span>License: Apache-2.0</span>
    </div>
  </div>
  <img class="cover-logo" src="data:image/png;base64,{icon_b64}" alt="Teamux Logo">
</div>

<!-- SECTION 1: INTRODUCTION & OVERVIEW -->
<h1><span>1.</span> Introduction &amp; Core Highlights</h1>
<p>
  <strong>Teamux</strong> is an unofficial, high-performance desktop client for Microsoft Teams engineered specifically for demanding enterprise workflows, branch-office internet environments, and modern Linux and Windows desktops.
</p>

<div class="grid-2 avoid-break">
  <div class="card">
    <div class="card-title">🛡️ Adaptive Network Guardian</div>
    <div class="card-body">
      Real-time WebRTC telemetry monitoring that continuously tracks RTT latency, packet loss, and available bandwidth. Auto-scales video from 720p to 480p and 360p, with an emergency <strong>Audio-First Mode</strong> that cuts video upload to 0 kbps so voice audio never drops.
    </div>
  </div>
  <div class="card">
    <div class="card-title">🧊 Zero-Freeze &amp; Instant Exit</div>
    <div class="card-body">
      Re-engineered process architecture featuring single-instance camera lifecycle tracking, display-synced frame callbacks, top-frame iframe isolation, a double-close escape hatch, and a 1.5-second forced exit watchdog timer.
    </div>
  </div>
  <div class="card">
    <div class="card-title">✨ In-Meeting Studio Beauty Cam</div>
    <div class="card-body">
      Built-in virtual camera processing right inside Teams: skin tone smoothing, studio lighting booster, portrait vignette focus, and full tone grading (contrast, saturation, shadow lift, warm ambience glow, and monochrome grayscale).
    </div>
  </div>
  <div class="card">
    <div class="card-title">🎭 Custom Themes Engine</div>
    <div class="card-body">
      Seamlessly injects 6 curated UI themes directly into Teams: OLED Pure Black (battery saver), Catppuccin Mocha, Nord Frost, Tokyo Night, Dracula, and Rosé Pine.
    </div>
  </div>
</div>

<div class="callout callout-info avoid-break">
  <strong>📌 Privacy &amp; Local Execution Guarantee:</strong> All Studio video processing and telemetry analytics execute 100% locally on your machine's hardware using Chromium's internal canvas pipeline. No video streams, camera frames, or private meeting data are ever transmitted to external AI servers.
</div>

<!-- SECTION 2: INSTALLATION & GETTING STARTED -->
<h1><span>2.</span> Step-by-Step Installation &amp; Setup</h1>

<h2>🐧 Linux Installation Options</h2>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">A</span> Universal AppImage (Recommended — Works on Any Linux Distro)</div>
  <p>The AppImage requires zero installation and no root/sudo privileges:</p>
  <pre># 1. Download teamux-v1.0.0-linux-x86_64.AppImage from GitHub Releases
# 2. Open terminal and mark the file executable:
chmod +x teamux-v1.0.0-linux-x86_64.AppImage

# 3. Launch Teamux:
./teamux-v1.0.0-linux-x86_64.AppImage</pre>
  <p style="font-size:8.5pt; color:#64748b; margin-top:4px;">
    <em>Tip:</em> To launch Teamux from your application launcher, place the file in <code>~/.local/share/teamux/teamux.AppImage</code>. A desktop entry will automatically be created.
  </p>
</div>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">B</span> Ubuntu / Debian / Linux Mint / Pop!_OS (.deb Package)</div>
  <pre># Install using dpkg or apt:
sudo dpkg -i teamux-v1.0.0-linux-amd64.deb
# Or resolve any missing system dependencies automatically:
sudo apt install ./teamux-v1.0.0-linux-amd64.deb</pre>
</div>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">C</span> Portable Tarball (.tar.gz)</div>
  <pre>tar -xvf teamux-v1.0.0-linux-x64.tar.gz
cd teamux-1.0.0
./teamux</pre>
</div>

<h2>🪟 Windows Installation Options</h2>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">1</span> Portable Single-File Executable (.exe)</div>
  <p>
    Download <code>teamux-v1.0.0-windows-portable-x64.exe</code> from GitHub Releases. Double-click to launch immediately. No installer, no administrator privileges required. You can run it directly from your Downloads folder, Desktop, or a USB flash drive.
  </p>
</div>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">2</span> Standalone Zip Archive (.zip)</div>
  <p>
    Download <code>teamux-v1.0.0-windows-x64.zip</code>, extract the folder to your preferred directory (e.g. <code>C:\Apps\Teamux</code>), and double-click <code>Teamux.exe</code>.
  </p>
</div>

<div class="page-break"></div>

<!-- SECTION 3: SIGNING IN & BASIC NAVIGATION -->
<h1><span>3.</span> Signing In &amp; Core Navigation</h1>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">1</span> Choosing Your Teams Environment</div>
  <p>
    Teamux supports both enterprise and personal Microsoft accounts:
  </p>
  <ul>
    <li><strong>Work / School (New Teams v2):</strong> Uses <code>teams.cloud.microsoft</code>. Supports enterprise M365 accounts, channels, calendar, breakout rooms, and tenant switching.</li>
    <li><strong>Personal (Teams Live):</strong> Uses <code>teams.live.com</code>. Supports personal Microsoft accounts (Outlook.com, Hotmail, Xbox).</li>
  </ul>
  <p>
    <em>To switch:</em> Open Preferences (<code>Ctrl + ,</code>) and select your desired environment from the dropdown.
  </p>
</div>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">2</span> Authentication &amp; Multi-Factor Authentication (MFA)</div>
  <p>
    Enter your corporate email and password. Teamux natively supports Microsoft Authenticator, FIDO2 hardware security keys, SMS codes, and Single Sign-On (SSO) redirects without session drops.
  </p>
</div>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">3</span> System Tray &amp; Unread Badges</div>
  <p>
    When Teamux is running, an icon appears in your System Tray:
  </p>
  <ul>
    <li><strong>Unread Count Badge:</strong> Shows real-time badge count (e.g. <code>(3)</code>) directly on the tray icon and taskbar dock.</li>
    <li><strong>Tray Context Menu:</strong> Right-click the tray icon to access quick actions:
      <ul>
        <li><code>Show Teamux</code> / <code>Hide Teamux</code>: Toggle main window visibility.</li>
        <li><code>Unread Messages: X</code>: View current unread count.</li>
        <li><code>Reload Teams</code>: Refresh the interface if web contents stall.</li>
        <li><code>Preferences</code>: Open settings window.</li>
        <li><code>Quit Teamux</code>: Safely exit all processes.</li>
      </ul>
    </li>
  </ul>
</div>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">4</span> Guaranteed Clean Exit (Double-Close Escape Hatch)</div>
  <p>
    To ensure Teamux never hangs or traps you in an invisible background loop:
  </p>
  <ul>
    <li><strong>Single Click Close:</strong> Minimizes or closes the window according to your preferences.</li>
    <li><strong>⚡ Double-Close Escape Hatch:</strong> If you press the window close button (<code>X</code>) <strong>twice within 2.5 seconds</strong>, Teamux immediately bypasses all background tray loops and terminates instantly.</li>
    <li><strong>1.5-Second Fail-Safe Timer:</strong> A built-in kernel shutdown hook guarantees that all child GPU and WebRTC processes are cleanly terminated within 1500ms of exit.</li>
  </ul>
</div>

<!-- SECTION 4: ADAPTIVE NETWORK GUARDIAN -->
<h1><span>4.</span> Adaptive Network Guardian (Low-Bandwidth Optimizer)</h1>

<p>
  Branch offices, remote sites, cellular hotspots, and satellite links often suffer from network latency spikes, packet loss, or constrained uplink capacity. Under standard Teams, video upload monopolizes the uplink, resulting in garbled audio, video freeze, or dropped calls. The <strong>Adaptive Network Guardian</strong> eliminates this problem.
</p>

<h2>How the Guardian Protects Your Call</h2>
<p>
  Teamux hooks into the WebRTC peer connection statistics engine, evaluating network metrics every 2.5 seconds:
</p>

<table class="avoid-break">
  <thead>
    <tr>
      <th>Quality Tier</th>
      <th>Resolution &amp; Framerate</th>
      <th>Upload Bitrate</th>
      <th>Network Triggers</th>
      <th>Guardian Action</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span class="badge badge-720p">720p Full HD</span></td>
      <td>1280 &times; 720 @ 30 FPS</td>
      <td>~2,000 kbps (2.0 Mbps)</td>
      <td>Ping &lt; 130 ms, Loss &lt; 2%</td>
      <td>Optimal network: full high-definition video output.</td>
    </tr>
    <tr>
      <td><span class="badge badge-480p">480p Balanced</span></td>
      <td>854 &times; 480 @ 20 FPS</td>
      <td>~500 kbps (0.5 Mbps)</td>
      <td>Ping 130–260 ms, Loss 2–6%</td>
      <td>Cuts upload bandwidth by 75% while keeping video sharp.</td>
    </tr>
    <tr>
      <td><span class="badge badge-360p">360p Eco Saver</span></td>
      <td>640 &times; 360 @ 15 FPS</td>
      <td>~250 kbps (0.25 Mbps)</td>
      <td>Ping 260–500 ms, Loss 6–15%</td>
      <td>Deep 87% bandwidth savings for congested office links.</td>
    </tr>
    <tr>
      <td><span class="badge badge-audio">Audio-First Priority</span></td>
      <td>Static Slate @ 1 FPS</td>
      <td>~0 kbps (Video paused)</td>
      <td>Ping &gt; 500 ms, Loss &gt; 15%</td>
      <td><strong>Voice Protection:</strong> Pauses video upload so call voice audio is 100% clear. Auto-recovers when bandwidth returns.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h2>Step-by-Step: Using the Network Guardian During a Meeting</h2>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">1</span> Open Teamux Studio in Any Call</div>
  <p>
    When you join a meeting or test your camera, look at the bottom-right corner of the Teams window. You will see the floating <strong>✨ Studio</strong> pill displaying your active video tier (e.g. <code>✨ Studio [720p]</code>). Click the pill to open the controller.
  </p>
</div>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">2</span> Switch to the 🌐 Network Tab</div>
  <p>
    Click the fourth tab labeled <strong>🌐 Network</strong>. You will see:
  </p>
  <ul>
    <li><strong>Adaptive Guardian Toggle:</strong> Turn the auto-guardian on or off. (Default: On).</li>
    <li><strong>Bandwidth Profile Dropdown:</strong> Select <code>Auto (Dynamic Guardian)</code>, or manually lock your stream to <code>720p</code>, <code>480p</code>, <code>360p</code>, or <code>Audio-First Priority</code>.</li>
    <li><strong>Live WebRTC Telemetry Card:</strong>
      <ul>
        <li><code>Latency (RTT)</code>: Displays current round-trip network ping in milliseconds.</li>
        <li><code>Packet Loss</code>: Shows real-time packet loss percentage (turns red if &gt; 5%).</li>
        <li><code>Est. Bandwidth</code>: Live available outgoing bitrate calculated by WebRTC.</li>
        <li><code>Active Video Stream</code>: Shows the resolution currently transmitting to attendees.</li>
      </ul>
    </li>
  </ul>
</div>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">3</span> How Audio-First Mode Works Automatically</div>
  <p>
    If someone at your branch office starts a large file transfer and your ping surges past 500ms:
  </p>
  <ol>
    <li>The Guardian instantly engages <strong>Audio-First Mode</strong>.</li>
    <li>Your video upload is paused, cutting outgoing video bandwidth to zero.</li>
    <li>Meeting participants see a clean dark slate: <em>"🔴 Audio-First Mode Active: Video upload paused to protect voice audio quality. Resuming automatically when network clears."</em></li>
    <li>Your call voice audio remains <strong>100% crisp and uninterrupted</strong> without robotic distortion.</li>
    <li>The top meeting recovery banner updates to red: <code>🔴 Audio-First Protection Active (Low Bandwidth)</code>.</li>
    <li>When network latency drops back to normal for 3 consecutive samples (~7.5s), Teamux automatically restores your video feed.</li>
  </ol>
</div>

<div class="callout callout-warning avoid-break">
  <strong>💡 Tip for Low-Bandwidth Branch Offices:</strong> If your office internet is permanently slow (&lt; 1 Mbps uplink), you can set your Bandwidth Profile to <code>360p Eco Saver</code> permanently in <strong>Preferences &gt; Network Guardian</strong>. This ensures you never saturate the branch uplink during all-hands video calls.
</div>

<!-- SECTION 5: IN-MEETING STUDIO CONTROLLER -->
<h1><span>5.</span> In-Meeting Studio Camera Controller</h1>

<p>
  The Teamux Studio widget lets you enhance your appearance, fix dim webcam hardware, and grade your video feed in real time without third-party virtual camera software.
</p>

<div class="grid-2 avoid-break">
  <div class="card">
    <div class="card-title">✨ Retouch Tab</div>
    <div class="card-body">
      <ul>
        <li><strong>Beauty Filter:</strong> Bilateral skin tone smoothing that reduces camera noise and blemishes while preserving facial sharpness. Slider adjustable from 10% to 100%.</li>
        <li><strong>Studio Lighting:</strong> Intelligent shadow illumination that brightens your face in dim offices or backlit windows.</li>
        <li><strong>Portrait Vignette Focus:</strong> Soft radial edge contrast drawing visual focus directly to you.</li>
      </ul>
    </div>
  </div>
  <div class="card">
    <div class="card-title">🎨 Tone &amp; Color Tab</div>
    <div class="card-body">
      <ul>
        <li><strong>Grayscale Toggle:</strong> High-definition black and white stream for professional interviews or low-light situations.</li>
        <li><strong>Contrast Slider (50% to 150%):</strong> Adjust tonal separation.</li>
        <li><strong>Saturation Slider (0% to 200%):</strong> Enrich washed-out colors.</li>
        <li><strong>Shadow Lift (-50 to +50):</strong> Recover details lost in dark shadows.</li>
        <li><strong>Warm Ambience (0% to 100%):</strong> Add a warm golden tint.</li>
      </ul>
    </div>
  </div>
</div>

<div class="step-box avoid-break">
  <div class="step-title">👁️ Hold-to-Compare Feature</div>
  <p>
    At the bottom of the Studio card, click and hold the <strong>👁️ Hold to Compare</strong> button. While held, your video preview instantly switches to the raw, unprocessed camera feed. Release the button to return to your enhanced stream. This makes calibrating your beauty and tone settings effortless.
  </p>
</div>

<div class="page-break"></div>

<!-- SECTION 6: CUSTOM THEMES ENGINE -->
<h1><span>6.</span> Custom Themes Engine</h1>

<p>
  Teamux includes a real-time CSS theme injection engine that customizes the entire Microsoft Teams interface (chats, channels, navigation bar, and settings):
</p>

<table class="avoid-break">
  <thead>
    <tr>
      <th>Theme</th>
      <th>Primary Background</th>
      <th>Accent Color</th>
      <th>Best For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>🖤 OLED Pure Black</strong></td>
      <td><code>#000000</code></td>
      <td><code>#6366f1</code> (Indigo)</td>
      <td>OLED laptops, dark rooms, maximum battery savings.</td>
    </tr>
    <tr>
      <td><strong>☕ Catppuccin Mocha</strong></td>
      <td><code>#1e1e2e</code></td>
      <td><code>#cba6f7</code> (Lavender)</td>
      <td>Warm, soothing pastel palette; reduces eye fatigue.</td>
    </tr>
    <tr>
      <td><strong>❄️ Nord Frost</strong></td>
      <td><code>#2e3440</code></td>
      <td><code>#88c0d0</code> (Glacial Blue)</td>
      <td>Clean Nordic aesthetic with calm slate contrasts.</td>
    </tr>
    <tr>
      <td><strong>🌃 Tokyo Night</strong></td>
      <td><code>#1a1b26</code></td>
      <td><code>#7aa2f7</code> (Neon Blue)</td>
      <td>Cyberpunk-inspired deep indigo with vibrant highlights.</td>
    </tr>
    <tr>
      <td><strong>🧛 Dracula</strong></td>
      <td><code>#282a36</code></td>
      <td><code>#bd93f9</code> (Purple)</td>
      <td>High-contrast, beloved developer dark theme.</td>
    </tr>
    <tr>
      <td><strong>🌸 Rosé Pine</strong></td>
      <td><code>#191724</code></td>
      <td><code>#eb6f92</code> (Rose)</td>
      <td>Minimalist, muted natural pine, rose, and gold tones.</td>
    </tr>
  </tbody>
</table>

<div class="step-box avoid-break">
  <div class="step-title"><span class="step-badge">→</span> How to Change Your App Theme</div>
  <p>
    Open the Studio widget during any call or camera preview, click the <strong>🎭 Themes</strong> tab, and click any theme card. The theme is applied instantly across all windows and persisted across app restarts.
  </p>
</div>

<!-- SECTION 7: SCREEN & WINDOW SHARING -->
<h1><span>7.</span> Screen &amp; Window Sharing Guide</h1>

<h2>Linux (Wayland &amp; PipeWire)</h2>
<p>
  On modern Linux desktops running Wayland (GNOME, KDE Plasma, Sway), Teamux communicates with the system desktop portal (<code>xdg-desktop-portal</code>) via PipeWire:
</p>
<ol>
  <li>In a Teams meeting, click the <strong>Share</strong> button.</li>
  <li>Teamux opens the native desktop portal picker showing live thumbnails of all active monitors and individual application windows.</li>
  <li>Select your display or window and click <strong>Share</strong>.</li>
  <li>Hardware-accelerated PipeWire streaming delivers 30 FPS screen sharing without black screens or cursor flicker.</li>
</ol>

<h2>Windows 10 &amp; 11</h2>
<p>
  Click <strong>Share</strong>, then select either an entire display or an individual application window. Hardware acceleration ensures smooth video playback and high-DPI font sharpness.
</p>

<!-- SECTION 8: PREFERENCES REFERENCE -->
<h1><span>8.</span> Settings &amp; Preferences Reference</h1>
<p>
  Open Preferences anytime by pressing <code>Ctrl + ,</code> or via <strong>File &gt; Preferences</strong>:
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
    <tr>
      <td><strong>Adaptive Guardian</strong></td>
      <td>Auto-throttle video bitrate based on network congestion</td>
      <td><code>true</code> (Enabled)</td>
      <td>Keep enabled for all remote &amp; branch offices.</td>
    </tr>
    <tr>
      <td><strong>Bandwidth Profile</strong></td>
      <td>Target video upload preset (Auto, 720p, 480p, 360p, Audio)</td>
      <td><code>Auto (Adaptive)</code></td>
      <td>Select <code>360p</code> for very slow links (&lt; 1 Mbps).</td>
    </tr>
    <tr>
      <td><strong>Teams Environment</strong></td>
      <td>Switch between Work/School v2 and Personal</td>
      <td><code>Work/School v2</code></td>
      <td>Set to <code>Work/School v2</code> for enterprise accounts.</td>
    </tr>
    <tr>
      <td><strong>Keep running in tray</strong></td>
      <td>Keep running in background when window is closed</td>
      <td><code>false</code> (Disabled)</td>
      <td>Leave disabled to ensure immediate clean exit.</td>
    </tr>
    <tr>
      <td><strong>Minimize to tray</strong></td>
      <td>Minimize window directly to system tray</td>
      <td><code>true</code> (Enabled)</td>
      <td>Useful for receiving background call notifications.</td>
    </tr>
    <tr>
      <td><strong>Hardware Acceleration</strong></td>
      <td>GPU rasterization and VA-API hardware decode</td>
      <td><code>true</code> (Enabled)</td>
      <td>Keep enabled for minimum CPU utilization.</td>
    </tr>
    <tr>
      <td><strong>Unread Badges</strong></td>
      <td>Display badge counter on tray and dock</td>
      <td><code>true</code> (Enabled)</td>
      <td>Provides instant visibility of missed messages.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- SECTION 9: TROUBLESHOOTING & FAQ -->
<h1><span>9.</span> Troubleshooting &amp; FAQs</h1>

<div class="step-box avoid-break">
  <div class="step-title">Q: My camera shows a black screen or fails to initialize.</div>
  <p>
    <strong>Linux:</strong> Verify your user belongs to the <code>video</code> group: <code>sudo usermod -a -G video $USER</code>, then log out and back in. Check if another application (e.g. OBS or Zoom) is holding an exclusive lock on <code>/dev/video0</code>.<br>
    <strong>Windows:</strong> Go to <em>Windows Settings &gt; Privacy &amp; Security &gt; Camera</em> and ensure "Allow desktop apps to access your camera" is toggled ON.
  </p>
</div>

<div class="step-box avoid-break">
  <div class="step-title">Q: Screen sharing yields a black screen on Linux Wayland.</div>
  <p>
    Verify PipeWire and the desktop portal are running:
  </p>
  <pre>systemctl --user status pipewire
# For GNOME on Ubuntu/Debian:
sudo apt install xdg-desktop-portal xdg-desktop-portal-gnome
# For KDE:
sudo apt install xdg-desktop-portal xdg-desktop-portal-kde</pre>
</div>

<div class="step-box avoid-break">
  <div class="step-title">Q: The app does not quit or hangs when closing.</div>
  <p>
    In Teamux v1.0.0, use the <strong>Double-Close Escape Hatch</strong>: click the window close button (<code>X</code>) twice within 2.5 seconds. Teamux will immediately terminate all processes cleanly. You can also right-click the System Tray icon and select <strong>Quit Teamux</strong>.
  </p>
</div>

<div class="step-box avoid-break">
  <div class="step-title">Q: Does the Studio Beauty Filter work in Microsoft Teams recordings?</div>
  <p>
    Yes! Because the Studio enhancements are applied directly to the camera stream inside Chromium before WebRTC transmission, all meeting attendees, call recordings, and live streams receive the enhanced video feed.
  </p>
</div>

<div class="step-box avoid-break">
  <div class="step-title">Q: Where can I report bugs or download new updates?</div>
  <p>
    Visit the official GitHub repository: <a href="https://github.com/quietbytehq/teamux">https://github.com/quietbytehq/teamux</a><br>
    Releases: <a href="https://github.com/quietbytehq/teamux/releases">https://github.com/quietbytehq/teamux/releases</a><br>
    Email support: <a href="mailto:hello@quietbytehq.uk">hello@quietbytehq.uk</a>
  </p>
</div>

<!-- DISCLAIMER -->
<div class="disclaimer-box avoid-break">
  <strong>Legal Disclaimer:</strong> Teamux is an independent open-source project and is not affiliated with, endorsed, or sponsored by Microsoft Corporation. Microsoft, Microsoft Teams, and Windows are trademarks of Microsoft Corporation. All code is licensed under the Apache License 2.0. Published by <strong>Quiet Byte</strong>.
</div>

</body>
</html>
"""

with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML guide generated at: {HTML_OUTPUT}")

# Render to PDF using Chromium headless
cmd = [
    "/snap/bin/chromium",
    "--headless",
    "--no-sandbox",
    "--disable-gpu",
    f"--print-to-pdf={PDF_OUTPUT}",
    "--print-to-pdf-no-header",
    HTML_OUTPUT
]

print("Rendering PDF via Chromium...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print(f"Chromium PDF render error: {res.stderr}")
    sys.exit(1)

print(f"PDF successfully rendered to: {PDF_OUTPUT}")

# Copy to accessible locations
subprocess.run(["cp", PDF_OUTPUT, USER_PDF_COPY])
print(f"Copied PDF to: {USER_PDF_COPY}")

# Also copy to Games workspace if available
if os.path.exists("/home/faisal/Games"):
    games_copy = "/home/faisal/Games/Teamux_User_Guide_v1.0.0.pdf"
    subprocess.run(["cp", PDF_OUTPUT, games_copy])
    print(f"Copied PDF to: {games_copy}")
