// src/main/tray.js
// Cross-platform System Tray integration for Teamux (Linux & Windows)

const { Tray, Menu, app } = require('electron');
const path = require('path');

let tray = null;
let currentUnread = 0;
let trayActions = {};

function createTray(mainWindow, openSettings, bringAllToFront, actions = {}) {
  trayActions = actions;
  const assetsDir = path.join(__dirname, '../../assets');
  const iconPath = path.join(assetsDir, 'tray-idle.png');

  tray = new Tray(iconPath);
  tray.setToolTip('Teamux - Microsoft Teams');

  updateContextMenu(mainWindow, openSettings, bringAllToFront);

  tray.on('click', () => {
    if (typeof bringAllToFront === 'function') {
      bringAllToFront();
    } else if (mainWindow && !mainWindow.isDestroyed()) {
      if (mainWindow.isVisible() && !mainWindow.isMinimized()) {
        mainWindow.hide();
      } else {
        mainWindow.show();
        mainWindow.focus();
      }
    }
  });

  return tray;
}

function updateContextMenu(mainWindow, openSettings, bringAllToFront) {
  if (!tray) return;

  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Show Teamux (Bring All to Front)',
      click: () => {
        if (typeof bringAllToFront === 'function') {
          bringAllToFront();
        } else if (mainWindow && !mainWindow.isDestroyed()) {
          mainWindow.show();
          mainWindow.focus();
        }
      }
    },
    {
      label: 'Hide to Tray',
      click: () => {
        if (mainWindow && !mainWindow.isDestroyed()) {
          mainWindow.hide();
        }
      }
    },
    {
      label: 'Privacy Lock (Ctrl+L)',
      click: () => {
        if (typeof trayActions.togglePrivacyLock === 'function') {
          trayActions.togglePrivacyLock();
        }
      }
    },
    { type: 'separator' },
    {
      label: currentUnread > 0 ? `Unread Messages: ${currentUnread}` : 'No unread messages',
      enabled: false
    },
    { type: 'separator' },
    {
      label: 'Reload App',
      accelerator: 'CmdOrCtrl+R',
      click: () => {
        if (mainWindow && !mainWindow.isDestroyed()) {
          mainWindow.reload();
        }
      }
    },
    {
      label: 'Settings & Preferences',
      click: () => {
        if (typeof openSettings === 'function') {
          openSettings();
        }
      }
    },
    {
      label: 'Check for Updates...',
      click: () => {
        if (typeof trayActions.checkForUpdates === 'function') {
          trayActions.checkForUpdates();
        }
      }
    },
    { type: 'separator' },
    {
      label: 'Quit Teamux',
      accelerator: 'CmdOrCtrl+Q',
      click: () => {
        app.isQuitting = true;
        app.quit();
      }
    }
  ]);

  tray.setContextMenu(contextMenu);
}

function setTrayUnreadCount(count, mainWindow, openSettings, bringAllToFront) {
  currentUnread = count;
  if (!tray) return;

  const assetsDir = path.join(__dirname, '../../assets');
  const iconName = count > 0 ? 'tray-unread.png' : 'tray-idle.png';
  tray.setImage(path.join(assetsDir, iconName));

  const tip = count > 0
    ? `Teamux - ${count} unread notification${count > 1 ? 's' : ''}`
    : 'Teamux - Microsoft Teams';
  tray.setToolTip(tip);

  updateContextMenu(mainWindow, openSettings, bringAllToFront);
}

module.exports = {
  createTray,
  setTrayUnreadCount
};
