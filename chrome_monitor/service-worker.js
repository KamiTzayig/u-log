
let focusedWindowId = undefined;
let lastLog = Date.now() - 1000; //make sure the initial log is captured


chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ enabled: true }); // Default the extension to be enabled on install
});

chrome.action.onClicked.addListener((tab) => {
  chrome.storage.local.get('enabled', (data) => {
    const currentState = data.enabled;
    chrome.storage.local.set({ enabled: !currentState }, () => {
      // Change the icon based on the current state
      const iconPath16 = currentState ? "icons/off-16.png" : "icons/on-16.png";
      const iconPath48 = currentState ? "icons/off-48.png" : "icons/on-48.png";
      const iconPath128 = currentState ? "icons/off-128.png" : "icons/on-128.png";
      chrome.action.setIcon({
        path: {
          "16": iconPath16,
          "48": iconPath48,
          "128": iconPath128
        }
      });
    });
  });
});



async function sendDataToServer(data) {
  try {
    const response = await fetch('http://127.0.0.1:2226/log', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const responseData = await response.json();
    console.log('Data successfully sent to the server');
  } catch (error) {
    console.error('Error sending data to the server:', error);
  }
}


async function bootstrap() {
  const focusedWindow = await chrome.windows.getLastFocused();
  focusedWindowId = focusedWindow.id;
  loadWindowList();
}

async function loadWindowList() {
  timestamp = Date.now();
  if (timestamp - lastLog < 200) {
    lastLog = Date.now()
    return;
  }
  lastLog = Date.now()

  chrome.storage.local.get('enabled', async (data) => {
    if (!data.enabled) {
    return;
    }else{
      const windowList = await chrome.windows.getAll({ populate: true });
      let state = {
        windows: windowList.map(window => ({
          id: window.id,
          left: window.left,
          top: window.top,
          width: window.width,
          height: window.height,
          focused: window.focused,
          tabs: window.tabs.map(tab => ({
            windowId: tab.windowId,
            title: tab.title,
            url: tab.url,
            active: tab.active,
            index: tab.index,
          }))
        }))
      };
      sendDataToServer(state)


      
    }
  }
  );
 
}

chrome.windows.onCreated.addListener(function (createInfo) {
  loadWindowList();
});

chrome.windows.onBoundsChanged.addListener(function (window) {
  loadWindowList();
});

chrome.windows.onFocusChanged.addListener(function (windowId) {
  focusedWindowId = windowId;
  loadWindowList();
});

chrome.windows.onRemoved.addListener(function (windowId) {
  loadWindowList();
});

chrome.tabs.onCreated.addListener(function (tab) {
  loadWindowList();
});

chrome.tabs.onAttached.addListener(function (tabId, props) {
  loadWindowList();
});


chrome.tabs.onUpdated.addListener(function (tabId, props) {
  loadWindowList()
});

chrome.tabs.onActivated.addListener(function (props) {
  loadWindowList();
});

chrome.tabs.onRemoved.addListener(function (tabId) {
loadWindowList()
});

