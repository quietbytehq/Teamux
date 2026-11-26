// src/main/flags.js
// Linux, Wayland, PipeWire, GPU Acceleration, and Low-Hardware Resource Optimization switches

const { app } = require('electron');

function configureAppFlags(store) {
  const hardwareAccel = store.get('hardwareAcceleration', true);
  const lowHardwareMode = store.get('lowHardwareMode', false);
  const forceWayland = store.get('forceWayland', false);

  if (!hardwareAccel) {
    app.disableHardwareAcceleration();
  }

  // Linux-specific display server & PipeWire flags
  if (process.platform === 'linux') {
    if (forceWayland) {
      app.commandLine.appendSwitch('ozone-platform', 'wayland');
    } else {
      app.commandLine.appendSwitch('ozone-platform-hint', 'auto');
    }
    app.commandLine.appendSwitch('enable-webrtc-pipewire-capturer');
    app.commandLine.appendSwitch('enable-wayland-ime');
  }

  // -----------------------------------------------------------
  // Memory & Resource Optimization Switches (Adaptive to Hardware)
  // -----------------------------------------------------------
  if (lowHardwareMode) {
    // Low-spec branch PC profile: tighter heap and cache footprints
    app.commandLine.appendSwitch('js-flags', '--max-old-space-size=896');
    app.commandLine.appendSwitch('disk-cache-size', '134217728'); // 128 MB max
    app.commandLine.appendSwitch('media-cache-size', '67108864'); // 64 MB max
    app.commandLine.appendSwitch('disable-gpu-vsync');
  } else {
    app.commandLine.appendSwitch('js-flags', '--max-old-space-size=2048');
    app.commandLine.appendSwitch('disk-cache-size', '536870912'); // 512 MB max
    app.commandLine.appendSwitch('media-cache-size', '268435456'); // 256 MB max
  }

  // Disable unnecessary background Chromium subsystems
  app.commandLine.appendSwitch('disable-breakpad');
  app.commandLine.appendSwitch('disable-component-update');
  app.commandLine.appendSwitch('disable-domain-reliability');
  app.commandLine.appendSwitch('disable-sync');

  const enableFeatures = [];
  if (process.platform === 'linux') {
    enableFeatures.push('WebRTCPipeWireCapturer', 'PulseaudioLoopbackForCast');
  }

  const disableFeatures = [
    'MediaRouter',
    'Translate',
    'AutofillServerCommunication',
    'OptimizationHints'
  ];

  if (enableFeatures.length > 0) {
    app.commandLine.appendSwitch('enable-features', enableFeatures.join(','));
  }
  app.commandLine.appendSwitch('disable-features', disableFeatures.join(','));

  // Audio / Media auto-play policy for uninterrupted calls
  app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
}

module.exports = { configureAppFlags };
