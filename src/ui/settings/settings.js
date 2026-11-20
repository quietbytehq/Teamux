// src/ui/settings/settings.js

const teamsUrl = document.getElementById('teamsUrl');
const closeToTray = document.getElementById('closeToTray');
const minimizeToTray = document.getElementById('minimizeToTray');
const startMinimized = document.getElementById('startMinimized');
const enableUnreadBadges = document.getElementById('enableUnreadBadges');
const adaptiveNetworkGuardian = document.getElementById('adaptiveNetworkGuardian');
const bandwidthMode = document.getElementById('bandwidthMode');
const hardwareAcceleration = document.getElementById('hardwareAcceleration');
const forceWayland = document.getElementById('forceWayland');

const btnSave = document.getElementById('btnSave');
const btnCancel = document.getElementById('btnCancel');
const btnClearCache = document.getElementById('btnClearCache');
const statusMsg = document.getElementById('status-msg');

async function loadCurrentSettings() {
  if (!window.settingsAPI) return;
  const config = await window.settingsAPI.getSettings();

  teamsUrl.value = config.teamsUrl || 'https://teams.cloud.microsoft/';
  closeToTray.checked = !!config.closeToTray;
  minimizeToTray.checked = !!config.minimizeToTray;
  startMinimized.checked = !!config.startMinimized;
  enableUnreadBadges.checked = !!config.enableUnreadBadges;
  adaptiveNetworkGuardian.checked = config.adaptiveNetworkGuardian !== false;
  bandwidthMode.value = config.bandwidthMode || 'auto';
  hardwareAcceleration.checked = !!config.hardwareAcceleration;
  forceWayland.checked = !!config.forceWayland;
}

btnSave.addEventListener('click', async () => {
  if (!window.settingsAPI) return;

  const updated = {
    teamsUrl: teamsUrl.value,
    closeToTray: closeToTray.checked,
    minimizeToTray: minimizeToTray.checked,
    startMinimized: startMinimized.checked,
    enableUnreadBadges: enableUnreadBadges.checked,
    adaptiveNetworkGuardian: adaptiveNetworkGuardian.checked,
    bandwidthMode: bandwidthMode.value,
    hardwareAcceleration: hardwareAcceleration.checked,
    forceWayland: forceWayland.checked
  };

  await window.settingsAPI.saveSettings(updated);
  statusMsg.textContent = 'Settings saved!';
  setTimeout(() => {
    window.settingsAPI.closeWindow();
  }, 600);
});

btnCancel.addEventListener('click', () => {
  if (window.settingsAPI) {
    window.settingsAPI.closeWindow();
  }
});

btnClearCache.addEventListener('click', async () => {
  if (confirm('Clear Teamux cache and cookies? You will need to log back in.')) {
    await window.settingsAPI.clearCache();
    statusMsg.textContent = 'Cache cleared!';
  }
});

loadCurrentSettings();
