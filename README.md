# Teamux 🐧🪟

<p align="center">
  <img src="assets/icon.png" alt="Teamux Logo" width="128" height="128" />
</p>

<p align="center">
  <strong>Unofficial Microsoft Teams desktop client for Linux and Windows with Adaptive Network Guardian, Studio Camera, and low-bandwidth optimization.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License: Apache-2.0"></a>
  <a href="#"><img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20x64-lightgrey.svg" alt="Supported Platforms"></a>
  <a href="#"><img src="https://img.shields.io/badge/display-Wayland%20%26%20X11-purple.svg" alt="Display Server Support"></a>
  <a href="#"><img src="https://img.shields.io/badge/audio%2Fvideo-PipeWire%20%26%20WebRTC-orange.svg" alt="Audio Video Support"></a>
</p>

> **Disclaimer:** Teamux is an unofficial project and is not affiliated with or endorsed by Microsoft. Microsoft Teams is a trademark of Microsoft Corporation.

---

## 💡 Why Teamux?

Standard Teams often struggles in demanding environments and branch offices:
* **Meeting drops on low bandwidth:** When branch office internet links experience congestion, video calls stutter, drop frames, or freeze entirely.
* **Wayland & PipeWire black screens:** Modern Linux desktops (Ubuntu 22.04+, Fedora 38+, Arch, Debian 12+) frequently experience black screens during screen sharing.
* **Camera permission & resource leaks:** Camera devices either lock up or cause background CPU spikes when switching calls or hardware devices.
* **Rigid UI styling:** No native OLED dark mode or low-contrast aesthetic options for extended workdays.

**Teamux v1.0.0** solves all of these problems out of the box with zero manual flag tinkering required.

---

## ✨ Features

- 🛡️ **Adaptive Network Guardian (Branch-Office Bandwidth Optimizer):**
  - **Live WebRTC Telemetry:** Continuously tracks round-trip ping latency (RTT), packet loss percentage, and available outgoing bandwidth.
  - **Dynamic Tier Scaling:** Automatically shifts camera feed between Full HD (720p @ 2.0 Mbps), Balanced (480p @ 500 kbps), and Eco Saver (360p @ 250 kbps).
  - **Fail-Safe Audio-First Mode:** If network drops severely (>500ms ping or >15% packet loss), video upload is paused with a clean informational slate to prioritize 100% of bandwidth for uninterrupted call audio, smoothly recovering video when the link stabilizes.
  - **Manual Bandwidth Presets:** Force specific bandwidth profiles directly from the in-meeting Studio widget or Settings.
- ✨ **In-Meeting Studio Controller:**
  - Real-time **Skin Smoothing (Beauty Filter)** with adjustable intensity.
  - **Studio Lighting Enhancer** to balance dim webcams.
  - **Portrait Vignette Focus** with soft radial contrast.
  - Tone and color adjustments: **Contrast, Saturation, Shadow Lift, Warm Ambience**, and one-click **Grayscale**.
  - **Hold-to-Compare** button to instantly preview raw camera output vs. enhanced stream.
- 🎭 **Custom App Themes Engine:**
  - Seamlessly injects curated UI themes into Teams: **OLED Pure Black, Catppuccin Mocha, Nord Frost, Tokyo Night, Dracula, and Rosé Pine**.
- 🖥️ **Cross-Platform Linux & Windows:**
  - Full native **Wayland** support via PipeWire and `xdg-desktop-portal` alongside X11 fallback.
  - Windows standalone portable `.exe` and `.zip` distribution.
  - Cross-platform System Tray icon with dynamic unread message count badges.
  - Single-instance camera management and leak-free render loop architecture.

---

## 📦 Downloads & Installation (v1.0.0)

Download official v1.0.0 binaries directly from [Releases](https://github.com/quietbytehq/teamux/releases):

### 🐧 Linux

#### 1. Universal (Any Linux Distro) — AppImage
```bash
chmod +x teamux-v1.0.0-linux-x86_64.AppImage
./teamux-v1.0.0-linux-x86_64.AppImage
```

#### 2. Ubuntu / Debian / Linux Mint / Pop!_OS — `.deb`
```bash
sudo dpkg -i teamux-v1.0.0-linux-amd64.deb
# Or using apt:
sudo apt install ./teamux-v1.0.0-linux-amd64.deb
```

#### 3. Portable Tarball — `.tar.gz`
```bash
tar -xvf teamux-v1.0.0-linux-x64.tar.gz
cd teamux-1.0.0
./teamux
```

### 🪟 Windows

* **Portable Executable:** Download and run `teamux-v1.0.0-windows-portable-x64.exe` (no installation required).
* **Standalone Zip:** Download `teamux-v1.0.0-windows-x64.zip`, extract anywhere, and launch `Teamux.exe`.

---

## 🛠️ Building from Source

### Prerequisites
* **Node.js** v20+ or v22+
* **npm** v10+

### 1. Clone Repository
```bash
git clone https://github.com/quietbytehq/teamux.git
cd teamux
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Run Development Build
```bash
npm start
```

### 4. Build Distribution Packages
```bash
# Build Linux packages (AppImage, deb, tar.gz)
npm run dist:linux

# Build Windows packages (portable .exe, zip)
npm run dist:win

# Build all packages simultaneously
npm run dist
```
All compiled distributions are generated in the `dist/` directory.

---

## ⚙️ Configuration & Preferences

Open Preferences with `Ctrl + ,` or from the **File > Preferences** menu:

| Option | Description | Default |
| :--- | :--- | :--- |
| **Adaptive Guardian** | Automatically throttle video bandwidth to protect voice audio quality | `true` |
| **Bandwidth Profile** | Video profile: Auto Adaptive, 720p Full HD, 480p Balanced, 360p Eco, or Audio-Only | `Auto (Adaptive)` |
| **Teams Environment** | Switch between Work/School (New Teams v2) and Personal (Teams Live) | Work/School v2 |
| **Keep running in tray** | Keep Teamux running in the system tray when window is closed | `false` |
| **Minimize to tray** | Minimize window directly to the system tray | `true` |
| **Hardware Acceleration** | GPU rasterization and video decode acceleration | `true` |
| **Unread Badges** | Display notification count badge on the tray icon and desktop dock | `true` |

---

## 🔍 Linux Wayland / PipeWire Troubleshooting

If screen sharing does not trigger on your system, verify that PipeWire and the desktop portal backend are active:

1. **Verify `xdg-desktop-portal` is installed and running:**
   ```bash
   # On Ubuntu / Debian:
   sudo apt install xdg-desktop-portal xdg-desktop-portal-gnome  # (for GNOME)
   # Or for KDE:
   sudo apt install xdg-desktop-portal-kde
   ```

2. **Verify PipeWire is running:**
   ```bash
   systemctl --user status pipewire
   ```

3. **Check Display Session:**
   ```bash
   echo $XDG_SESSION_TYPE  # Should output 'wayland' or 'x11'
   ```

---

## 🤝 Contributing

Contributions are welcome! If you encounter an issue or have a feature request:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/cool-feature`)
3. Commit your changes (`git commit -m "Add cool feature"`)
4. Push to your branch (`git push origin feature/cool-feature`)
5. Open a Pull Request

---

## 📬 Contact & Support

For questions, support, or security reports, reach out to:
* **Email:** [hello@quietbytehq.uk](mailto:hello@quietbytehq.uk)
* **Website:** [https://quietbytehq.uk](https://quietbytehq.uk)
* **GitHub Issues:** [https://github.com/quietbytehq/teamux/issues](https://github.com/quietbytehq/teamux/issues)

---

## 📄 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) and [NOTICE](NOTICE) files for details.

*Microsoft and Microsoft Teams are registered trademarks of Microsoft Corporation. Teamux is an independent open-source project and is not affiliated with, sponsored, or endorsed by Microsoft.*
