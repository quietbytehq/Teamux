# Teamux 🐧🪟

<p align="center">
  <img src="assets/icon.png" alt="Teamux Logo" width="128" height="128" />
</p>

<p align="center">
  <strong>Unofficial Microsoft Teams desktop client for Linux and Windows with Adaptive Network Guardian, Low-Hardware Mode, Studio Camera, and Hardened Isolation.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License: Apache-2.0"></a>
  <a href="#"><img src="https://img.shields.io/badge/version-v2.1.0-indigo.svg" alt="Version v2.1.0"></a>
  <a href="https://snapcraft.io/teamux"><img src="https://img.shields.io/badge/snapcraft-teamux-orange.svg" alt="Snapcraft"></a>
  <a href="#"><img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20x64-lightgrey.svg" alt="Supported Platforms"></a>
</p>

> **Disclaimer:** Teamux is an unofficial project and is not affiliated with or endorsed by Microsoft. Microsoft Teams is a trademark of Microsoft Corporation.

---

## ✨ What's New in v2.1.0

- 🪟 **Pop-Out Multitasking During Active Meetings:**
  - Clicking **Calendar**, **Chat**, **Teams**, **Activity**, or **Calls** in the left rail (or pressing `Ctrl+1..6`) while in a meeting opens that section in a **separate Teamux window** automatically — keeping your live meeting stage undisturbed.
- ☕ **Reliable Be Right Back Slate:**
  - Continuous 8 FPS animated keep-alive prevents Teams WebRTC from marking your camera as disabled after extended breaks.
- ⚡ **Low-Hardware / Potato PC Mode:**
  - **0% CPU Camera Pass-Through** when Studio effects are off, hardware-level resolution downscaling (`applyConstraints`), paused render loops in Audio-First/Away modes, and dynamic background throttling when idle.
- 🔒 **Hardened Security & Privacy Lock:**
  - Sandboxed `contextIsolation: true` preload with `contextBridge`, origin-whitelisted media/notification permissions, external URL protocol validation, and **Privacy Lock (`Ctrl + L`)** with optional 4-digit PIN.
- 🛡️ **Adaptive Network Guardian + Metered Hotspot Mode:**
  - Real-time WebRTC telemetry (RTT ping, packet loss, data saved MB counter) with dynamic 720p ➔ 480p ➔ 360p ➔ **Audio-First Mode** (0 kbps video upload) and 1-click **Metered Hotspot Mode**.
- 🎙️ **Branch Office Mic & Camera Tools:**
  - High-pass **Noise Filter (90Hz)**, **Push-to-Talk (`Ctrl+Space`)**, **Mirror Camera**, **Stepped Away Slate (`Ctrl+Shift+V`)**, **Loud Office Call Alert**, **Multi-Account Profile Switcher**, and built-in **Update Checker**.
- ✨ **Studio Camera & 7 Custom Themes:**
  - Beauty smoothing, studio lighting, vignette, tone grading, Hold-to-Compare, and 7 themes (Default, OLED Midnight, Catppuccin Mocha, Nord Frost, Tokyo Night, Dracula, Rosé Pine).

---

## 📦 Downloads & Installation (v2.1.0)

Download binaries and the **Picture-Based PDF User Guide** from [Releases](https://github.com/quietbytehq/teamux/releases) or install via Snapcraft:

### 🐧 Linux
* **Snapcraft (Ubuntu / Fedora / Debian / Arch):**
  ```bash
  sudo snap install teamux
  ```
* **Universal AppImage:**
  ```bash
  chmod +x teamux-v2.1.0-linux-x86_64.AppImage
  ./teamux-v2.1.0-linux-x86_64.AppImage
  ```
* **Ubuntu / Debian (`.deb`):** `sudo apt install ./teamux-v2.1.0-linux-amd64.deb`
* **Arch Linux (`.pacman`):** `sudo pacman -U teamux-v2.1.0-linux-x64.pacman`
* **Portable Tarball (`.tar.gz`):** `tar -xvf teamux-v2.1.0-linux-x64.tar.gz`

### 🪟 Windows
* **MSI Installer (Enterprise / Intune / GPO):** Download [`teamux-v2.1.0-windows-x64.msi`](https://github.com/quietbytehq/teamux/releases/download/v2.1.0/teamux-v2.1.0-windows-x64.msi)
* **Setup Installer (`.exe`):** Download [`teamux-v2.1.0-windows-setup-x64.exe`](https://github.com/quietbytehq/teamux/releases/download/v2.1.0/teamux-v2.1.0-windows-setup-x64.exe)
* **Portable Executable:** Download and double-click [`teamux-v2.1.0-windows-portable-x64.exe`](https://github.com/quietbytehq/teamux/releases/download/v2.1.0/teamux-v2.1.0-windows-portable-x64.exe) (no installation or admin rights required).
* **Standalone Zip:** Extract [`teamux-v2.1.0-windows-x64.zip`](https://github.com/quietbytehq/teamux/releases/download/v2.1.0/teamux-v2.1.0-windows-x64.zip) and run `Teamux.exe`.

---

## 🛠️ Building from Source
```bash
git clone https://github.com/quietbytehq/teamux.git
cd teamux
npm install
npm run dist        # Builds all Linux & Windows targets
```

## 📄 License
Licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
