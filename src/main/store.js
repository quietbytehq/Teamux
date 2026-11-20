// src/main/store.js
// Lightweight, reliable configuration manager for Teamux

const fs = require('fs');
const path = require('path');
const { app } = require('electron');

class SettingsStore {
  constructor() {
    this.userDataPath = app.getPath('userData');
    this.configPath = path.join(this.userDataPath, 'teamux-config.json');
    this.defaults = {
      startMinimized: false,
      minimizeToTray: false,
      closeToTray: false,
      hardwareAcceleration: true,
      forceWayland: false,
      teamsUrl: 'https://teams.cloud.microsoft/',
      windowBounds: { width: 1280, height: 820 },
      isMaximized: false,
      enableUnreadBadges: true,
      enableNotifications: true,
      configVersion: 2
    };
    this.data = this.load();
  }

  load() {
    try {
      if (fs.existsSync(this.configPath)) {
        const raw = fs.readFileSync(this.configPath, 'utf8');
        const parsed = JSON.parse(raw);
        // Migration: Default closeToTray to false for users upgrading from v0.1/v0.2
        // so clicking the window close button cleanly exits rather than hanging in the background
        if (!parsed.configVersion || parsed.configVersion < 2) {
          parsed.closeToTray = false;
          parsed.minimizeToTray = false;
          parsed.configVersion = 2;
        }
        return Object.assign({}, this.defaults, parsed);
      }
    } catch (err) {
      console.warn('[Teamux Store] Failed to load config, using defaults:', err.message);
    }
    return Object.assign({}, this.defaults);
  }

  save() {
    try {
      if (!fs.existsSync(this.userDataPath)) {
        fs.mkdirSync(this.userDataPath, { recursive: true });
      }
      fs.writeFileSync(this.configPath, JSON.stringify(this.data, null, 2), 'utf8');
    } catch (err) {
      console.error('[Teamux Store] Failed to save config:', err.message);
    }
  }

  get(key, fallback) {
    if (this.data[key] !== undefined) {
      return this.data[key];
    }
    return fallback !== undefined ? fallback : this.defaults[key];
  }

  set(key, value) {
    this.data[key] = value;
    this.save();
  }

  getAll() {
    return Object.assign({}, this.data);
  }

  setAll(newConfig) {
    this.data = Object.assign({}, this.data, newConfig);
    this.save();
  }
}

module.exports = { SettingsStore };
