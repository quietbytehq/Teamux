// src/main/user-agent.js
// Configures User-Agent and Client Hints to ensure Microsoft Teams
// fully enables HD calling, camera, and screen sharing on Linux and Windows.

const CHROME_VERSION = '131.0.0.0';
const CHROME_MAJOR = '131';

const IS_WIN = process.platform === 'win32';
const CHROME_UA = IS_WIN
  ? `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${CHROME_VERSION} Safari/537.36`
  : `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${CHROME_VERSION} Safari/537.36`;
const CH_PLATFORM = IS_WIN ? '"Windows"' : '"Linux"';

function setupUserAgent(session) {
  session.setUserAgent(CHROME_UA);

  const filter = {
    urls: [
      '*://*.teams.microsoft.com/*',
      '*://*.teams.cloud.microsoft/*',
      '*://*.cloud.microsoft/*',
      '*://*.teams.live.com/*',
      '*://*.microsoft.com/*',
      '*://*.microsoftonline.com/*',
      '*://*.live.com/*',
      '*://*.office.com/*',
      '*://*.office365.com/*',
      '*://*.sharepoint.com/*',
      '*://*.msftauth.net/*'
    ]
  };

  session.webRequest.onBeforeSendHeaders(filter, (details, callback) => {
    const requestHeaders = Object.assign({}, details.requestHeaders);
    requestHeaders['User-Agent'] = CHROME_UA;
    requestHeaders['Sec-CH-UA'] = `"Chromium";v="${CHROME_MAJOR}", "Google Chrome";v="${CHROME_MAJOR}", "Not_A Brand";v="24"`;
    requestHeaders['Sec-CH-UA-Mobile'] = '?0';
    requestHeaders['Sec-CH-UA-Platform'] = CH_PLATFORM;

    callback({ requestHeaders });
  });
}

module.exports = {
  CHROME_UA,
  setupUserAgent
};
