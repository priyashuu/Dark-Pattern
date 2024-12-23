// background.js
chrome.runtime.onInstalled.addListener(() => {
  console.log('DarkPatternDetector extension installed.');
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.isDarkPattern) {
    chrome.browserAction.setBadgeText({ text: "!" });
    chrome.browserAction.setBadgeBackgroundColor({ color: "#FF0000" });

    // Open the popup when a dark pattern is detected
    chrome.action.openPopup();
  } else {
    chrome.browserAction.setBadgeText({ text: "" });
    
    // Close the popup when no dark pattern is detected
    chrome.action.closePopup();
  }
});
