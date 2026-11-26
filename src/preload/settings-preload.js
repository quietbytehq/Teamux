// src/preload/settings-preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('settingsAPI', {
  getSettings: () => ipcRenderer.invoke('get-settings'),
  saveSettings: (settings) => ipcRenderer.invoke('save-settings', settings),
  clearCache: () => ipcRenderer.invoke('clear-cache'),
  checkForUpdates: () => ipcRenderer.invoke('check-for-updates'),
  closeWindow: () => ipcRenderer.send('close-settings')
});
