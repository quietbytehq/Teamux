// src/main/media-handler.js
// Handles WebRTC media permissions, V4L2 cameras, and Wayland/X11 screen sharing
// Hardened: Whitelists only trusted Microsoft/Teams origins and required permissions.

const { BrowserWindow, desktopCapturer, ipcMain } = require('electron');
const path = require('path');

let activePickerWindow = null;
let activePickerCallback = null;
let pickerIpcRegistered = false;

const TRUSTED_HOST_REGEX = /(^|\.)(teams\.cloud\.microsoft|teams\.microsoft\.com|cloud\.microsoft|teams\.live\.com|microsoft\.com|microsoftonline\.com|live\.com|office\.com|office365\.com|sharepoint\.com|skype\.com|msftauth\.net)$/i;

const ALLOWED_PERMISSIONS = new Set([
  'media',
  'mediaKeySystem',
  'notifications',
  'display-capture',
  'fullscreen',
  'clipboard-sanitized-write',
  'clipboard-read',
  'speaker-selection',
  'pointerLock',
  'idle-detection'
]);

function isTrustedOrigin(rawUrl) {
  if (!rawUrl || typeof rawUrl !== 'string') return false;
  try {
    const parsed = new URL(rawUrl);
    if (parsed.protocol !== 'https:') return false;
    return TRUSTED_HOST_REGEX.test(parsed.hostname);
  } catch (_) {
    return false;
  }
}

function setupMediaHandlers(targetSession, getMainWindow) {
  // 1. Scoped permission handler: only trusted Microsoft origins & required permissions
  targetSession.setPermissionRequestHandler((webContents, permission, callback, details) => {
    const originUrl = (details && details.requestingUrl) || (webContents && webContents.getURL()) || '';
    const allowed = ALLOWED_PERMISSIONS.has(permission) && isTrustedOrigin(originUrl);
    if (!allowed) {
      console.warn(`[Teamux Security] Denied permission "${permission}" for origin: ${originUrl}`);
    }
    callback(allowed);
  });

  targetSession.setPermissionCheckHandler((webContents, permission, requestingOrigin) => {
    const originUrl = requestingOrigin || (webContents && webContents.getURL()) || '';
    return ALLOWED_PERMISSIONS.has(permission) && isTrustedOrigin(originUrl);
  });

  if (targetSession.setDevicePermissionHandler) {
    targetSession.setDevicePermissionHandler((details) => {
      const originUrl = (details && details.origin) || '';
      return isTrustedOrigin(originUrl);
    });
  }

  // 2. Handle Screen & Window Sharing (getDisplayMedia)
  targetSession.setDisplayMediaRequestHandler(async (request, callback) => {
    const isWayland = Boolean(process.env.WAYLAND_DISPLAY || process.env.XDG_SESSION_TYPE === 'wayland');

    try {
      if (isWayland) {
        const sources = await desktopCapturer.getSources({ types: ['screen'] });
        if (sources && sources.length > 0) {
          callback({ video: sources[0], audio: 'loopback' });
        } else {
          callback();
        }
        return;
      }

      const mainWindow = getMainWindow();
      if (activePickerCallback) {
        activePickerCallback();
        activePickerCallback = null;
      }
      if (activePickerWindow && !activePickerWindow.isDestroyed()) {
        activePickerWindow.close();
      }

      const sources = await desktopCapturer.getSources({
        types: ['screen', 'window'],
        thumbnailSize: { width: 320, height: 180 },
        fetchWindowIcons: true
      });

      if (!sources || sources.length === 0) {
        callback();
        return;
      }

      activePickerCallback = callback;
      openPickerModal(sources, mainWindow);
    } catch (err) {
      console.error('[Teamux Media] Failed to handle display media request:', err);
      callback();
    }
  });

  // Register picker IPC listeners only once across profile switches
  if (!pickerIpcRegistered) {
    pickerIpcRegistered = true;

    ipcMain.on('screen-picker-select', async (_event, sourceId) => {
      if (!activePickerCallback) return;
      try {
        const sources = await desktopCapturer.getSources({
          types: ['screen', 'window'],
          thumbnailSize: { width: 1, height: 1 }
        });
        const selected = sources.find((s) => s.id === sourceId);
        if (selected) {
          activePickerCallback({ video: selected, audio: 'loopback' });
        } else {
          activePickerCallback();
        }
      } catch (e) {
        console.error('[Teamux Media] Error selecting source:', e);
        activePickerCallback();
      } finally {
        activePickerCallback = null;
        if (activePickerWindow && !activePickerWindow.isDestroyed()) {
          activePickerWindow.close();
        }
      }
    });

    ipcMain.on('screen-picker-cancel', () => {
      if (activePickerCallback) {
        activePickerCallback();
        activePickerCallback = null;
      }
      if (activePickerWindow && !activePickerWindow.isDestroyed()) {
        activePickerWindow.close();
      }
    });
  }
}

function openPickerModal(sources, parentWindow) {
  activePickerWindow = new BrowserWindow({
    title: 'Share Screen or Window - Teamux',
    parent: parentWindow && !parentWindow.isDestroyed() ? parentWindow : null,
    modal: true,
    width: 720,
    height: 540,
    resizable: true,
    minimizable: false,
    maximizable: false,
    autoHideMenuBar: true,
    backgroundColor: '#1f1f23',
    webPreferences: {
      preload: path.join(__dirname, '../preload/picker-preload.js'),
      contextIsolation: true,
      sandbox: true,
      nodeIntegration: false
    }
  });

  activePickerWindow.loadFile(path.join(__dirname, '../ui/picker/picker.html'));

  activePickerWindow.webContents.on('did-finish-load', () => {
    const serializedSources = sources.map((s) => ({
      id: s.id,
      name: s.name,
      thumbnail: s.thumbnail ? s.thumbnail.toDataURL() : null,
      appIcon: s.appIcon ? s.appIcon.toDataURL() : null,
      isScreen: s.id.startsWith('screen:')
    }));

    activePickerWindow.webContents.send('populate-sources', serializedSources);
  });

  activePickerWindow.on('closed', () => {
    activePickerWindow = null;
    if (activePickerCallback) {
      activePickerCallback();
      activePickerCallback = null;
    }
  });
}

module.exports = { setupMediaHandlers, isTrustedOrigin };
