// src/ui/settings/settings.js

const activeProfile = document.getElementById('activeProfile');
const teamsUrl = document.getElementById('teamsUrl');
const closeToTray = document.getElementById('closeToTray');
const minimizeToTray = document.getElementById('minimizeToTray');
const startMinimized = document.getElementById('startMinimized');
const enableUnreadBadges = document.getElementById('enableUnreadBadges');
const adaptiveNetworkGuardian = document.getElementById('adaptiveNetworkGuardian');
const bandwidthMode = document.getElementById('bandwidthMode');
const lowHardwareMode = document.getElementById('lowHardwareMode');
const hardwareAcceleration = document.getElementById('hardwareAcceleration');
const forceWayland = document.getElementById('forceWayland');
const privacyPin = document.getElementById('privacyPin');
const loudRingAlert = document.getElementById('loudRingAlert');

const btnSave = document.getElementById('btnSave');
const btnCancel = document.getElementById('btnCancel');
const btnClearCache = document.getElementById('btnClearCache');
const btnCheckUpdates = document.getElementById('btnCheckUpdates');
const statusMsg = document.getElementById('status-msg');

async function loadCurrentSettings() {
  if (!window.settingsAPI) return;
  const config = await window.settingsAPI.getSettings();

  activeProfile.value = config.activeProfile || 'default';
  teamsUrl.value = config.teamsUrl || 'https://teams.cloud.microsoft/';
  closeToTray.checked = !!config.closeToTray;
  minimizeToTray.checked = !!config.minimizeToTray;
  startMinimized.checked = !!config.startMinimized;
  enableUnreadBadges.checked = !!config.enableUnreadBadges;
  adaptiveNetworkGuardian.checked = config.adaptiveNetworkGuardian !== false;
  bandwidthMode.value = config.bandwidthMode || 'auto';
  lowHardwareMode.checked = !!config.lowHardwareMode;
  hardwareAcceleration.checked = !!config.hardwareAcceleration;
  forceWayland.checked = !!config.forceWayland;
  privacyPin.value = config.privacyPin || '';
  loudRingAlert.checked = !!config.loudRingAlert;
}

btnSave.addEventListener('click', async () => {
  if (!window.settingsAPI) return;

  const pinVal = privacyPin.value.trim();
  if (pinVal && !/^\d{4}$/.test(pinVal)) {
    statusMsg.textContent = 'Privacy PIN must be exactly 4 digits (or blank).';
    return;
  }

  const updated = {
    activeProfile: activeProfile.value,
    teamsUrl: teamsUrl.value,
    closeToTray: closeToTray.checked,
    minimizeToTray: minimizeToTray.checked,
    startMinimized: startMinimized.checked,
    enableUnreadBadges: enableUnreadBadges.checked,
    adaptiveNetworkGuardian: adaptiveNetworkGuardian.checked,
    bandwidthMode: bandwidthMode.value,
    lowHardwareMode: lowHardwareMode.checked,
    hardwareAcceleration: hardwareAcceleration.checked,
    forceWayland: forceWayland.checked,
    privacyPin: pinVal,
    loudRingAlert: loudRingAlert.checked
  };

  await window.settingsAPI.saveSettings(updated);
  statusMsg.textContent = 'Settings saved!';
  setTimeout(() => {
    window.settingsAPI.closeWindow();
  }, 600);
});

btnCancel.addEventListener('click', () => {
  if (window.settingsAPI) window.settingsAPI.closeWindow();
});

btnClearCache.addEventListener('click', async () => {
  if (confirm('Clear Teamux cache and cookies for this profile? You will need to log back in.')) {
    await window.settingsAPI.clearCache();
    statusMsg.textContent = 'Cache cleared!';
  }
});

btnCheckUpdates.addEventListener('click', async () => {
  if (window.settingsAPI) {
    statusMsg.textContent = 'Checking GitHub Releases...';
    await window.settingsAPI.checkForUpdates();
    statusMsg.textContent = '';
  }
});

loadCurrentSettings();
