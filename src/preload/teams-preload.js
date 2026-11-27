// src/preload/teams-preload.js
// Hardened, Sandboxed Preload Script (contextIsolation: true, sandbox: true)
// Exposes minimal safe bridge via contextBridge and injects page-world hooks via webFrame.

const { contextBridge, ipcRenderer, webFrame } = require('electron');

contextBridge.exposeInMainWorld('teamuxBridge', {
  sendUnreadCount: (count) => {
    if (Number.isInteger(count) && count >= 0) {
      ipcRenderer.send('unread-badge-update', count);
    }
  },
  bringAllToFront: () => ipcRenderer.send('bring-all-to-front'),
  requestShowStudio: () => ipcRenderer.send('show-studio-request'),
  setCallActive: (isActive) => ipcRenderer.send('call-state-changed', Boolean(isActive)),
  onShowStudio: (cb) => {
    if (typeof cb === 'function') ipcRenderer.on('show-studio', () => cb());
  },
  onTogglePrivacyLock: (cb) => {
    if (typeof cb === 'function') ipcRenderer.on('toggle-privacy-lock', () => cb());
  },
  onConfigUpdated: (cb) => {
    if (typeof cb === 'function') ipcRenderer.on('config-updated', (_ev, cfg) => cb(cfg));
  }
});

// Page-world hook function executed directly in the main world (bypasses CSP via webFrame)
function initTeamuxPageHook() {
  if (window.__teamuxInitialized) return;
  window.__teamuxInitialized = true;

  const isTopFrame = (() => {
    try { return window.top === window.self; } catch (_) { return false; }
  })();

  const runtimeConfig = {
    lowHardwareMode: false,
    adaptiveNetworkGuardian: true,
    bandwidthMode: 'auto',
    privacyPin: '',
    loudRingAlert: false
  };

  // -------------------------------------------------------------
  // 1. Studio Camera, Audio & Away Slate State
  // -------------------------------------------------------------
  const studioState = {
    beautyEnabled: localStorage.getItem('teamux_beauty_enabled') !== 'false',
    beautyLevel: parseInt(localStorage.getItem('teamux_beauty_level') || '65', 10),
    studioLightEnabled: localStorage.getItem('teamux_light_enabled') !== 'false',
    vignetteEnabled: localStorage.getItem('teamux_vignette_enabled') === 'true',
    mirrorCamera: localStorage.getItem('teamux_mirror_camera') === 'true',
    awaySlateActive: false,

    grayscaleEnabled: localStorage.getItem('teamux_grayscale_enabled') === 'true',
    contrast: parseInt(localStorage.getItem('teamux_contrast') || '100', 10),
    saturation: parseInt(localStorage.getItem('teamux_saturation') || '100', 10),
    shadows: parseInt(localStorage.getItem('teamux_shadows') || '0', 10),
    ambience: parseInt(localStorage.getItem('teamux_ambience') || '0', 10),

    noiseGateEnabled: localStorage.getItem('teamux_noise_gate') === 'true',
    pushToTalkEnabled: localStorage.getItem('teamux_ptt') === 'true',
    pttActive: false,

    activeTab: localStorage.getItem('teamux_active_tab') || 'retouch',
    isComparing: false,
    activeVideoStream: null
  };

  function saveStudioSettings() {
    try {
      localStorage.setItem('teamux_beauty_enabled', studioState.beautyEnabled ? 'true' : 'false');
      localStorage.setItem('teamux_beauty_level', String(studioState.beautyLevel));
      localStorage.setItem('teamux_light_enabled', studioState.studioLightEnabled ? 'true' : 'false');
      localStorage.setItem('teamux_vignette_enabled', studioState.vignetteEnabled ? 'true' : 'false');
      localStorage.setItem('teamux_mirror_camera', studioState.mirrorCamera ? 'true' : 'false');
      localStorage.setItem('teamux_grayscale_enabled', studioState.grayscaleEnabled ? 'true' : 'false');
      localStorage.setItem('teamux_contrast', String(studioState.contrast));
      localStorage.setItem('teamux_saturation', String(studioState.saturation));
      localStorage.setItem('teamux_shadows', String(studioState.shadows));
      localStorage.setItem('teamux_ambience', String(studioState.ambience));
      localStorage.setItem('teamux_noise_gate', studioState.noiseGateEnabled ? 'true' : 'false');
      localStorage.setItem('teamux_ptt', studioState.pushToTalkEnabled ? 'true' : 'false');
      localStorage.setItem('teamux_active_tab', studioState.activeTab);
    } catch (_) {}
  }

  function hasAnyStudioVisualEffect() {
    return (
      studioState.beautyEnabled ||
      studioState.studioLightEnabled ||
      studioState.vignetteEnabled ||
      studioState.mirrorCamera ||
      studioState.awaySlateActive ||
      studioState.grayscaleEnabled ||
      studioState.contrast !== 100 ||
      studioState.saturation !== 100 ||
      studioState.shadows !== 0 ||
      studioState.ambience !== 0
    );
  }

  // -------------------------------------------------------------
  // 1b. App Themes Engine (7 Built-in Themes)
  // -------------------------------------------------------------
  const THEMES = {
    default: {
      id: 'default', name: 'Teams Default', emoji: '🖥️',
      description: 'Microsoft Teams native appearance',
      swatches: ['#201f1f', '#2d2c2c', '#6264a7']
    },
    oled: {
      id: 'oled', name: 'OLED Midnight', emoji: '🌌',
      description: 'True pitch black with neon electric blue',
      swatches: ['#000000', '#121212', '#38bdf8'],
      vars: {
        bg1: '#000000', bg2: '#080808', bg3: '#121212', bg4: '#1a1a1a',
        subtle: 'rgba(255,255,255,0.04)', subtleHover: 'rgba(255,255,255,0.08)', subtlePressed: 'rgba(255,255,255,0.12)',
        brand: '#38bdf8', brandHover: '#60a5fa', brandPressed: '#0284c7', brandFg: '#38bdf8',
        fg1: '#ffffff', fg2: '#a3a3a3', fg3: '#737373', fg4: '#525252',
        stroke1: '#262626', stroke2: '#1a1a1a', strokeSubtle: '#141414', shadow: 'rgba(0,0,0,0.9)'
      }
    },
    catppuccin: {
      id: 'catppuccin', name: 'Catppuccin Mocha', emoji: '☕',
      description: 'Soothing developer pastel & mauve',
      swatches: ['#1e1e2e', '#313244', '#cba6f7'],
      vars: {
        bg1: '#1e1e2e', bg2: '#181825', bg3: '#313244', bg4: '#45475a',
        subtle: 'rgba(205,214,244,0.05)', subtleHover: 'rgba(205,214,244,0.09)', subtlePressed: 'rgba(205,214,244,0.14)',
        brand: '#cba6f7', brandHover: '#b4befe', brandPressed: '#a6e3a1', brandFg: '#cba6f7',
        fg1: '#cdd6f4', fg2: '#bac2de', fg3: '#a6adc8', fg4: '#6c7086',
        stroke1: '#313244', stroke2: '#45475a', strokeSubtle: '#26283b', shadow: 'rgba(17,17,27,0.8)'
      }
    },
    nord: {
      id: 'nord', name: 'Nord Frost', emoji: '❄️',
      description: 'Arctic slates & crisp polar cyan',
      swatches: ['#2e3440', '#3b4252', '#88c0d0'],
      vars: {
        bg1: '#2e3440', bg2: '#242933', bg3: '#3b4252', bg4: '#434c5e',
        subtle: 'rgba(236,239,244,0.05)', subtleHover: 'rgba(236,239,244,0.09)', subtlePressed: 'rgba(236,239,244,0.14)',
        brand: '#88c0d0', brandHover: '#81a1c1', brandPressed: '#5e81ac', brandFg: '#88c0d0',
        fg1: '#eceff4', fg2: '#e5e9f0', fg3: '#d8dee9', fg4: '#4c566a',
        stroke1: '#434c5e', stroke2: '#4c566a', strokeSubtle: '#3b4252', shadow: 'rgba(36,41,51,0.8)'
      }
    },
    tokyo: {
      id: 'tokyo', name: 'Tokyo Night', emoji: '🌆',
      description: 'Deep navy twilight & neon cyan/magenta',
      swatches: ['#1a1b26', '#24283b', '#7dcfff'],
      vars: {
        bg1: '#1a1b26', bg2: '#16161e', bg3: '#24283b', bg4: '#292e42',
        subtle: 'rgba(192,202,245,0.05)', subtleHover: 'rgba(192,202,245,0.09)', subtlePressed: 'rgba(192,202,245,0.14)',
        brand: '#7dcfff', brandHover: '#bb9af7', brandPressed: '#7aa2f7', brandFg: '#7dcfff',
        fg1: '#c0caf5', fg2: '#a9b1d6', fg3: '#787c99', fg4: '#565f89',
        stroke1: '#292e42', stroke2: '#3b4261', strokeSubtle: '#1f2335', shadow: 'rgba(22,22,30,0.85)'
      }
    },
    dracula: {
      id: 'dracula', name: 'Dracula', emoji: '🧛',
      description: 'Vampire dark slate & vibrant neon pink',
      swatches: ['#282a36', '#44475a', '#ff79c6'],
      vars: {
        bg1: '#282a36', bg2: '#1e1f29', bg3: '#44475a', bg4: '#6272a4',
        subtle: 'rgba(248,248,242,0.05)', subtleHover: 'rgba(248,248,242,0.09)', subtlePressed: 'rgba(248,248,242,0.14)',
        brand: '#ff79c6', brandHover: '#bd93f9', brandPressed: '#8be9fd', brandFg: '#ff79c6',
        fg1: '#f8f8f2', fg2: '#d6d6d4', fg3: '#6272a4', fg4: '#44475a',
        stroke1: '#44475a', stroke2: '#6272a4', strokeSubtle: '#282a36', shadow: 'rgba(30,31,41,0.85)'
      }
    },
    rose: {
      id: 'rose', name: 'Rosé Pine', emoji: '🌸',
      description: 'Cozy warm dusk & delicate rose gold',
      swatches: ['#191724', '#26233a', '#ebbcba'],
      vars: {
        bg1: '#191724', bg2: '#14121e', bg3: '#26233a', bg4: '#403d52',
        subtle: 'rgba(224,222,244,0.05)', subtleHover: 'rgba(224,222,244,0.09)', subtlePressed: 'rgba(224,222,244,0.14)',
        brand: '#ebbcba', brandHover: '#f6c177', brandPressed: '#31748f', brandFg: '#ebbcba',
        fg1: '#e0def4', fg2: '#908caa', fg3: '#6e6a86', fg4: '#524f67',
        stroke1: '#26233a', stroke2: '#403d52', strokeSubtle: '#1f1d2e', shadow: 'rgba(20,18,30,0.85)'
      }
    }
  };

  let currentTheme = localStorage.getItem('teamux_theme') || 'default';

  function generateThemeCSS(themeKey) {
    const theme = THEMES[themeKey];
    if (!theme || !theme.vars) return '';
    const v = theme.vars;
    return `
      :root, [data-theme], body, #root, #app, .fui-FluentProvider {
        --colorNeutralBackground1: ${v.bg1} !important; --colorNeutralBackground1Hover: ${v.bg2} !important;
        --colorNeutralBackground1Pressed: ${v.bg3} !important; --colorNeutralBackground1Selected: ${v.bg2} !important;
        --colorNeutralBackground2: ${v.bg2} !important; --colorNeutralBackground2Hover: ${v.bg3} !important;
        --colorNeutralBackground2Pressed: ${v.bg1} !important; --colorNeutralBackground2Selected: ${v.bg3} !important;
        --colorNeutralBackground3: ${v.bg3} !important; --colorNeutralBackground3Hover: ${v.bg4} !important;
        --colorNeutralBackground3Pressed: ${v.bg2} !important; --colorNeutralBackground3Selected: ${v.bg4} !important;
        --colorNeutralBackground4: ${v.bg4} !important; --colorNeutralBackground5: ${v.bg4} !important;
        --colorNeutralBackground6: ${v.bg3} !important;
        --colorNeutralBackgroundAlpha: ${v.subtle} !important; --colorNeutralBackgroundAlpha2: ${v.subtleHover} !important;
        --colorSubtleBackground: transparent !important; --colorSubtleBackgroundHover: ${v.subtleHover} !important;
        --colorSubtleBackgroundPressed: ${v.subtlePressed} !important; --colorSubtleBackgroundSelected: ${v.subtleHover} !important;
        --colorBrandBackground: ${v.brand} !important; --colorBrandBackgroundHover: ${v.brandHover} !important;
        --colorBrandBackgroundPressed: ${v.brandPressed} !important; --colorBrandBackgroundSelected: ${v.brand} !important;
        --colorBrandForeground1: ${v.brandFg} !important; --colorBrandForeground2: ${v.brandFg} !important;
        --colorBrandForegroundInverted: ${v.bg1} !important;
        --colorNeutralForeground1: ${v.fg1} !important; --colorNeutralForeground2: ${v.fg2} !important;
        --colorNeutralForeground3: ${v.fg3} !important; --colorNeutralForeground4: ${v.fg4} !important;
        --colorNeutralForegroundDisabled: ${v.fg4} !important; --colorNeutralForegroundOnBrand: #ffffff !important;
        --colorNeutralStroke1: ${v.stroke1} !important; --colorNeutralStroke2: ${v.stroke2} !important;
        --colorNeutralStrokeSubtle: ${v.strokeSubtle} !important;
      }
      html, body, #root, #app, [data-tid="app-layout"], [class*="app-layout"] { background-color: ${v.bg1} !important; color: ${v.fg1} !important; }
      header, [data-tid="app-header"], .fui-Toolbar, [class*="app-header"] { background-color: ${v.bg2} !important; border-bottom: 1px solid ${v.stroke1} !important; }
      [data-tid="app-bar"], nav[aria-label*="App bar"], [class*="app-bar"], [data-tid="app-bar-items"] { background-color: ${v.bg2} !important; border-right: 1px solid ${v.stroke1} !important; }
      [data-tid="chat-list"], [data-tid="team-list"], [data-tid="channel-list"], [class*="chat-list"] { background-color: ${v.bg2} !important; border-right: 1px solid ${v.stroke1} !important; }
      [data-tid*="chat-list-item"][aria-selected="true"], [data-tid*="chat-list-item"].active, [data-tid*="channel-list-item"][aria-selected="true"] { background-color: ${v.bg3} !important; border-left: 3px solid ${v.brand} !important; }
      [data-tid="chat-pane"], [data-tid="message-pane"], [role="main"], [data-tid="team-channel-pane"] { background-color: ${v.bg1} !important; }
      [data-tid="search-input"], [data-tid="search-box"], input[placeholder*="Search"] { background-color: ${v.bg3} !important; color: ${v.fg1} !important; border: 1px solid ${v.stroke1} !important; border-radius: 8px !important; }
      [data-tid="chat-input-control"], [data-tid="ckeditor"], [class*="chat-input"], [data-tid="ckeditor-chat-input"] { background-color: ${v.bg3} !important; border-radius: 10px !important; border: 1px solid ${v.stroke1} !important; }
      .fui-PopoverSurface, .fui-MenuPopover, .fui-DialogSurface, [role="menu"], [role="dialog"], [role="listbox"] { background-color: ${v.bg4} !important; color: ${v.fg1} !important; border: 1px solid ${v.stroke1} !important; border-radius: 10px !important; box-shadow: 0 12px 32px ${v.shadow} !important; }
      *::-webkit-scrollbar { width: 6px !important; height: 6px !important; }
      *::-webkit-scrollbar-track { background: transparent !important; }
      *::-webkit-scrollbar-thumb { background: ${v.stroke2} !important; border-radius: 6px !important; }
      *::-webkit-scrollbar-thumb:hover { background: ${v.brand} !important; }
    `;
  }

  function applyTheme(themeKey) {
    if (!THEMES[themeKey]) themeKey = 'default';
    currentTheme = themeKey;
    try { localStorage.setItem('teamux_theme', themeKey); } catch (_) {}
    let styleTag = document.getElementById('teamux-theme-styles');
    if (!styleTag) {
      styleTag = document.createElement('style');
      styleTag.id = 'teamux-theme-styles';
      const target = document.head || document.documentElement;
      if (target) target.appendChild(styleTag);
    }
    if (styleTag) styleTag.textContent = generateThemeCSS(themeKey);
  }

  try { if (isTopFrame && typeof document !== 'undefined') applyTheme(currentTheme); } catch (_) {}

  // -------------------------------------------------------------
  // 2. Stream Lifecycle Tracking & Dynamic Background Throttling
  // -------------------------------------------------------------
  const activeStreams = new Set();
  let currentCameraContext = null;
  let currentAudioContextCtrl = null;

  function registerStream(stream) {
    if (!stream) return stream;
    activeStreams.add(stream);

    stream.getTracks().forEach((track) => {
      track.addEventListener('ended', () => {
        if (stream.getTracks().every((t) => t.readyState === 'ended')) {
          activeStreams.delete(stream);
          updateActiveCallBanner();
        }
      });
    });

    updateActiveCallBanner();
    return stream;
  }

  function stopAllStreams() {
    if (currentCameraContext) {
      try { currentCameraContext.cleanup(); } catch (_) {}
      currentCameraContext = null;
    }
    if (currentAudioContextCtrl) {
      try { currentAudioContextCtrl.cleanup(); } catch (_) {}
      currentAudioContextCtrl = null;
    }
    activeStreams.forEach((stream) => {
      try {
        stream.getTracks().forEach((track) => {
          if (track.readyState !== 'ended') track.stop();
        });
      } catch (_) {}
    });
    activeStreams.clear();
    updateActiveCallBanner();
  }

  // -------------------------------------------------------------
  // 2b. Adaptive Network Guardian + Metered Hotspot & Data Saved
  // -------------------------------------------------------------
  const QUALITY_PROFILES = {
    '720p': { id: '720p', name: 'Full HD (Normal)', width: 1280, height: 720, fps: 30, maxBitrate: 2000000, badge: '720p', icon: '🚀' },
    '480p': { id: '480p', name: 'Balanced Office', width: 854, height: 480, fps: 20, maxBitrate: 500000, badge: '480p', icon: '⚖️' },
    '360p': { id: '360p', name: 'Eco Saver', width: 640, height: 360, fps: 15, maxBitrate: 250000, badge: '360p', icon: '📉' },
    'audio-only': { id: 'audio-only', name: 'Audio-First Priority', width: 480, height: 270, fps: 1, maxBitrate: 30000, badge: 'Voice Only', icon: '🔴' }
  };

  const networkState = {
    guardianEnabled: localStorage.getItem('teamux_guardian_enabled') !== 'false',
    bandwidthMode: localStorage.getItem('teamux_bandwidth_mode') || 'auto',
    meteredMode: localStorage.getItem('teamux_metered_mode') === 'true',
    currentTier: '720p',
    currentRtt: 0,
    currentLoss: 0,
    currentBitrate: 0,
    bytesSaved: 0,
    audioFirstEngaged: false,
    networkQuality: 'good',
    activePeerConnections: new Set(),
    activeSenders: new Set()
  };

  function saveNetworkSettings() {
    try {
      localStorage.setItem('teamux_guardian_enabled', networkState.guardianEnabled ? 'true' : 'false');
      localStorage.setItem('teamux_bandwidth_mode', networkState.bandwidthMode);
      localStorage.setItem('teamux_metered_mode', networkState.meteredMode ? 'true' : 'false');
    } catch (_) {}
  }

  let telemetryTimer = null;

  function startTelemetryIfNeeded() {
    if (telemetryTimer || networkState.activePeerConnections.size === 0) return;
    telemetryTimer = setInterval(pollWebRtcTelemetry, 2500);
  }

  function stopTelemetryIfIdle() {
    if (telemetryTimer && networkState.activePeerConnections.size === 0) {
      clearInterval(telemetryTimer);
      telemetryTimer = null;
    }
  }

  const OrigRTCPeerConnection = typeof RTCPeerConnection !== 'undefined' ? RTCPeerConnection : null;
  if (OrigRTCPeerConnection) {
    window.RTCPeerConnection = function (...args) {
      const pc = new OrigRTCPeerConnection(...args);
      networkState.activePeerConnections.add(pc);
      startTelemetryIfNeeded();

      pc.addEventListener('connectionstatechange', () => {
        if (pc.connectionState === 'closed' || pc.connectionState === 'failed') {
          networkState.activePeerConnections.delete(pc);
          stopTelemetryIfIdle();
        }
      });

      const origAddTrack = pc.addTrack.bind(pc);
      pc.addTrack = function (track, ...streams) {
        const sender = origAddTrack(track, ...streams);
        if (track && track.kind === 'video') {
          networkState.activeSenders.add(sender);
          applyBitrateToSender(sender, networkState.currentTier);
        }
        return sender;
      };

      return pc;
    };
    window.RTCPeerConnection.prototype = OrigRTCPeerConnection.prototype;
  }

  async function applyBitrateToSender(sender, tierKey) {
    if (!sender || typeof sender.getParameters !== 'function') return;
    const profile = QUALITY_PROFILES[tierKey] || QUALITY_PROFILES['720p'];
    try {
      const params = sender.getParameters();
      if (!params.encodings || params.encodings.length === 0) params.encodings = [{}];
      params.encodings.forEach((enc) => { enc.maxBitrate = profile.maxBitrate; });
      await sender.setParameters(params);
    } catch (_) {}
  }

  function updateAllSendersBitrate(tierKey) {
    networkState.activeSenders.forEach((sender) => applyBitrateToSender(sender, tierKey));
  }

  let consecutiveGoodTelemetry = 0;

  function evaluateAndApplyAdaptiveNetwork(rtt, lossPct, bwe) {
    if (networkState.meteredMode) {
      // Metered Hotspot Mode caps at 360p unless critical congestion demands audio-only
      if (rtt > 500 || lossPct > 15 || (bwe > 0 && bwe < 180000)) {
        networkState.networkQuality = 'critical';
        applyQualityTier('audio-only');
      } else {
        networkState.networkQuality = 'poor';
        applyQualityTier('360p');
      }
      return;
    }

    if (networkState.bandwidthMode !== 'auto') {
      applyQualityTier(networkState.bandwidthMode);
      return;
    }
    if (!networkState.guardianEnabled) {
      applyQualityTier('720p');
      return;
    }

    if (rtt > 500 || lossPct > 15 || (bwe > 0 && bwe < 180000)) {
      consecutiveGoodTelemetry = 0;
      networkState.networkQuality = 'critical';
      applyQualityTier('audio-only');
      return;
    }
    if (rtt > 260 || lossPct > 6 || (bwe > 0 && bwe < 420000)) {
      consecutiveGoodTelemetry = 0;
      networkState.networkQuality = 'poor';
      applyQualityTier('360p');
      return;
    }
    if (rtt > 130 || lossPct > 2 || (bwe > 0 && bwe < 800000)) {
      consecutiveGoodTelemetry = 0;
      networkState.networkQuality = 'moderate';
      applyQualityTier('480p');
      return;
    }

    consecutiveGoodTelemetry++;
    networkState.networkQuality = 'good';
    if (consecutiveGoodTelemetry >= 3) {
      applyQualityTier('720p');
    }
  }

  function applyQualityTier(tierKey) {
    if (!QUALITY_PROFILES[tierKey]) tierKey = '720p';
    const tierChanged = networkState.currentTier !== tierKey;
    networkState.currentTier = tierKey;
    networkState.audioFirstEngaged = (tierKey === 'audio-only');

    if (tierChanged) {
      updateAllSendersBitrate(tierKey);
      // P2: Apply hardware-level camera resolution constraints to save USB/CPU load
      if (currentCameraContext && typeof currentCameraContext.applyHardwareConstraints === 'function') {
        currentCameraContext.applyHardwareConstraints(tierKey);
      }
      // P3: Resume render loop if stepping out of paused audio-only slate
      if (currentCameraContext && typeof currentCameraContext.resumeRender === 'function') {
        currentCameraContext.resumeRender();
      }
      updateStudioPillNetworkBadge();
      updateActiveCallBanner();
      updateNetworkDashboardUI();
    }
  }

  async function pollWebRtcTelemetry() {
    if (networkState.activePeerConnections.size === 0) {
      stopTelemetryIfIdle();
      return;
    }

    let maxRtt = 0;
    let maxLoss = 0;
    let estimatedBps = 0;

    for (const pc of networkState.activePeerConnections) {
      try {
        if (pc.connectionState === 'closed') {
          networkState.activePeerConnections.delete(pc);
          continue;
        }
        const stats = await pc.getStats();
        stats.forEach((report) => {
          if (report.type === 'candidate-pair' && report.state === 'succeeded') {
            if (typeof report.currentRoundTripTime === 'number') {
              const rttMs = Math.round(report.currentRoundTripTime * 1000);
              if (rttMs > maxRtt) maxRtt = rttMs;
            }
            if (typeof report.availableOutgoingBitrate === 'number') {
              estimatedBps = report.availableOutgoingBitrate;
            }
          }
          if (report.type === 'remote-inbound-rtp' && report.kind === 'video') {
            if (typeof report.fractionLost === 'number') {
              const lossPct = Math.round(report.fractionLost * 100);
              if (lossPct > maxLoss) maxLoss = lossPct;
            }
          }
        });
      } catch (_) {}
    }

    if (networkState.activePeerConnections.size === 0) {
      stopTelemetryIfIdle();
      return;
    }

    networkState.currentRtt = maxRtt;
    networkState.currentLoss = maxLoss;
    networkState.currentBitrate = estimatedBps;

    // F1: Accumulate estimated MB saved when below 720p (2.0 Mbps)
    const activeProfile = QUALITY_PROFILES[networkState.currentTier] || QUALITY_PROFILES['720p'];
    if (activeProfile.maxBitrate < 2000000) {
      networkState.bytesSaved += ((2000000 - activeProfile.maxBitrate) / 8) * 2.5;
    }

    evaluateAndApplyAdaptiveNetwork(maxRtt, maxLoss, estimatedBps);
    updateNetworkDashboardUI();
  }

  // -------------------------------------------------------------
  // 3. Audio Noise Gate & Push-to-Talk Processor (F3)
  // -------------------------------------------------------------
  function processMicrophoneTracks(rawAudioTracks) {
    if (!rawAudioTracks || rawAudioTracks.length === 0) return rawAudioTracks;
    if (!studioState.noiseGateEnabled && !studioState.pushToTalkEnabled) {
      return rawAudioTracks;
    }

    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return rawAudioTracks;

      const audioCtx = new AudioCtx();
      const source = audioCtx.createMediaStreamSource(new MediaStream([rawAudioTracks[0]]));

      // High-pass filter removes low-frequency AC/fan/desk rumble (< 90 Hz)
      const highpass = audioCtx.createBiquadFilter();
      highpass.type = 'highpass';
      highpass.frequency.value = 90;

      // Compressor smooths loud spikes and acts as gentle office noise control
      const compressor = audioCtx.createDynamicsCompressor();
      compressor.threshold.value = -36;
      compressor.knee.value = 24;
      compressor.ratio.value = 6;

      const gainNode = audioCtx.createGain();
      gainNode.gain.value = studioState.pushToTalkEnabled ? (studioState.pttActive ? 1.0 : 0.0) : 1.0;

      const dest = audioCtx.createMediaStreamDestination();
      source.connect(highpass);
      highpass.connect(compressor);
      compressor.connect(gainNode);
      gainNode.connect(dest);

      const ctrl = {
        updateGain: () => {
          if (audioCtx.state === 'suspended') audioCtx.resume().catch(() => {});
          gainNode.gain.setTargetAtTime(
            studioState.pushToTalkEnabled ? (studioState.pttActive ? 1.0 : 0.0) : 1.0,
            audioCtx.currentTime,
            0.02
          );
        },
        cleanup: () => {
          try { source.disconnect(); } catch (_) {}
          try { audioCtx.close(); } catch (_) {}
        }
      };

      if (currentAudioContextCtrl) {
        try { currentAudioContextCtrl.cleanup(); } catch (_) {}
      }
      currentAudioContextCtrl = ctrl;

      const processedTrack = dest.stream.getAudioTracks()[0];
      processedTrack.addEventListener('ended', ctrl.cleanup);
      return [processedTrack];
    } catch (_) {
      return rawAudioTracks;
    }
  }

  // -------------------------------------------------------------
  // 4. Virtual Camera Hook (P1 Pass-Through, P2 Constraints, P3 Pause)
  // -------------------------------------------------------------
  const MediaDevicesProto = typeof MediaDevices !== 'undefined' ? MediaDevices.prototype : null;
  const origGetUserMedia = MediaDevicesProto?.getUserMedia || (typeof navigator !== 'undefined' && navigator.mediaDevices?.getUserMedia?.bind(navigator.mediaDevices));

  if (origGetUserMedia) {
    const customGetUserMedia = async function (constraints) {
      const hasVideoRequest = constraints && constraints.video;
      const hasAudioRequest = constraints && constraints.audio;

      if (!hasVideoRequest) {
        const audioStream = await origGetUserMedia.call(this || navigator.mediaDevices, constraints);
        if (hasAudioRequest && (studioState.noiseGateEnabled || studioState.pushToTalkEnabled)) {
          const processed = processMicrophoneTracks(audioStream.getAudioTracks());
          return registerStream(new MediaStream(processed));
        }
        return registerStream(audioStream);
      }

      const rawStream = await origGetUserMedia.call(this || navigator.mediaDevices, constraints);
      const rawVideoTrack = rawStream.getVideoTracks()[0];
      if (!rawVideoTrack) return registerStream(rawStream);

      const processedAudioTracks = processMicrophoneTracks(rawStream.getAudioTracks());

      // P1: Zero-Overhead Pass-Through in Low-Hardware Mode when no visual effects are active
      if (runtimeConfig.lowHardwareMode && !hasAnyStudioVisualEffect() && networkState.currentTier !== 'audio-only') {
        const profile = QUALITY_PROFILES[networkState.currentTier] || QUALITY_PROFILES['720p'];
        if (profile.id !== '720p') {
          rawVideoTrack.applyConstraints({
            width: { ideal: profile.width },
            height: { ideal: profile.height },
            frameRate: { ideal: profile.fps }
          }).catch(() => {});
        }
        const passStream = new MediaStream([rawVideoTrack, ...processedAudioTracks]);
        studioState.activeVideoStream = passStream;
        showStudioWidget();
        return registerStream(passStream);
      }

      if (currentCameraContext) {
        try { currentCameraContext.cleanup(); } catch (_) {}
      }

      const video = document.createElement('video');
      video.muted = true;
      video.playsInline = true;
      video.autoplay = true;
      video.srcObject = new MediaStream([rawVideoTrack]);
      try { await video.play(); } catch (_) {}

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d', { alpha: false, desynchronized: true });
      const initProfile = QUALITY_PROFILES[networkState.currentTier] || QUALITY_PROFILES['720p'];
      canvas.width = Math.min(initProfile.width, rawVideoTrack.getSettings()?.width || 1280);
      canvas.height = Math.min(initProfile.height, rawVideoTrack.getSettings()?.height || 720);

      let cachedVignette = null;
      let vignetteW = 0;
      let vignetteH = 0;
      let isRunning = true;
      let isFrameProcessing = false;
      let frameHandle = null;
      let lastRenderTime = 0;
      let slateDrawnMode = null;

      let slateKeepAliveTimer = null;

      const scheduleNextFrame = () => {
        if (!isRunning) return;
        if (typeof video.requestVideoFrameCallback === 'function') {
          frameHandle = video.requestVideoFrameCallback(processFrame);
        } else {
          frameHandle = requestAnimationFrame(processFrame);
        }
      };

      const scheduleSlateKeepAlive = () => {
        if (!isRunning || slateKeepAliveTimer !== null) return;
        // 4 FPS gentle keep-alive prevents Teams WebRTC from marking the camera as disabled/starved
        slateKeepAliveTimer = setTimeout(() => {
          slateKeepAliveTimer = null;
          if (isRunning) processFrame();
        }, 250);
      };

      const cleanup = () => {
        if (!isRunning) return;
        isRunning = false;
        if (slateKeepAliveTimer !== null) {
          clearTimeout(slateKeepAliveTimer);
          slateKeepAliveTimer = null;
        }
        if (frameHandle !== null) {
          if (typeof video.cancelVideoFrameCallback === 'function') {
            try { video.cancelVideoFrameCallback(frameHandle); } catch (_) {}
          } else {
            try { cancelAnimationFrame(frameHandle); } catch (_) {}
          }
          frameHandle = null;
        }
        rawStream.getTracks().forEach((t) => { try { t.stop(); } catch (_) {} });
        video.srcObject = null;
        if (currentCameraContext === cameraCtx) currentCameraContext = null;
      };

      const cameraCtx = {
        cleanup,
        applyHardwareConstraints: (tierKey) => {
          const prof = QUALITY_PROFILES[tierKey] || QUALITY_PROFILES['720p'];
          if (rawVideoTrack.readyState === 'live' && prof.id !== 'audio-only') {
            rawVideoTrack.applyConstraints({
              width: { ideal: prof.width },
              height: { ideal: prof.height },
              frameRate: { ideal: prof.fps }
            }).catch(() => {});
          }
        },
        resumeRender: () => {
          if (!isRunning) return;
          if (slateKeepAliveTimer !== null) {
            clearTimeout(slateKeepAliveTimer);
            slateKeepAliveTimer = null;
          }
          if (frameHandle === null) {
            scheduleNextFrame();
          }
        }
      };
      currentCameraContext = cameraCtx;

      const drawAudioFirstSlate = () => {
        const w = canvas.width;
        const h = canvas.height;
        ctx.filter = 'none';
        ctx.globalAlpha = 1.0;
        ctx.globalCompositeOperation = 'source-over';
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, w, h);

        ctx.fillStyle = '#ef4444';
        ctx.font = 'bold 22px "Segoe UI", system-ui, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('🔴 Audio-First Mode Active', w / 2, h / 2 - 20);

        ctx.fillStyle = '#94a3b8';
        ctx.font = '14px "Segoe UI", system-ui, sans-serif';
        ctx.fillText('Video upload paused to protect voice audio quality.', w / 2, h / 2 + 14);
        ctx.fillText('Resuming automatically when network clears.', w / 2, h / 2 + 36);
      };

      const drawBeRightBackSlate = () => {
        const w = canvas.width;
        const h = canvas.height;
        const t = performance.now() / 1000;
        ctx.filter = 'none';
        ctx.globalAlpha = 1.0;
        ctx.globalCompositeOperation = 'source-over';

        // Rich multi-stop dark cosmic gradient background
        const bgGrad = ctx.createLinearGradient(0, 0, w, h);
        bgGrad.addColorStop(0, '#090d1f');
        bgGrad.addColorStop(0.5, '#1e1b4b');
        bgGrad.addColorStop(1, '#311042');
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, w, h);

        // Soft colorful glowing ambient orbs
        const orb1 = ctx.createRadialGradient(w * 0.2, h * 0.25, 10, w * 0.2, h * 0.25, w * 0.35);
        orb1.addColorStop(0, 'rgba(56, 189, 248, 0.26)');
        orb1.addColorStop(1, 'rgba(56, 189, 248, 0)');
        ctx.fillStyle = orb1;
        ctx.fillRect(0, 0, w, h);

        const orb2 = ctx.createRadialGradient(w * 0.82, h * 0.78, 10, w * 0.82, h * 0.78, w * 0.38);
        orb2.addColorStop(0, 'rgba(236, 72, 153, 0.26)');
        orb2.addColorStop(1, 'rgba(236, 72, 153, 0)');
        ctx.fillStyle = orb2;
        ctx.fillRect(0, 0, w, h);

        // Center frosted card with colorful gradient border
        const cardW = Math.min(w * 0.82, 540);
        const cardH = Math.min(h * 0.68, 250);
        const cardX = (w - cardW) / 2;
        const cardY = (h - cardH) / 2;
        const radius = 20;

        ctx.fillStyle = 'rgba(15, 23, 42, 0.78)';
        ctx.beginPath();
        if (typeof ctx.roundRect === 'function') ctx.roundRect(cardX, cardY, cardW, cardH, radius);
        else ctx.rect(cardX, cardY, cardW, cardH);
        ctx.fill();

        const borderGrad = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY + cardH);
        borderGrad.addColorStop(0, '#38bdf8');
        borderGrad.addColorStop(0.35, '#a855f7');
        borderGrad.addColorStop(0.7, '#ec4899');
        borderGrad.addColorStop(1, '#fbbf24');
        ctx.lineWidth = 3;
        ctx.strokeStyle = borderGrad;
        ctx.stroke();

        // Top pill badge
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.font = 'bold 13px "Segoe UI", system-ui, sans-serif';
        ctx.fillStyle = '#fbbf24';
        ctx.fillText('☕  STEPPED AWAY FOR A MOMENT', w / 2, cardY + cardH * 0.22);

        // Fancy colorful gradient main heading: "Be Right Back!"
        const titleSize = Math.max(28, Math.min(46, Math.round(w * 0.06)));
        ctx.font = `800 ${titleSize}px "Segoe UI", system-ui, sans-serif`;
        const textGrad = ctx.createLinearGradient(w * 0.25, 0, w * 0.75, 0);
        textGrad.addColorStop(0, '#38bdf8');
        textGrad.addColorStop(0.35, '#c084fc');
        textGrad.addColorStop(0.7, '#f472b6');
        textGrad.addColorStop(1, '#fbbf24');
        ctx.fillStyle = textGrad;
        ctx.fillText('Be Right Back!', w / 2, cardY + cardH * 0.46);

        // Clean subtitle
        ctx.font = '500 15px "Segoe UI", system-ui, sans-serif';
        ctx.fillStyle = '#e2e8f0';
        ctx.fillText("I'll be back in the meeting shortly — thank you!", w / 2, cardY + cardH * 0.67);

        // Animated pulsing dots + audio connected status
        const activeDot = Math.floor(t * 2.5) % 3;
        const dotColors = ['#38bdf8', '#c084fc', '#f472b6'];
        for (let i = 0; i < 3; i++) {
          ctx.beginPath();
          ctx.arc(w / 2 - 18 + i * 18, cardY + cardH * 0.84, i === activeDot ? 5.5 : 3.5, 0, Math.PI * 2);
          ctx.fillStyle = i === activeDot ? dotColors[i] : 'rgba(148, 163, 184, 0.45)';
          ctx.fill();
        }
      };

      const processFrame = () => {
        frameHandle = null;
        if (!isRunning) return;

        // Keep-alive 4 FPS frames during Audio-First or Be Right Back so Teams never flags camera as disabled
        if (networkState.currentTier === 'audio-only') {
          drawAudioFirstSlate();
          scheduleSlateKeepAlive();
          return;
        }
        if (studioState.awaySlateActive) {
          drawBeRightBackSlate();
          scheduleSlateKeepAlive();
          return;
        }

        scheduleNextFrame();

        const profile = QUALITY_PROFILES[networkState.currentTier] || QUALITY_PROFILES['720p'];
        const now = performance.now();
        const minInterval = 1000 / (profile.fps || 30);
        if (now - lastRenderTime < minInterval - 3) return;

        if (isFrameProcessing || video.readyState < 2 || !rawVideoTrack.enabled || rawVideoTrack.readyState === 'ended') {
          return;
        }

        isFrameProcessing = true;
        lastRenderTime = now;
        try {
          const targetW = Math.min(profile.width, video.videoWidth || 1280);
          const targetH = Math.min(profile.height, video.videoHeight || 720);
          if (canvas.width !== targetW || canvas.height !== targetH) {
            canvas.width = targetW;
            canvas.height = targetH;
            cachedVignette = null;
          }

          const hasTone = studioState.grayscaleEnabled || studioState.contrast !== 100 ||
                          studioState.saturation !== 100 || studioState.shadows !== 0 || studioState.ambience !== 0;
          const isProcessingActive = (studioState.beautyEnabled || hasTone || studioState.studioLightEnabled || studioState.vignetteEnabled) && !studioState.isComparing;

          ctx.save();
          if (studioState.mirrorCamera && !studioState.isComparing) {
            ctx.translate(canvas.width, 0);
            ctx.scale(-1, 1);
          }

          if (isProcessingActive) {
            let cVal = studioState.contrast;
            let sVal = studioState.saturation;
            let bVal = 100;
            if (studioState.studioLightEnabled) { bVal += 6; cVal = Math.round(cVal * 1.03); sVal = Math.round(sVal * 1.04); }
            if (studioState.shadows !== 0) { bVal += Math.round(studioState.shadows * 0.30); cVal = Math.round(cVal * (1 - studioState.shadows * 0.0018)); }
            if (studioState.ambience > 0) { bVal += Math.round(studioState.ambience * 0.07); }

            const filterParts = [];
            if (bVal !== 100) filterParts.push(`brightness(${bVal}%)`);
            if (cVal !== 100) filterParts.push(`contrast(${cVal}%)`);
            if (studioState.grayscaleEnabled) {
              filterParts.push('grayscale(100%)');
            } else {
              if (sVal !== 100) filterParts.push(`saturate(${sVal}%)`);
              if (studioState.ambience > 0) {
                const sepiaPct = Math.round((studioState.ambience / 100) * 16);
                if (sepiaPct > 0) filterParts.push(`sepia(${sepiaPct}%)`);
              }
            }

            ctx.filter = filterParts.length > 0 ? filterParts.join(' ') : 'none';
            ctx.globalAlpha = 1.0;
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            if (studioState.beautyEnabled && !runtimeConfig.lowHardwareMode) {
              const levelNorm = studioState.beautyLevel / 100;
              const blurRadius = Math.max(2, Math.round(levelNorm * 6));
              const overlayAlpha = Math.min(0.50, 0.15 + (levelNorm * 0.35));
              ctx.filter = `blur(${blurRadius}px)`;
              ctx.globalAlpha = overlayAlpha;
              ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            }

            ctx.restore();
            ctx.save();

            if (studioState.shadows > 10 && !studioState.grayscaleEnabled) {
              ctx.filter = 'none';
              ctx.globalCompositeOperation = 'screen';
              ctx.fillStyle = `rgba(180, 195, 215, ${(studioState.shadows / 100) * 0.14})`;
              ctx.fillRect(0, 0, canvas.width, canvas.height);
              ctx.globalCompositeOperation = 'source-over';
            }

            if (studioState.ambience > 20 && !studioState.grayscaleEnabled) {
              ctx.filter = 'none';
              ctx.globalCompositeOperation = 'soft-light';
              ctx.fillStyle = `rgba(255, 232, 204, ${(studioState.ambience / 100) * 0.22})`;
              ctx.fillRect(0, 0, canvas.width, canvas.height);
              ctx.globalCompositeOperation = 'source-over';
            }

            if (studioState.vignetteEnabled) {
              ctx.filter = 'none';
              ctx.globalCompositeOperation = 'source-over';
              if (!cachedVignette || vignetteW !== canvas.width || vignetteH !== canvas.height) {
                vignetteW = canvas.width;
                vignetteH = canvas.height;
                cachedVignette = ctx.createRadialGradient(
                  vignetteW / 2, vignetteH / 2, Math.min(vignetteW, vignetteH) * 0.35,
                  vignetteW / 2, vignetteH / 2, Math.max(vignetteW, vignetteH) * 0.75
                );
                cachedVignette.addColorStop(0, 'rgba(0,0,0,0)');
                cachedVignette.addColorStop(1, 'rgba(0,0,0,0.50)');
              }
              ctx.fillStyle = cachedVignette;
              ctx.fillRect(0, 0, canvas.width, canvas.height);
            }
          } else {
            ctx.filter = 'none';
            ctx.globalAlpha = 1.0;
            ctx.globalCompositeOperation = 'source-over';
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            if (studioState.isComparing) {
              ctx.restore();
              ctx.save();
              ctx.fillStyle = 'rgba(0, 0, 0, 0.65)';
              ctx.fillRect(16, 16, 170, 36);
              ctx.font = 'bold 14px sans-serif';
              ctx.fillStyle = '#38bdf8';
              ctx.fillText('👁️ RAW ORIGINAL', 32, 40);
            }
          }
          ctx.restore();
        } catch (_) {
          try {
            ctx.filter = 'none';
            ctx.globalAlpha = 1.0;
            ctx.globalCompositeOperation = 'source-over';
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          } catch (_) {}
        } finally {
          isFrameProcessing = false;
        }
      };

      scheduleNextFrame();

      const virtualStream = canvas.captureStream(initProfile.fps || 30);
      const virtualVideoTrack = virtualStream.getVideoTracks()[0];
      const origTrackStop = virtualVideoTrack.stop.bind(virtualVideoTrack);
      virtualVideoTrack.stop = () => {
        cleanup();
        origTrackStop();
      };
      virtualVideoTrack.addEventListener('ended', cleanup);

      const outputStream = new MediaStream([virtualVideoTrack, ...processedAudioTracks]);
      studioState.activeVideoStream = outputStream;
      showStudioWidget();
      return registerStream(outputStream);
    };

    if (MediaDevicesProto) MediaDevicesProto.getUserMedia = customGetUserMedia;
    if (typeof navigator !== 'undefined' && navigator.mediaDevices) navigator.mediaDevices.getUserMedia = customGetUserMedia;
  }

  const origGetDisplayMedia = MediaDevicesProto?.getDisplayMedia || (typeof navigator !== 'undefined' && navigator.mediaDevices?.getDisplayMedia?.bind(navigator.mediaDevices));
  if (origGetDisplayMedia) {
    const customGetDisplayMedia = async function (...args) {
      const stream = await origGetDisplayMedia.apply(this || navigator.mediaDevices, args);
      return registerStream(stream);
    };
    if (MediaDevicesProto) MediaDevicesProto.getDisplayMedia = customGetDisplayMedia;
    if (typeof navigator !== 'undefined' && navigator.mediaDevices) navigator.mediaDevices.getDisplayMedia = customGetDisplayMedia;
  }

  // -------------------------------------------------------------
  // 5. In-Meeting Floating Studio UI, Privacy Lock (S5) & Loud Ringtone (F6)
  // -------------------------------------------------------------
  function injectStudioUI() {
    if (document.getElementById('teamux-studio-widget')) return;

    const style = document.createElement('style');
    style.id = 'teamux-studio-styles';
    style.textContent = `
      #teamux-studio-widget { position:fixed!important; bottom:24px!important; right:24px!important; z-index:2147483647!important; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; user-select:none; }
      .teamux-studio-card { display:none; background:rgba(24,24,28,0.96); backdrop-filter:blur(16px); border:1px solid rgba(99,102,241,0.45); border-radius:12px; width:330px; box-shadow:0 12px 32px rgba(0,0,0,0.65); color:#f4f4f5; overflow:hidden; flex-direction:column; }
      .teamux-studio-header { padding:10px 14px; background:rgba(36,36,42,0.95); border-bottom:1px solid rgba(63,63,70,0.5); display:flex; align-items:center; justify-content:space-between; }
      .teamux-studio-title { font-size:13px; font-weight:600; display:flex; align-items:center; gap:6px; color:#c7d2fe; }
      .teamux-studio-btn-min { background:none; border:none; color:#a1a1aa; cursor:pointer; font-size:16px; padding:2px 6px; border-radius:4px; }
      .teamux-studio-btn-min:hover { background:rgba(255,255,255,0.1); color:white; }
      .teamux-studio-tabs { display:flex; background:rgba(30,30,36,0.85); border-bottom:1px solid rgba(63,63,70,0.5); }
      .teamux-studio-tab { flex:1; padding:8px 5px; font-size:11px; font-weight:600; text-align:center; background:transparent; border:none; color:#a1a1aa; cursor:pointer; border-bottom:2px solid transparent; white-space:nowrap; }
      .teamux-studio-tab.active { color:#818cf8; border-bottom-color:#6366f1; background:rgba(99,102,241,0.08); }
      .teamux-studio-body { padding:12px 14px; display:flex; flex-direction:column; gap:10px; max-height:460px; overflow-y:auto; }
      .teamux-tab-pane { display:flex; flex-direction:column; gap:9px; }
      .teamux-tab-pane.hidden { display:none; }
      .teamux-toggle-row { display:flex; align-items:center; justify-content:space-between; font-size:12.5px; }
      .teamux-switch { position:relative; display:inline-block; width:40px; height:21px; flex-shrink:0; }
      .teamux-switch input { opacity:0; width:0; height:0; }
      .teamux-slider { position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background-color:#3f3f46; transition:.2s; border-radius:21px; }
      .teamux-slider:before { position:absolute; content:""; height:15px; width:15px; left:3px; bottom:3px; background-color:white; transition:.2s; border-radius:50%; }
      input:checked + .teamux-slider { background-color:#6366f1; }
      input:checked + .teamux-slider:before { transform:translateX(19px); }
      .teamux-range-group { display:flex; flex-direction:column; gap:4px; }
      .teamux-range-label { font-size:12px; color:#a1a1aa; display:flex; justify-content:space-between; }
      .teamux-range-input { width:100%; height:5px; border-radius:5px; background:#3f3f46; accent-color:#6366f1; cursor:pointer; }
      .teamux-btn-compare { background:#27272a; border:1px solid #3f3f46; color:#e4e4e7; padding:7px 12px; border-radius:6px; font-size:12px; font-weight:500; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; }
      .teamux-btn-compare.active { background:#4338ca; border-color:#6366f1; color:white; }
      .teamux-btn-reset { background:#1f1f23; border:1px solid #3f3f46; color:#a1a1aa; padding:6px 12px; border-radius:6px; font-size:11px; cursor:pointer; text-align:center; }
      .teamux-divider { border-top:1px solid rgba(63,63,70,0.5); margin:2px 0; padding-top:7px; font-size:11px; font-weight:600; color:#818cf8; }
      .teamux-theme-list { display:flex; flex-direction:column; gap:6px; max-height:270px; overflow-y:auto; padding-right:4px; }
      .teamux-theme-card { display:flex; align-items:center; justify-content:space-between; padding:7px 10px; background:rgba(36,36,42,0.7); border:1px solid rgba(63,63,70,0.5); border-radius:8px; cursor:pointer; }
      .teamux-theme-card.active { background:rgba(99,102,241,0.18); border-color:#818cf8; }
      .teamux-theme-card-title { font-size:12px; font-weight:600; color:#f4f4f5; display:flex; align-items:center; gap:5px; }
      .teamux-theme-card-desc { font-size:10px; color:#a1a1aa; }
      .teamux-theme-swatches { display:flex; gap:4px; }
      .teamux-swatch-dot { width:12px; height:12px; border-radius:50%; border:1px solid rgba(255,255,255,0.25); }
      .teamux-theme-badge { font-size:9px; font-weight:700; padding:1px 5px; border-radius:10px; background:#4f46e5; color:#fff; margin-left:3px; }
      .teamux-studio-pill { display:flex; background:rgba(30,27,75,0.94); border:1px solid #818cf8; color:#fff; padding:8px 14px; border-radius:24px; align-items:center; gap:6px; cursor:pointer; box-shadow:0 4px 16px rgba(0,0,0,0.5); font-size:13px; font-weight:600; }
      .teamux-hint-box { font-size:11px; color:#94a3b8; background:rgba(30,41,59,0.5); border:1px solid rgba(51,65,85,0.6); border-radius:6px; padding:6px 8px; line-height:1.35; }
      .teamux-select { width:100%; background:#24242a; border:1px solid #3f3f46; color:#f4f4f5; padding:6px 10px; border-radius:6px; font-size:12px; cursor:pointer; }
      .teamux-network-dashboard { background:rgba(24,24,27,0.75); border:1px solid rgba(63,63,70,0.5); border-radius:8px; padding:9px; display:flex; flex-direction:column; gap:7px; }
      .teamux-net-grid { display:grid; grid-template-columns:1fr 1fr; gap:6px; }
      .teamux-net-stat { background:rgba(39,39,42,0.6); padding:5px 8px; border-radius:6px; border:1px solid rgba(63,63,70,0.35); }
      .teamux-net-label { font-size:10px; color:#a1a1aa; }
      .teamux-net-val { font-size:12.5px; font-weight:600; color:#f4f4f5; }
      .teamux-status-badge { font-size:10px; font-weight:700; padding:2px 7px; border-radius:10px; color:white; }
      .teamux-status-good { background:#16a34a; } .teamux-status-moderate { background:#d97706; } .teamux-status-poor { background:#ea580c; } .teamux-status-critical { background:#dc2626; }
      .teamux-pill-net-badge { font-size:10px; font-weight:700; padding:1px 6px; border-radius:8px; background:rgba(255,255,255,0.15); color:#e0e7ff; }
      #teamux-call-banner { display:none; position:fixed!important; top:14px!important; left:50%!important; transform:translateX(-50%)!important; z-index:2147483646!important; background:rgba(15,23,42,0.94); border:1px solid #22c55e; box-shadow:0 8px 24px rgba(0,0,0,0.5); border-radius:30px; padding:8px 18px; color:white; font-size:13px; font-weight:500; align-items:center; gap:12px; cursor:pointer; }
      #teamux-privacy-lock { display:none; position:fixed!important; inset:0!important; z-index:2147483647!important; background:rgba(9,9,11,0.82); backdrop-filter:blur(26px); align-items:center; justify-content:center; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }
      .teamux-lock-card { background:#18181b; border:1px solid #3f3f46; border-radius:16px; padding:28px 32px; text-align:center; color:#f4f4f5; box-shadow:0 20px 50px rgba(0,0,0,0.8); width:320px; }
      .teamux-lock-input { width:140px; text-align:center; font-size:20px; letter-spacing:8px; padding:8px; border-radius:8px; border:1px solid #52525b; background:#27272a; color:white; margin:12px auto; display:block; }
      .teamux-lock-btn { background:#4f46e5; color:white; border:none; padding:9px 22px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer; margin-top:8px; }
    `;
    document.head.appendChild(style);

    function createToggleRow(labelText, switchId, isChecked) {
      const row = document.createElement('div');
      row.className = 'teamux-toggle-row';
      const span = document.createElement('span');
      span.textContent = labelText;
      const label = document.createElement('label');
      label.className = 'teamux-switch';
      const input = document.createElement('input');
      input.type = 'checkbox';
      input.id = switchId;
      input.checked = !!isChecked;
      const slider = document.createElement('span');
      slider.className = 'teamux-slider';
      label.appendChild(input);
      label.appendChild(slider);
      row.appendChild(span);
      row.appendChild(label);
      return row;
    }

    function createRangeGroup(labelText, inputId, valId, min, max, val, unit) {
      const group = document.createElement('div');
      group.className = 'teamux-range-group';
      group.id = `${inputId}-group`;
      const labelRow = document.createElement('div');
      labelRow.className = 'teamux-range-label';
      const nameSpan = document.createElement('span');
      nameSpan.textContent = labelText;
      const valSpan = document.createElement('span');
      valSpan.id = valId;
      valSpan.textContent = `${unit === '+/-' && val > 0 ? '+' : ''}${val}${unit === '+/-' ? '' : unit}`;
      labelRow.appendChild(nameSpan);
      labelRow.appendChild(valSpan);
      const rangeInput = document.createElement('input');
      rangeInput.type = 'range';
      rangeInput.id = inputId;
      rangeInput.className = 'teamux-range-input';
      rangeInput.min = String(min);
      rangeInput.max = String(max);
      rangeInput.value = String(val);
      group.appendChild(labelRow);
      group.appendChild(rangeInput);
      return { group, rangeInput, valSpan };
    }

    const container = document.createElement('div');
    container.id = 'teamux-studio-widget';

    const card = document.createElement('div');
    card.id = 'teamux-studio-card';
    card.className = 'teamux-studio-card';

    const header = document.createElement('div');
    header.className = 'teamux-studio-header';
    const title = document.createElement('div');
    title.className = 'teamux-studio-title';
    title.textContent = '✨ Teamux Studio';
    const minBtn = document.createElement('button');
    minBtn.className = 'teamux-studio-btn-min';
    minBtn.type = 'button';
    minBtn.textContent = '−';
    header.appendChild(title);
    header.appendChild(minBtn);
    card.appendChild(header);

    const tabsBar = document.createElement('div');
    tabsBar.className = 'teamux-studio-tabs';
    const tabRetouch = document.createElement('button');
    tabRetouch.className = `teamux-studio-tab ${studioState.activeTab === 'retouch' ? 'active' : ''}`;
    tabRetouch.type = 'button';
    tabRetouch.textContent = '✨ Retouch';
    const tabTone = document.createElement('button');
    tabTone.className = `teamux-studio-tab ${studioState.activeTab === 'tone' ? 'active' : ''}`;
    tabTone.type = 'button';
    tabTone.textContent = '🎨 Tone';
    const tabThemes = document.createElement('button');
    tabThemes.className = `teamux-studio-tab ${studioState.activeTab === 'themes' ? 'active' : ''}`;
    tabThemes.type = 'button';
    tabThemes.textContent = '🎭 Themes';
    const tabNetwork = document.createElement('button');
    tabNetwork.className = `teamux-studio-tab ${studioState.activeTab === 'network' ? 'active' : ''}`;
    tabNetwork.type = 'button';
    tabNetwork.textContent = '🌐 Network';
    tabsBar.appendChild(tabRetouch);
    tabsBar.appendChild(tabTone);
    tabsBar.appendChild(tabThemes);
    tabsBar.appendChild(tabNetwork);
    card.appendChild(tabsBar);

    const body = document.createElement('div');
    body.className = 'teamux-studio-body';

    // --- PANE 1: RETOUCH & MIC ---
    const paneRetouch = document.createElement('div');
    paneRetouch.className = `teamux-tab-pane ${studioState.activeTab === 'retouch' ? '' : 'hidden'}`;
    paneRetouch.appendChild(createToggleRow('Beauty Filter', 'teamux-toggle-beauty', studioState.beautyEnabled));
    const smoothGroup = createRangeGroup('Smoothness', 'teamux-range-level', 'teamux-level-val', 10, 100, studioState.beautyLevel, '%');
    if (!studioState.beautyEnabled) { smoothGroup.group.style.opacity = '0.4'; smoothGroup.group.style.pointerEvents = 'none'; }
    paneRetouch.appendChild(smoothGroup.group);
    paneRetouch.appendChild(createToggleRow('Studio Lighting', 'teamux-toggle-light', studioState.studioLightEnabled));
    paneRetouch.appendChild(createToggleRow('Portrait Focus (Vignette)', 'teamux-toggle-vignette', studioState.vignetteEnabled));
    paneRetouch.appendChild(createToggleRow('Mirror Camera (Flip)', 'teamux-toggle-mirror', studioState.mirrorCamera));
    paneRetouch.appendChild(createToggleRow('Be Right Back Screen (Ctrl+Shift+V)', 'teamux-toggle-away', studioState.awaySlateActive));

    const micDivider = document.createElement('div');
    micDivider.className = 'teamux-divider';
    micDivider.textContent = '🎙️ Branch Office Mic Controls';
    paneRetouch.appendChild(micDivider);
    paneRetouch.appendChild(createToggleRow('Noise Filter (High-Pass 90Hz)', 'teamux-toggle-noisegate', studioState.noiseGateEnabled));
    paneRetouch.appendChild(createToggleRow('Push-to-Talk (Hold Ctrl+Space)', 'teamux-toggle-ptt', studioState.pushToTalkEnabled));
    body.appendChild(paneRetouch);

    // --- PANE 2: TONE ---
    const paneTone = document.createElement('div');
    paneTone.className = `teamux-tab-pane ${studioState.activeTab === 'tone' ? '' : 'hidden'}`;
    paneTone.appendChild(createToggleRow('Grayscale (Black & White)', 'teamux-toggle-grayscale', studioState.grayscaleEnabled));
    const contrastGroup = createRangeGroup('Contrast', 'teamux-range-contrast', 'teamux-contrast-val', 50, 150, studioState.contrast, '%');
    paneTone.appendChild(contrastGroup.group);
    const satGroup = createRangeGroup('Saturation', 'teamux-range-sat', 'teamux-sat-val', 0, 200, studioState.saturation, '%');
    if (studioState.grayscaleEnabled) { satGroup.group.style.opacity = '0.4'; satGroup.group.style.pointerEvents = 'none'; }
    paneTone.appendChild(satGroup.group);
    const shadowsGroup = createRangeGroup('Shadow Lift', 'teamux-range-shadows', 'teamux-shadows-val', -50, 50, studioState.shadows, '+/-');
    paneTone.appendChild(shadowsGroup.group);
    const ambienceGroup = createRangeGroup('Ambience (Warm Glow)', 'teamux-range-ambience', 'teamux-ambience-val', 0, 100, studioState.ambience, '%');
    paneTone.appendChild(ambienceGroup.group);
    const btnResetTone = document.createElement('button');
    btnResetTone.className = 'teamux-btn-reset';
    btnResetTone.type = 'button';
    btnResetTone.textContent = '↺ Reset Tone Adjustments';
    paneTone.appendChild(btnResetTone);
    body.appendChild(paneTone);

    // --- PANE 3: THEMES ---
    const paneThemes = document.createElement('div');
    paneThemes.className = `teamux-tab-pane ${studioState.activeTab === 'themes' ? '' : 'hidden'}`;
    const themeList = document.createElement('div');
    themeList.className = 'teamux-theme-list';
    const themeCards = [];

    function refreshThemeSelection(selectedKey) {
      applyTheme(selectedKey);
      themeCards.forEach(({ key, card: tc, titleRow, badge }) => {
        if (key === selectedKey) {
          tc.classList.add('active');
          if (!titleRow.contains(badge)) titleRow.appendChild(badge);
        } else {
          tc.classList.remove('active');
          if (titleRow.contains(badge)) titleRow.removeChild(badge);
        }
      });
    }

    Object.keys(THEMES).forEach((key) => {
      const t = THEMES[key];
      const isAct = currentTheme === key;
      const tCard = document.createElement('div');
      tCard.className = `teamux-theme-card ${isAct ? 'active' : ''}`;
      const tInfo = document.createElement('div');
      const tTitleRow = document.createElement('div');
      tTitleRow.className = 'teamux-theme-card-title';
      tTitleRow.textContent = `${t.emoji} ${t.name}`;
      const tBadge = document.createElement('span');
      tBadge.className = 'teamux-theme-badge';
      tBadge.textContent = 'Active';
      if (isAct) tTitleRow.appendChild(tBadge);
      const tDesc = document.createElement('div');
      tDesc.className = 'teamux-theme-card-desc';
      tDesc.textContent = t.description;
      tInfo.appendChild(tTitleRow);
      tInfo.appendChild(tDesc);
      const tSwatches = document.createElement('div');
      tSwatches.className = 'teamux-theme-swatches';
      t.swatches.forEach((c) => {
        const dot = document.createElement('span');
        dot.className = 'teamux-swatch-dot';
        dot.style.backgroundColor = c;
        tSwatches.appendChild(dot);
      });
      tCard.appendChild(tInfo);
      tCard.appendChild(tSwatches);
      tCard.addEventListener('click', () => refreshThemeSelection(key));
      themeCards.push({ key, card: tCard, titleRow: tTitleRow, badge: tBadge });
      themeList.appendChild(tCard);
    });
    paneThemes.appendChild(themeList);
    body.appendChild(paneThemes);

    // --- PANE 4: NETWORK & METERED SAVER ---
    const paneNetwork = document.createElement('div');
    paneNetwork.className = `teamux-tab-pane ${studioState.activeTab === 'network' ? '' : 'hidden'}`;
    paneNetwork.appendChild(createToggleRow('Adaptive Guardian', 'teamux-toggle-guardian', networkState.guardianEnabled));
    paneNetwork.appendChild(createToggleRow('Metered Hotspot Mode (Cap 360p)', 'teamux-toggle-metered', networkState.meteredMode));

    const modeGroup = document.createElement('div');
    modeGroup.className = 'teamux-range-group';
    const modeLabel = document.createElement('div');
    modeLabel.className = 'teamux-range-label';
    modeLabel.textContent = 'Bandwidth Profile';
    const modeSelect = document.createElement('select');
    modeSelect.id = 'teamux-select-bandwidth';
    modeSelect.className = 'teamux-select';
    [
      { value: 'auto', label: 'Auto (Dynamic Guardian)' },
      { value: '720p', label: '720p Full HD (~2.0 Mbps)' },
      { value: '480p', label: '480p Balanced (~500 kbps)' },
      { value: '360p', label: '360p Eco Saver (~250 kbps)' },
      { value: 'audio-only', label: 'Audio-First Priority (~30 kbps)' }
    ].forEach((opt) => {
      const el = document.createElement('option');
      el.value = opt.value;
      el.textContent = opt.label;
      if (networkState.bandwidthMode === opt.value) el.selected = true;
      modeSelect.appendChild(el);
    });
    modeGroup.appendChild(modeLabel);
    modeGroup.appendChild(modeSelect);
    paneNetwork.appendChild(modeGroup);

    const dashboard = document.createElement('div');
    dashboard.className = 'teamux-network-dashboard';
    const dashTitle = document.createElement('div');
    dashTitle.style.cssText = 'font-size:11px; font-weight:600; color:#cbd5e1; display:flex; justify-content:space-between; align-items:center;';
    const dashTitleSpan = document.createElement('span');
    dashTitleSpan.textContent = 'Live WebRTC Telemetry';
    const dashStatusBadge = document.createElement('span');
    dashStatusBadge.id = 'teamux-net-badge-status';
    dashStatusBadge.className = 'teamux-status-badge teamux-status-good';
    dashStatusBadge.textContent = 'Optimal';
    dashTitle.appendChild(dashTitleSpan);
    dashTitle.appendChild(dashStatusBadge);

    const grid = document.createElement('div');
    grid.className = 'teamux-net-grid';
    const makeStat = (lbl, id, initVal) => {
      const box = document.createElement('div');
      box.className = 'teamux-net-stat';
      const l = document.createElement('div');
      l.className = 'teamux-net-label';
      l.textContent = lbl;
      const v = document.createElement('div');
      v.id = id;
      v.className = 'teamux-net-val';
      v.textContent = initVal;
      box.appendChild(l);
      box.appendChild(v);
      return box;
    };
    grid.appendChild(makeStat('Latency (RTT)', 'teamux-net-rtt', '0 ms'));
    grid.appendChild(makeStat('Packet Loss', 'teamux-net-loss', '0%'));
    grid.appendChild(makeStat('Active Stream', 'teamux-net-tier', '🚀 720p'));
    grid.appendChild(makeStat('Data Saved', 'teamux-net-saved', '0.0 MB'));
    dashboard.appendChild(dashTitle);
    dashboard.appendChild(grid);
    paneNetwork.appendChild(dashboard);
    body.appendChild(paneNetwork);

    const btnCompare = document.createElement('button');
    btnCompare.className = 'teamux-btn-compare';
    btnCompare.type = 'button';
    btnCompare.textContent = '👁️ Hold to Compare';
    btnCompare.style.display = (studioState.activeTab === 'themes' || studioState.activeTab === 'network') ? 'none' : 'flex';
    body.appendChild(btnCompare);

    card.appendChild(body);
    container.appendChild(card);

    const pill = document.createElement('div');
    pill.id = 'teamux-studio-pill';
    pill.className = 'teamux-studio-pill';
    const pillIcon = document.createElement('span');
    pillIcon.textContent = '✨';
    const pillText = document.createElement('span');
    pillText.textContent = 'Studio';
    const pillNetBadge = document.createElement('span');
    pillNetBadge.id = 'teamux-pill-net-badge';
    pillNetBadge.className = 'teamux-pill-net-badge';
    pillNetBadge.textContent = QUALITY_PROFILES[networkState.currentTier]?.badge || '720p';
    pill.appendChild(pillIcon);
    pill.appendChild(pillText);
    pill.appendChild(pillNetBadge);
    container.appendChild(pill);
    document.body.appendChild(container);

    // Call Recovery Banner
    const callBanner = document.createElement('div');
    callBanner.id = 'teamux-call-banner';
    const callText = document.createElement('span');
    callText.id = 'teamux-call-banner-text';
    callText.textContent = '🟢 Active Call in Progress';
    const callBtn = document.createElement('span');
    callBtn.textContent = 'RETURN TO MEETING';
    callBtn.style.cssText = 'background:#22c55e; color:#0f172a; font-weight:700; padding:2px 8px; border-radius:12px; font-size:11px;';
    callBanner.appendChild(callText);
    callBanner.appendChild(callBtn);
    document.body.appendChild(callBanner);
    callBanner.addEventListener('click', () => {
      // Delay slightly so mainWindow click finishes before focusing any pop-out meeting window
      setTimeout(() => window.teamuxBridge?.bringAllToFront(), 60);

      const findAndClickReturn = (rootDoc) => {
        if (!rootDoc) return false;
        const selectors = [
          '[data-tid="return-to-call-button"]',
          '[data-tid="calling-header-return-button"]',
          '[data-tid="calling-pip"]',
          '[data-tid*="calling-mini"]',
          '[data-tid*="pip-container"]',
          '[aria-label*="Return to call" i]',
          '[aria-label*="Back to call" i]',
          '[aria-label*="Return to meeting" i]',
          '[aria-label*="Tap to return" i]',
          '[aria-label*="Maximize call" i]',
          '[aria-label*="Resume call" i]'
        ];
        for (const sel of selectors) {
          const el = rootDoc.querySelector(sel);
          if (el) { el.click(); return true; }
        }
        // Fallback: match visible button text (New Teams v2 PIP / header bar)
        const btns = rootDoc.querySelectorAll('button, [role="button"]');
        for (const b of btns) {
          const txt = (b.textContent || '').trim();
          if (/^(return to call|back to call|return to meeting|tap to return)/i.test(txt)) {
            b.click();
            return true;
          }
        }
        return false;
      };

      if (!findAndClickReturn(document)) {
        const frames = document.querySelectorAll('iframe');
        for (const fr of frames) {
          try {
            if (findAndClickReturn(fr.contentDocument)) break;
          } catch (_) {}
        }
      }
    });

    // S5: Privacy Lock Overlay
    const lockOverlay = document.createElement('div');
    lockOverlay.id = 'teamux-privacy-lock';
    const lockCard = document.createElement('div');
    lockCard.className = 'teamux-lock-card';
    const lockTitle = document.createElement('div');
    lockTitle.style.cssText = 'font-size:18px; font-weight:700; margin-bottom:6px;';
    lockTitle.textContent = '🔒 Teamux Privacy Lock';
    const lockSub = document.createElement('div');
    lockSub.id = 'teamux-lock-sub';
    lockSub.style.cssText = 'font-size:12px; color:#a1a1aa;';
    lockSub.textContent = 'Screen hidden for branch desk privacy.';
    const lockInput = document.createElement('input');
    lockInput.id = 'teamux-lock-pin';
    lockInput.type = 'password';
    lockInput.maxLength = 4;
    lockInput.placeholder = '••••';
    lockInput.className = 'teamux-lock-input';
    const lockErr = document.createElement('div');
    lockErr.id = 'teamux-lock-err';
    lockErr.style.cssText = 'font-size:11px; color:#f87171; min-height:16px;';
    const lockBtn = document.createElement('button');
    lockBtn.className = 'teamux-lock-btn';
    lockBtn.type = 'button';
    lockBtn.textContent = '🔓 Unlock Teamux';
    lockCard.appendChild(lockTitle);
    lockCard.appendChild(lockSub);
    lockCard.appendChild(lockInput);
    lockCard.appendChild(lockErr);
    lockCard.appendChild(lockBtn);
    lockOverlay.appendChild(lockCard);
    document.body.appendChild(lockOverlay);

    const tryUnlock = () => {
      const pin = runtimeConfig.privacyPin;
      if (pin && /^\d{4}$/.test(pin)) {
        if (lockInput.value === pin) {
          lockOverlay.style.display = 'none';
          lockInput.value = '';
          lockErr.textContent = '';
        } else {
          lockErr.textContent = 'Incorrect 4-digit PIN.';
          lockInput.value = '';
          lockInput.focus();
        }
      } else {
        lockOverlay.style.display = 'none';
      }
    };
    lockBtn.addEventListener('click', tryUnlock);
    lockInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') tryUnlock(); });

    // Tab switching
    const switchTab = (name, tabEl, paneEl, showCompare) => {
      [tabRetouch, tabTone, tabThemes, tabNetwork].forEach((t) => t.classList.remove('active'));
      [paneRetouch, paneTone, paneThemes, paneNetwork].forEach((p) => p.classList.add('hidden'));
      tabEl.classList.add('active');
      paneEl.classList.remove('hidden');
      btnCompare.style.display = showCompare ? 'flex' : 'none';
      studioState.activeTab = name;
      saveStudioSettings();
      if (name === 'network') updateNetworkDashboardUI();
    };
    tabRetouch.addEventListener('click', () => switchTab('retouch', tabRetouch, paneRetouch, true));
    tabTone.addEventListener('click', () => switchTab('tone', tabTone, paneTone, true));
    tabThemes.addEventListener('click', () => switchTab('themes', tabThemes, paneThemes, false));
    tabNetwork.addEventListener('click', () => switchTab('network', tabNetwork, paneNetwork, false));

    // Listeners: Retouch & Mic
    const toggleBeauty = container.querySelector('#teamux-toggle-beauty');
    const toggleLight = container.querySelector('#teamux-toggle-light');
    const toggleVignette = container.querySelector('#teamux-toggle-vignette');
    const toggleMirror = container.querySelector('#teamux-toggle-mirror');
    const toggleAway = container.querySelector('#teamux-toggle-away');
    const toggleNoise = container.querySelector('#teamux-toggle-noisegate');
    const togglePtt = container.querySelector('#teamux-toggle-ptt');

    toggleBeauty?.addEventListener('change', () => {
      studioState.beautyEnabled = toggleBeauty.checked;
      smoothGroup.group.style.opacity = studioState.beautyEnabled ? '1' : '0.4';
      smoothGroup.group.style.pointerEvents = studioState.beautyEnabled ? 'auto' : 'none';
      saveStudioSettings();
    });
    smoothGroup.rangeInput.addEventListener('input', () => {
      studioState.beautyLevel = parseInt(smoothGroup.rangeInput.value, 10);
      smoothGroup.valSpan.textContent = `${studioState.beautyLevel}%`;
      saveStudioSettings();
    });
    toggleLight?.addEventListener('change', () => { studioState.studioLightEnabled = toggleLight.checked; saveStudioSettings(); });
    toggleVignette?.addEventListener('change', () => { studioState.vignetteEnabled = toggleVignette.checked; saveStudioSettings(); });
    toggleMirror?.addEventListener('change', () => { studioState.mirrorCamera = toggleMirror.checked; saveStudioSettings(); });
    toggleAway?.addEventListener('change', () => {
      studioState.awaySlateActive = toggleAway.checked;
      if (!studioState.awaySlateActive && currentCameraContext) currentCameraContext.resumeRender();
    });
    toggleNoise?.addEventListener('change', () => { studioState.noiseGateEnabled = toggleNoise.checked; saveStudioSettings(); });
    togglePtt?.addEventListener('change', () => {
      studioState.pushToTalkEnabled = togglePtt.checked;
      saveStudioSettings();
      if (currentAudioContextCtrl) currentAudioContextCtrl.updateGain();
    });

    // Listeners: Tone
    const toggleGrayscale = container.querySelector('#teamux-toggle-grayscale');
    toggleGrayscale?.addEventListener('change', () => {
      studioState.grayscaleEnabled = toggleGrayscale.checked;
      satGroup.group.style.opacity = studioState.grayscaleEnabled ? '0.4' : '1';
      satGroup.group.style.pointerEvents = studioState.grayscaleEnabled ? 'none' : 'auto';
      saveStudioSettings();
    });
    contrastGroup.rangeInput.addEventListener('input', () => { studioState.contrast = parseInt(contrastGroup.rangeInput.value, 10); contrastGroup.valSpan.textContent = `${studioState.contrast}%`; saveStudioSettings(); });
    satGroup.rangeInput.addEventListener('input', () => { studioState.saturation = parseInt(satGroup.rangeInput.value, 10); satGroup.valSpan.textContent = `${studioState.saturation}%`; saveStudioSettings(); });
    shadowsGroup.rangeInput.addEventListener('input', () => { studioState.shadows = parseInt(shadowsGroup.rangeInput.value, 10); shadowsGroup.valSpan.textContent = `${studioState.shadows > 0 ? '+' : ''}${studioState.shadows}`; saveStudioSettings(); });
    ambienceGroup.rangeInput.addEventListener('input', () => { studioState.ambience = parseInt(ambienceGroup.rangeInput.value, 10); ambienceGroup.valSpan.textContent = `${studioState.ambience}%`; saveStudioSettings(); });
    btnResetTone.addEventListener('click', () => {
      studioState.grayscaleEnabled = false; studioState.contrast = 100; studioState.saturation = 100; studioState.shadows = 0; studioState.ambience = 0;
      if (toggleGrayscale) toggleGrayscale.checked = false;
      satGroup.group.style.opacity = '1'; satGroup.group.style.pointerEvents = 'auto';
      contrastGroup.rangeInput.value = '100'; contrastGroup.valSpan.textContent = '100%';
      satGroup.rangeInput.value = '100'; satGroup.valSpan.textContent = '100%';
      shadowsGroup.rangeInput.value = '0'; shadowsGroup.valSpan.textContent = '0';
      ambienceGroup.rangeInput.value = '0'; ambienceGroup.valSpan.textContent = '0%';
      saveStudioSettings();
    });

    // Listeners: Compare
    const startCompare = () => { studioState.isComparing = true; btnCompare.classList.add('active'); btnCompare.textContent = '👁️ Showing RAW Original'; };
    const stopCompare = () => { studioState.isComparing = false; btnCompare.classList.remove('active'); btnCompare.textContent = '👁️ Hold to Compare'; };
    btnCompare.addEventListener('mousedown', startCompare);
    btnCompare.addEventListener('touchstart', startCompare, { passive: true });
    window.addEventListener('mouseup', stopCompare);
    window.addEventListener('touchend', stopCompare);

    // Listeners: Network
    const toggleGuardian = container.querySelector('#teamux-toggle-guardian');
    const toggleMetered = container.querySelector('#teamux-toggle-metered');
    const selectBandwidth = container.querySelector('#teamux-select-bandwidth');
    toggleGuardian?.addEventListener('change', () => {
      networkState.guardianEnabled = toggleGuardian.checked;
      saveNetworkSettings();
      evaluateAndApplyAdaptiveNetwork(networkState.currentRtt, networkState.currentLoss, networkState.currentBitrate);
    });
    toggleMetered?.addEventListener('change', () => {
      networkState.meteredMode = toggleMetered.checked;
      saveNetworkSettings();
      evaluateAndApplyAdaptiveNetwork(networkState.currentRtt, networkState.currentLoss, networkState.currentBitrate);
    });
    selectBandwidth?.addEventListener('change', () => {
      networkState.bandwidthMode = selectBandwidth.value;
      saveNetworkSettings();
      evaluateAndApplyAdaptiveNetwork(networkState.currentRtt, networkState.currentLoss, networkState.currentBitrate);
    });

    minBtn.addEventListener('click', () => { card.style.display = 'none'; pill.style.display = 'flex'; });
    pill.addEventListener('click', () => { pill.style.display = 'none'; card.style.display = 'flex'; });
  }

  function showStudioWidget() {
    if (!isTopFrame) {
      window.teamuxBridge?.requestShowStudio();
      return;
    }
    const widget = document.getElementById('teamux-studio-widget');
    const card = document.getElementById('teamux-studio-card');
    const pill = document.getElementById('teamux-studio-pill');
    if (widget) widget.style.display = 'block';
    if (card && pill) { pill.style.display = 'none'; card.style.display = 'flex'; }
  }

  function togglePrivacyLockUI() {
    if (!isTopFrame) return;
    const overlay = document.getElementById('teamux-privacy-lock');
    if (!overlay) return;
    const isVisible = overlay.style.display === 'flex';
    if (isVisible) {
      if (!runtimeConfig.privacyPin) overlay.style.display = 'none';
      return;
    }
    const pinInput = document.getElementById('teamux-lock-pin');
    const sub = document.getElementById('teamux-lock-sub');
    const hasPin = Boolean(runtimeConfig.privacyPin && /^\d{4}$/.test(runtimeConfig.privacyPin));
    if (pinInput) {
      pinInput.style.display = hasPin ? 'block' : 'none';
      pinInput.value = '';
    }
    if (sub) sub.textContent = hasPin ? 'Enter your 4-digit PIN to unlock.' : 'Screen hidden for branch desk privacy.';
    overlay.style.display = 'flex';
    if (hasPin && pinInput) setTimeout(() => pinInput.focus(), 50);
  }

  function updateStudioPillNetworkBadge() {
    if (!isTopFrame) return;
    const badge = document.getElementById('teamux-pill-net-badge');
    if (!badge) return;
    const profile = QUALITY_PROFILES[networkState.currentTier] || QUALITY_PROFILES['720p'];
    badge.textContent = profile.badge;
    badge.style.background = networkState.currentTier === 'audio-only' ? '#dc2626' : (networkState.currentTier === '360p' ? '#d97706' : 'rgba(255,255,255,0.15)');
  }

  function updateNetworkDashboardUI() {
    if (!isTopFrame) return;
    const rttEl = document.getElementById('teamux-net-rtt');
    const lossEl = document.getElementById('teamux-net-loss');
    const tierEl = document.getElementById('teamux-net-tier');
    const savedEl = document.getElementById('teamux-net-saved');
    const statusEl = document.getElementById('teamux-net-badge-status');

    if (rttEl) rttEl.textContent = `${networkState.currentRtt || 0} ms`;
    if (lossEl) {
      lossEl.textContent = `${networkState.currentLoss || 0}%`;
      lossEl.style.color = (networkState.currentLoss || 0) > 5 ? '#f87171' : '#f4f4f5';
    }
    if (tierEl) {
      const prof = QUALITY_PROFILES[networkState.currentTier] || QUALITY_PROFILES['720p'];
      tierEl.textContent = `${prof.icon} ${prof.badge}`;
    }
    if (savedEl) {
      savedEl.textContent = `${(networkState.bytesSaved / (1024 * 1024)).toFixed(1)} MB`;
    }
    if (statusEl) {
      statusEl.className = 'teamux-status-badge';
      if (networkState.currentTier === 'audio-only') { statusEl.classList.add('teamux-status-critical'); statusEl.textContent = 'Audio-First'; }
      else if (networkState.currentTier === '360p') { statusEl.classList.add('teamux-status-poor'); statusEl.textContent = 'Eco Saver'; }
      else if (networkState.currentTier === '480p') { statusEl.classList.add('teamux-status-moderate'); statusEl.textContent = 'Balanced'; }
      else { statusEl.classList.add('teamux-status-good'); statusEl.textContent = 'Optimal'; }
    }
  }

  function updateActiveCallBanner() {
    if (!isTopFrame) return;
    const isCallActive = activeStreams.size > 0;
    window.teamuxBridge?.setCallActive(isCallActive);

    const banner = document.getElementById('teamux-call-banner');
    if (!banner) return;
    banner.style.display = isCallActive ? 'flex' : 'none';
    if (!isCallActive) return;

    const callText = document.getElementById('teamux-call-banner-text');
    if (networkState.audioFirstEngaged || networkState.currentTier === 'audio-only') {
      banner.style.borderColor = '#ef4444';
      if (callText) callText.textContent = '🔴 Audio-First Protection Active (Low Bandwidth)';
    } else if (networkState.currentTier === '360p') {
      banner.style.borderColor = '#f59e0b';
      if (callText) callText.textContent = '⚠️ Eco Saver Active (Constrained Network)';
    } else {
      banner.style.borderColor = '#22c55e';
      if (callText) callText.textContent = '🟢 Active Call in Progress';
    }
  }

  // F6: Loud Office Ring Alert chime
  let lastRingTime = 0;
  function playLoudRingChime() {
    const now = Date.now();
    if (now - lastRingTime < 4500) return;
    lastRingTime = now;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      [0, 0.22].forEach((delay, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.value = idx === 0 ? 784 : 1046.5;
        gain.gain.setValueAtTime(0.18, ctx.currentTime + delay);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + delay + 0.19);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime + delay);
        osc.stop(ctx.currentTime + delay + 0.2);
      });
      setTimeout(() => ctx.close().catch(() => {}), 700);
    } catch (_) {}
  }

  // Sync runtime config from main process
  const applyRuntimeConfig = (cfg) => {
    if (!cfg || typeof cfg !== 'object') return;
    Object.assign(runtimeConfig, cfg);
    if (typeof cfg.adaptiveNetworkGuardian === 'boolean') {
      networkState.guardianEnabled = cfg.adaptiveNetworkGuardian;
    }
    if (cfg.bandwidthMode) {
      networkState.bandwidthMode = cfg.bandwidthMode;
      evaluateAndApplyAdaptiveNetwork(networkState.currentRtt, networkState.currentLoss, networkState.currentBitrate);
    }
  };

  window.addEventListener('teamux-runtime-config', (ev) => applyRuntimeConfig(ev.detail));
  window.teamuxBridge?.onConfigUpdated(applyRuntimeConfig);
  window.teamuxBridge?.onShowStudio(showStudioWidget);
  window.teamuxBridge?.onTogglePrivacyLock(togglePrivacyLockUI);

  let lastCount = 0;
  function checkTitleForBadges(title) {
    if (!isTopFrame || !title) return;
    const match = title.match(/\((\d+)\)/);
    const count = match ? parseInt(match[1], 10) : 0;
    if (count !== lastCount) {
      lastCount = count;
      window.teamuxBridge?.sendUnreadCount(count);
    }
  }

  window.addEventListener('DOMContentLoaded', () => {
    if (!isTopFrame) return;

    const style = document.createElement('style');
    style.id = 'teamux-custom-styles';
    style.textContent = '[data-tid="download-desktop-app-banner"],[data-tid="app-download-banner"],.download-desktop-banner,.use-desktop-app-bar{display:none!important;}';
    document.head.appendChild(style);

    applyTheme(currentTheme);
    injectStudioUI();

    // Watchdog for SPA navigation (lightweight)
    setInterval(() => {
      if (document.body && !document.getElementById('teamux-studio-widget')) injectStudioUI();
      if (!document.getElementById('teamux-theme-styles') && currentTheme !== 'default') applyTheme(currentTheme);
      if (runtimeConfig.loudRingAlert && document.querySelector('[data-tid="accept-call-button"], [aria-label*="Accept with audio"]')) {
        playLoudRingChime();
      }
    }, 4000);

    // P6: MutationObserver only (removed redundant 5s polling interval)
    const titleElement = document.querySelector('title');
    if (titleElement) {
      new MutationObserver(() => checkTitleForBadges(document.title)).observe(titleElement, { childList: true });
      checkTitleForBadges(document.title);
    }

    // Keyboard shortcuts: Ctrl+Shift+V (Away Slate), Ctrl+Space (Push-to-Talk)
    window.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.shiftKey && e.code === 'KeyV') {
        studioState.awaySlateActive = !studioState.awaySlateActive;
        const chk = document.getElementById('teamux-toggle-away');
        if (chk) chk.checked = studioState.awaySlateActive;
        if (!studioState.awaySlateActive && currentCameraContext) currentCameraContext.resumeRender();
      }
      if (studioState.pushToTalkEnabled && e.ctrlKey && e.code === 'Space' && !studioState.pttActive) {
        studioState.pttActive = true;
        if (currentAudioContextCtrl) currentAudioContextCtrl.updateGain();
      }
    });

    window.addEventListener('keyup', (e) => {
      if (studioState.pushToTalkEnabled && (e.code === 'Space' || !e.ctrlKey) && studioState.pttActive) {
        studioState.pttActive = false;
        if (currentAudioContextCtrl) currentAudioContextCtrl.updateGain();
      }
    });

    document.addEventListener('click', (e) => {
      const el = e.target;
      if (!el) return;
      if (el.closest('[data-tid*="hangup"], [data-tid*="call-end"], [aria-label*="Leave"], [aria-label*="Hang up"], #hangup-button')) {
        setTimeout(stopAllStreams, 150);
      }
    }, true);
  });

  window.addEventListener('beforeunload', stopAllStreams);
}

// Execute page-world hook immediately in the main world
try {
  webFrame.executeJavaScript(`(${initTeamuxPageHook.toString()})();`);
} catch (err) {
  console.error('[Teamux Preload] Failed to inject page hook:', err);
}

// Fetch runtime config from main process and sync it into the page world
ipcRenderer.invoke('get-runtime-config').then((cfg) => {
  try {
    webFrame.executeJavaScript(`window.dispatchEvent(new CustomEvent('teamux-runtime-config', { detail: ${JSON.stringify(cfg)} }));`);
  } catch (_) {}
}).catch(() => {});
