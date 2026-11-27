// src/main/index.js
// Main process entry point for Teamux v2.0.0

const { app, BrowserWindow, session, ipcMain, shell, screen, dialog } = require('electron');
const path = require('path');
const https = require('https');
const { SettingsStore } = require('./store');
const { configureAppFlags } = require('./flags');
const { setupUserAgent } = require('./user-agent');
const { setupMediaHandlers, isTrustedOrigin } = require('./media-handler');
const { createTray, setTrayUnreadCount } = require('./tray');
const { buildAppMenu } = require('./menu');

// 1. Single Instance Lock
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
  process.exit(0);
}

// Register default protocol handler for msteams
if (process.defaultApp) {
  if (process.argv.length >= 2) {
    app.setAsDefaultProtocolClient('msteams', process.execPath, [path.resolve(process.argv[1])]);
  }
} else {
  app.setAsDefaultProtocolClient('msteams');
}

// 2. Initialize Persistent Store
const store = new SettingsStore();

// 3. Configure Chromium & Linux / Wayland / PipeWire / Low-Hardware Flags
configureAppFlags(store);

let mainWindow = null;
let settingsWindow = null;
const allActiveWindows = new Set();
const configuredSessions = new Set();
app.isQuitting = false;

const ALLOWED_EXTERNAL_PROTOCOLS = new Set(['https:', 'http:', 'mailto:']);
const ALLOWED_PROFILES = new Set(['default', 'work2', 'personal']);
const ALLOWED_BANDWIDTH_MODES = new Set(['auto', '720p', '480p', '360p', 'audio-only']);

function openSafeExternalUrl(rawUrl) {
  if (!rawUrl || typeof rawUrl !== 'string') return;
  try {
    const parsed = new URL(rawUrl);
    if (!ALLOWED_EXTERNAL_PROTOCOLS.has(parsed.protocol)) {
      console.warn(`[Teamux Security] Blocked unsafe external protocol: ${parsed.protocol}`);
      return;
    }
    shell.openExternal(parsed.toString());
  } catch (_) {
    console.warn('[Teamux Security] Blocked malformed external URL.');
  }
}

function getProfilePartition(profileKey) {
  const safeKey = ALLOWED_PROFILES.has(profileKey) ? profileKey : 'default';
  if (safeKey === 'default') return undefined; // defaultSession preserves existing logins on upgrade
  return `persist:teamux_${safeKey}`;
}

function ensureSessionConfigured(targetSession) {
  if (!targetSession || configuredSessions.has(targetSession)) return;
  configuredSessions.add(targetSession);
  setupUserAgent(targetSession);
  setupMediaHandlers(targetSession, () => mainWindow);
}

// Clamp and validate window bounds so the window never goes off-screen
function sanitizeWindowBounds(bounds) {
  const primaryDisplay = screen.getPrimaryDisplay();
  const workArea = primaryDisplay ? primaryDisplay.workArea : { x: 0, y: 0, width: 1920, height: 1080 };

  const defaultWidth = 1280;
  const defaultHeight = 820;

  if (!bounds || typeof bounds.width !== 'number' || typeof bounds.height !== 'number') {
    return {
      width: Math.min(defaultWidth, workArea.width),
      height: Math.min(defaultHeight, workArea.height),
      x: workArea.x + Math.max(0, Math.round((workArea.width - defaultWidth) / 2)),
      y: workArea.y + Math.max(0, Math.round((workArea.height - defaultHeight) / 2))
    };
  }

  const targetDisplay = screen.getDisplayMatching(bounds) || primaryDisplay;
  const area = targetDisplay.workArea;

  const width = Math.max(800, Math.min(bounds.width, area.width));
  const height = Math.max(560, Math.min(bounds.height, area.height));

  let x = bounds.x;
  let y = bounds.y;

  if (typeof x !== 'number' || x < area.x || x + 300 > area.x + area.width) {
    x = area.x + Math.max(0, Math.round((area.width - width) / 2));
  }
  if (typeof y !== 'number' || y < area.y || y + 60 > area.y + area.height) {
    y = area.y + Math.max(0, Math.round((area.height - height) / 2));
  }

  return { x: Math.round(x), y: Math.round(y), width: Math.round(width), height: Math.round(height) };
}

function bringAllTeamuxWindowsToFront() {
  // Show and restore mainWindow first, then focus child/meeting pop-out windows LAST so they stay on top
  if (mainWindow && !mainWindow.isDestroyed()) {
    if (mainWindow.isMinimized()) mainWindow.restore();
    if (!mainWindow.isVisible()) mainWindow.show();
    mainWindow.focus();
  }
  allActiveWindows.forEach((win) => {
    if (win && !win.isDestroyed() && win !== mainWindow) {
      if (win.isMinimized()) win.restore();
      if (!win.isVisible()) win.show();
      if (typeof win.moveTop === 'function') win.moveTop();
      win.focus();
    }
  });
}

function resetMainWindowPosition() {
  if (!mainWindow || mainWindow.isDestroyed()) return;
  const primary = screen.getPrimaryDisplay();
  const area = primary ? primary.workArea : { x: 0, y: 0, width: 1920, height: 1080 };
  const targetWidth = Math.min(1280, area.width);
  const targetHeight = Math.min(820, area.height);

  mainWindow.setSize(targetWidth, targetHeight);
  mainWindow.center();
  mainWindow.show();
  mainWindow.focus();

  store.set('windowBounds', mainWindow.getBounds());
  store.set('isMaximized', false);
}

function triggerPrivacyLock() {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send('toggle-privacy-lock');
  }
}

function compareVersions(a, b) {
  const pa = String(a).replace(/^v/i, '').split('.').map(Number);
  const pb = String(b).replace(/^v/i, '').split('.').map(Number);
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const na = pa[i] || 0;
    const nb = pb[i] || 0;
    if (na > nb) return 1;
    if (na < nb) return -1;
  }
  return 0;
}

function checkForUpdates(silent = false) {
  const currentVersion = app.getVersion();
  const options = {
    hostname: 'api.github.com',
    path: '/repos/quietbytehq/Teamux/releases/latest',
    headers: { 'User-Agent': `Teamux/${currentVersion}` },
    timeout: 7000
  };

  const req = https.get(options, (res) => {
    let body = '';
    res.on('data', (chunk) => { body += chunk; });
    res.on('end', () => {
      try {
        const data = JSON.parse(body);
        const latestTag = data && data.tag_name;
        if (!latestTag) {
          if (!silent) {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Teamux Updates',
              message: `You are running Teamux v${currentVersion}. Could not read latest release tag.`
            });
          }
          return;
        }
        const cmp = compareVersions(latestTag, currentVersion);
        if (cmp > 0) {
          dialog.showMessageBox(mainWindow, {
            type: 'info',
            title: 'Teamux Update Available',
            message: `A new version of Teamux (${latestTag}) is available!`,
            detail: `You are currently running v${currentVersion}. Open the GitHub Releases page to download the latest Windows, Linux, or Snap build.`,
            buttons: ['Download Update', 'Later'],
            defaultId: 0,
            cancelId: 1
          }).then(({ response }) => {
            if (response === 0) {
              openSafeExternalUrl(data.html_url || 'https://github.com/quietbytehq/Teamux/releases/latest');
            }
          }).catch(() => {});
        } else if (!silent) {
          dialog.showMessageBox(mainWindow, {
            type: 'info',
            title: 'Teamux Up to Date',
            message: `You are on the latest version (v${currentVersion}).`
          });
        }
      } catch (_) {
        if (!silent) {
          dialog.showMessageBox(mainWindow, {
            type: 'warning',
            title: 'Update Check Failed',
            message: 'Unable to check for updates right now. Please check your internet connection.'
          });
        }
      }
    });
  });

  req.on('error', () => {
    if (!silent) {
      dialog.showMessageBox(mainWindow, {
        type: 'warning',
        title: 'Update Check Failed',
        message: 'Unable to reach GitHub Releases. Please verify your internet connection.'
      });
    }
  });
  req.on('timeout', () => { req.destroy(); });
}

function attachNavigationSecurity(win) {
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (!isTrustedOrigin(url)) {
      openSafeExternalUrl(url);
      return { action: 'deny' };
    }
    return { action: 'allow' };
  });

  win.webContents.on('will-navigate', (event, url) => {
    if (!isTrustedOrigin(url)) {
      event.preventDefault();
      openSafeExternalUrl(url);
    }
  });
}

async function createMainWindow() {
  const rawBounds = store.get('windowBounds', { width: 1280, height: 820 });
  const bounds = sanitizeWindowBounds(rawBounds);
  const isMaximized = store.get('isMaximized', false);
  const startMinimized = store.get('startMinimized', false);
  const lowHardwareMode = store.get('lowHardwareMode', false);
  const activeProfile = store.get('activeProfile', 'default');
  const partition = getProfilePartition(activeProfile);
  const targetSession = partition ? session.fromPartition(partition) : session.defaultSession;
  ensureSessionConfigured(targetSession);

  const iconPath = path.join(__dirname, '../../assets', process.platform === 'win32' ? 'icon.ico' : 'icon.png');

  mainWindow = new BrowserWindow({
    title: `Teamux - Microsoft Teams${activeProfile !== 'default' ? ` (${activeProfile})` : ''}`,
    width: bounds.width,
    height: bounds.height,
    x: bounds.x,
    y: bounds.y,
    minWidth: 800,
    minHeight: 560,
    show: !startMinimized,
    icon: iconPath,
    backgroundColor: '#1b1b1e',
    autoHideMenuBar: false,
    webPreferences: {
      preload: path.join(__dirname, '../preload/teams-preload.js'),
      partition,
      contextIsolation: true,
      sandbox: true,
      nodeIntegration: false,
      spellcheck: !lowHardwareMode,
      backgroundThrottling: true // Dynamically disabled while in an active call
    }
  });

  allActiveWindows.add(mainWindow);

  if (isMaximized && !startMinimized) {
    mainWindow.maximize();
  }

  const saveBounds = () => {
    if (!mainWindow || mainWindow.isDestroyed()) return;
    if (!mainWindow.isMaximized() && !mainWindow.isMinimized()) {
      const current = mainWindow.getBounds();
      store.set('windowBounds', sanitizeWindowBounds(current));
    }
    store.set('isMaximized', mainWindow.isMaximized());
  };

  mainWindow.on('resize', saveBounds);
  mainWindow.on('move', saveBounds);

  let lastCloseAttempt = 0;

  mainWindow.on('close', (event) => {
    if (app.isQuitting) return;

    const now = Date.now();
    if (now - lastCloseAttempt < 2500) {
      console.log('[Teamux] Double-close detected: exiting application cleanly.');
      app.isQuitting = true;
      app.quit();
      return;
    }
    lastCloseAttempt = now;

    const closeToTray = store.get('closeToTray', false);
    if (closeToTray) {
      event.preventDefault();
      mainWindow.hide();
      return false;
    }
    saveBounds();
  });

  mainWindow.on('minimize', (event) => {
    if (store.get('minimizeToTray', false)) {
      event.preventDefault();
      mainWindow.hide();
    }
  });

  mainWindow.on('unresponsive', () => {
    console.warn('[Teamux] Window became unresponsive.');
    dialog.showMessageBox(mainWindow, {
      type: 'warning',
      title: 'Teamux Unresponsive',
      message: 'Microsoft Teams is not responding. Would you like to reload or exit?',
      buttons: ['Wait', 'Reload Teams', 'Exit Teamux'],
      defaultId: 1,
      cancelId: 0
    }).then(({ response }) => {
      if (response === 1 && mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.reload();
      } else if (response === 2) {
        app.isQuitting = true;
        app.exit(0);
      }
    }).catch(() => {});
  });

  mainWindow.webContents.on('render-process-gone', (_event, details) => {
    console.error('[Teamux] Renderer crashed or exited unexpectedly:', details.reason, 'code:', details.exitCode);
    if (details.reason !== 'clean-exit' && !app.isQuitting && mainWindow && !mainWindow.isDestroyed()) {
      console.log('[Teamux] Recovering renderer: reloading Teams...');
      mainWindow.reload();
    }
  });

  mainWindow.on('closed', () => {
    allActiveWindows.delete(mainWindow);
    mainWindow = null;
  });

  attachNavigationSecurity(mainWindow);

  mainWindow.webContents.on('did-create-window', (childWindow) => {
    childWindow.setIcon(iconPath);
    childWindow.setMinimumSize(640, 480);
    allActiveWindows.add(childWindow);
    attachNavigationSecurity(childWindow);

    childWindow.on('closed', () => {
      allActiveWindows.delete(childWindow);
    });
  });

  const teamsUrl = store.get('teamsUrl', 'https://teams.cloud.microsoft/');
  const safeTeamsUrl = isTrustedOrigin(teamsUrl) ? teamsUrl : 'https://teams.cloud.microsoft/';
  console.log(`[Teamux] Loading Microsoft Teams (${activeProfile}) from: ${safeTeamsUrl}`);
  mainWindow.loadURL(safeTeamsUrl);

  return mainWindow;
}

async function switchAccountProfile(profileKey) {
  const safeKey = ALLOWED_PROFILES.has(profileKey) ? profileKey : 'default';
  if (store.get('activeProfile', 'default') === safeKey) return;
  store.set('activeProfile', safeKey);

  const oldWin = mainWindow;
  mainWindow = null;
  if (oldWin && !oldWin.isDestroyed()) {
    oldWin.destroy();
  }
  await createMainWindow();
  rebuildAppMenus();
}

function openSettingsDialog() {
  if (settingsWindow && !settingsWindow.isDestroyed()) {
    settingsWindow.show();
    settingsWindow.focus();
    return;
  }

  settingsWindow = new BrowserWindow({
    title: 'Teamux Preferences',
    parent: mainWindow && !mainWindow.isDestroyed() ? mainWindow : null,
    modal: true,
    width: 620,
    height: 690,
    resizable: false,
    minimizable: false,
    maximizable: false,
    autoHideMenuBar: true,
    backgroundColor: '#18181b',
    webPreferences: {
      preload: path.join(__dirname, '../preload/settings-preload.js'),
      contextIsolation: true,
      sandbox: true,
      nodeIntegration: false
    }
  });

  settingsWindow.loadFile(path.join(__dirname, '../ui/settings/settings.html'));

  settingsWindow.on('closed', () => {
    settingsWindow = null;
  });
}

function rebuildAppMenus() {
  buildAppMenu(mainWindow, openSettingsDialog, {
    bringAllToFront: bringAllTeamuxWindowsToFront,
    resetPosition: resetMainWindowPosition,
    switchProfile: switchAccountProfile,
    activeProfile: store.get('activeProfile', 'default'),
    togglePrivacyLock: triggerPrivacyLock,
    checkForUpdates: () => checkForUpdates(false)
  });
}

app.on('second-instance', () => {
  bringAllTeamuxWindowsToFront();
});

app.whenReady().then(async () => {
  await createMainWindow();
  createTray(mainWindow, openSettingsDialog, bringAllTeamuxWindowsToFront, {
    togglePrivacyLock: triggerPrivacyLock,
    checkForUpdates: () => checkForUpdates(false)
  });
  rebuildAppMenus();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    } else {
      bringAllTeamuxWindowsToFront();
    }
  });
});

let quitTimeout = null;

app.on('before-quit', () => {
  app.isQuitting = true;
  if (!quitTimeout) {
    quitTimeout = setTimeout(() => {
      console.log('[Teamux] Forced termination on quit timeout.');
      process.exit(0);
    }, 1500);
    if (quitTimeout.unref) quitTimeout.unref();
  }
});

app.on('will-quit', () => {
  app.isQuitting = true;
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin' && !store.get('closeToTray', false)) {
    app.quit();
  }
});

const handleTermination = () => {
  if (app.isQuitting) return;
  app.isQuitting = true;
  try {
    BrowserWindow.getAllWindows().forEach((w) => {
      try { if (!w.isDestroyed()) w.destroy(); } catch (_) {}
    });
    app.quit();
  } finally {
    setTimeout(() => process.exit(0), 400).unref();
  }
};

process.on('SIGINT', handleTermination);
process.on('SIGTERM', handleTermination);

// IPC: Unread badge update from preload (validated)
ipcMain.on('unread-badge-update', (_event, rawCount) => {
  const count = Number.isInteger(rawCount) && rawCount >= 0 ? Math.min(rawCount, 9999) : 0;
  if (store.get('enableUnreadBadges', true)) {
    if (app.setBadgeCount) {
      app.setBadgeCount(count);
    }
    setTrayUnreadCount(count, mainWindow, openSettingsDialog, bringAllTeamuxWindowsToFront);
  }
});

// IPC: Bring all windows to front
ipcMain.on('bring-all-to-front', () => {
  bringAllTeamuxWindowsToFront();
});

// IPC: Forward studio open request from child/calling frames to top frame safely
ipcMain.on('show-studio-request', () => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send('show-studio');
  }
});

// IPC: Dynamic backgroundThrottling based on active WebRTC call
ipcMain.on('call-state-changed', (_event, isActive) => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.setBackgroundThrottling(!Boolean(isActive));
  }
});

// IPC: Reset window position
ipcMain.on('reset-window-position', () => {
  resetMainWindowPosition();
});

// IPC: Runtime config for preload/page-hook
ipcMain.handle('get-runtime-config', () => {
  return {
    lowHardwareMode: !!store.get('lowHardwareMode', false),
    adaptiveNetworkGuardian: store.get('adaptiveNetworkGuardian', true) !== false,
    bandwidthMode: store.get('bandwidthMode', 'auto'),
    privacyPin: String(store.get('privacyPin', '') || ''),
    loudRingAlert: !!store.get('loudRingAlert', false),
    activeProfile: store.get('activeProfile', 'default')
  };
});

// IPC: Check for updates from Settings
ipcMain.handle('check-for-updates', () => {
  checkForUpdates(false);
  return true;
});

// IPC: Settings management (validated)
ipcMain.handle('get-settings', () => {
  return store.getAll();
});

ipcMain.handle('save-settings', async (_event, newSettings) => {
  if (!newSettings || typeof newSettings !== 'object') return false;

  const oldUrl = store.get('teamsUrl');
  const oldProfile = store.get('activeProfile', 'default');

  const sanitized = {
    teamsUrl: isTrustedOrigin(newSettings.teamsUrl) ? newSettings.teamsUrl : oldUrl,
    activeProfile: ALLOWED_PROFILES.has(newSettings.activeProfile) ? newSettings.activeProfile : oldProfile,
    closeToTray: Boolean(newSettings.closeToTray),
    minimizeToTray: Boolean(newSettings.minimizeToTray),
    startMinimized: Boolean(newSettings.startMinimized),
    enableUnreadBadges: Boolean(newSettings.enableUnreadBadges),
    adaptiveNetworkGuardian: Boolean(newSettings.adaptiveNetworkGuardian),
    bandwidthMode: ALLOWED_BANDWIDTH_MODES.has(newSettings.bandwidthMode) ? newSettings.bandwidthMode : 'auto',
    hardwareAcceleration: Boolean(newSettings.hardwareAcceleration),
    lowHardwareMode: Boolean(newSettings.lowHardwareMode),
    forceWayland: Boolean(newSettings.forceWayland),
    loudRingAlert: Boolean(newSettings.loudRingAlert),
    privacyPin: typeof newSettings.privacyPin === 'string' && /^\d{4}$/.test(newSettings.privacyPin.trim())
      ? newSettings.privacyPin.trim()
      : ''
  };

  store.setAll(sanitized);

  if (sanitized.activeProfile !== oldProfile) {
    await switchAccountProfile(sanitized.activeProfile);
    return true;
  }

  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send('config-updated', sanitized);
    if (sanitized.teamsUrl !== oldUrl) {
      mainWindow.loadURL(sanitized.teamsUrl);
    }
  }
  return true;
});

ipcMain.handle('clear-cache', async () => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    await mainWindow.webContents.session.clearStorageData();
    mainWindow.reload();
  }
  return true;
});

ipcMain.on('close-settings', () => {
  if (settingsWindow && !settingsWindow.isDestroyed()) {
    settingsWindow.close();
  }
});
