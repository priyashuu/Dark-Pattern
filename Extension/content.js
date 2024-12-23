// content.js
const darkPatternButtonClass = "dark-pattern-button";

function loadScript(url, callback) {
  const script = document.createElement("script");
  script.type = "text/javascript";
  script.src = url;
  script.onload = callback;
  document.head.appendChild(script);
}

function checkForDarkPatterns() {
  loadScript(chrome.runtime.getURL("jquery.min.js"), function () {
    const darkPatternButton = $(`.${darkPatternButtonClass}`);
    if (darkPatternButton.length > 0) {
      chrome.runtime.sendMessage({ isDarkPattern: true });
    } else {
      chrome.runtime.sendMessage({ isDarkPattern: false });
    }
  });
}

// Wait for the document to be ready before executing the script
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", checkForDarkPatterns);
} else {
  checkForDarkPatterns();
}
