// src/main/menu.js
// Application menu configuration for Teamux v2.0.0

const { app, Menu, shell, dialog } = require('electron');

function buildAppMenu(mainWindow, openSettings, windowActions = {}) {
  const {
    bringAllToFront,
    resetPosition,
    switchProfile,
    activeProfile = 'default',
    togglePrivacyLock,
    checkForUpdates
  } = windowActions;

  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Preferences / Settings',
          accelerator: 'CmdOrCtrl+,',
          click: () => openSettings()
        },
        {
          label: 'Switch Account Profile',
          submenu: [
            {
              label: 'Work / Default Profile',
              type: 'radio',
              checked: activeProfile === 'default',
              click: () => { if (typeof switchProfile === 'function') switchProfile('default'); }
            },
            {
              label: 'Work Account 2 (Isolated)',
              type: 'radio',
              checked: activeProfile === 'work2',
              click: () => { if (typeof switchProfile === 'function') switchProfile('work2'); }
            },
            {
              label: 'Personal Account (Isolated)',
              type: 'radio',
              checked: activeProfile === 'personal',
              click: () => { if (typeof switchProfile === 'function') switchProfile('personal'); }
            }
          ]
        },
        {
          label: 'Hide to Tray',
          accelerator: 'CmdOrCtrl+W',
          click: () => {
            if (mainWindow && !mainWindow.isDestroyed()) mainWindow.hide();
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
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' },
        { role: 'selectAll' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' },
        { type: 'separator' },
        { role: 'toggleDevTools' }
      ]
    },
    {
      label: 'Window',
      submenu: [
        {
          label: 'Privacy Lock Screen',
          accelerator: 'CmdOrCtrl+L',
          click: () => {
            if (typeof togglePrivacyLock === 'function') togglePrivacyLock();
          }
        },
        { type: 'separator' },
        {
          label: 'Bring All Windows to Front',
          accelerator: 'CmdOrCtrl+Shift+B',
          click: () => {
            if (typeof bringAllToFront === 'function') bringAllToFront();
          }
        },
        {
          label: 'Reset Window Position & Size',
          accelerator: 'CmdOrCtrl+Alt+R',
          click: () => {
            if (typeof resetPosition === 'function') resetPosition();
          }
        },
        { type: 'separator' },
        {
          label: 'Toggle Always on Top',
          type: 'checkbox',
          checked: false,
          click: (menuItem) => {
            if (mainWindow && !mainWindow.isDestroyed()) {
              mainWindow.setAlwaysOnTop(menuItem.checked);
            }
          }
        },
        { role: 'minimize' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Check for Updates...',
          click: () => {
            if (typeof checkForUpdates === 'function') checkForUpdates();
          }
        },
        { type: 'separator' },
        {
          label: 'QuietByte GitHub Repository',
          click: async () => {
            await shell.openExternal('https://github.com/quietbytehq/teamux');
          }
        },
        {
          label: 'Report an Issue',
          click: async () => {
            await shell.openExternal('https://github.com/quietbytehq/teamux/issues');
          }
        },
        { type: 'separator' },
        {
          label: 'About Teamux',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'About Teamux',
              message: `Teamux v${app.getVersion()} — Microsoft Teams for Linux & Windows`,
              detail: 'Developed by QuietByte (https://quietbytehq.uk)\nFeatures: Adaptive Network Guardian, Studio Camera, Themes, Low-Hardware Mode, and Hardened Isolation.\n\nUnofficial client. Not affiliated with Microsoft Corporation.'
            });
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

module.exports = { buildAppMenu };
