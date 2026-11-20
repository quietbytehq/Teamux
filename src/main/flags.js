// src/main/flags.js
// Linux, Wayland, PipeWire, GPU Acceleration, and Resource Optimization switches

const { app } = require('electron');

function configureAppFlags(store) {
  const hardwareAccel = store.get('hardwareAcceleration', true);
  const forceWayland = store.get('forceWayland', false);

  if (!hardwareAccel) {
    app.disableHardwareAcceleration();
  }

  // Ozone Platform hint (Wayland vs X11)
  if (forceWayland) {
    app.commandLine.appendSwitch('ozone-platform', 'wayland');
  } else {
    // 'auto' detects Wayland if WAYLAND_DISPLAY is present, else falls back to X11 cleanly
    app.commandLine.appendSwitch('ozone-platform-hint', 'auto');
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

  // 4. Features to enable / disable for low footprint, stable Wayland display, and fast media
  // Note: CanvasOopRasterization and WaylandWindowDecorations are intentionally omitted:
  // - CanvasOopRasterization causes GPU IPC deadlocks with canvas filter pipelines on hybrid Intel/NVIDIA Linux
  // - WaylandWindowDecorations breaks on GNOME Wayland which strictly mandates CSD (client-side decorations)
  const enableFeatures = [
    'WebRTCPipeWireCapturer',
    'PulseaudioLoopbackForCast'
  ];

  const disableFeatures = [
    'MediaRouter',
    'Translate',
    'AutofillServerCommunication',
    'OptimizationHints'
  ];

  app.commandLine.appendSwitch('enable-features', enableFeatures.join(','));
  app.commandLine.appendSwitch('disable-features', disableFeatures.join(','));
  app.commandLine.appendSwitch('enable-webrtc-pipewire-capturer');

  // Audio / Media auto-play policy for uninterrupted calls
  app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');

  // Input method support for Wayland
  app.commandLine.appendSwitch('enable-wayland-ime');
}

module.exports = { configureAppFlags };
