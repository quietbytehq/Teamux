// src/main/flags.js
// Linux, Wayland, PipeWire, GPU Acceleration, and Resource Optimization switches

const { app } = require('electron');

function configureAppFlags(store) {
  const hardwareAccel = store.get('hardwareAcceleration', true);
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
  // Memory & Resource Optimization Switches
  // -----------------------------------------------------------
  // 1. Adequate V8 heap space so garbage collection doesn't choke modern Teams micro-frontends
  app.commandLine.appendSwitch('js-flags', '--max-old-space-size=2048');

  // 2. Cap in-memory and disk cache sizes to avoid unbounded growth while leaving room for hashed packages
  app.commandLine.appendSwitch('disk-cache-size', '536870912'); // 512 MB max
  app.commandLine.appendSwitch('media-cache-size', '268435456'); // 256 MB max

  // 3. Disable unnecessary background Chromium subsystems
  app.commandLine.appendSwitch('disable-breakpad');
  app.commandLine.appendSwitch('disable-component-update');
  app.commandLine.appendSwitch('disable-domain-reliability');
  app.commandLine.appendSwitch('disable-sync');

  // 4. Features to enable / disable for low footprint, stable display, and fast media
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
