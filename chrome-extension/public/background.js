chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: "sendToAPI",
      title: "Analyze validitiy of highlighted text",
      contexts: ["selection"]
    });
  });

  chrome.contextMenus.onClicked.addListener((info, tab) => {
    console.log("TEST:");
    console.log(info.selectionText);

    if (info.menuItemId === "sendToAPI" && info.selectionText) {
      chrome.storage.local.set({ highlightedText: info.selectionText }, () => {
        if (chrome.runtime.lastError) {
          console.error("Storage error:", chrome.runtime.lastError);
        } else {
          console.log("Text saved:", info.selectionText);
        }
      });
    }
    // if (info.menuItemId === "sendToAPI" && info.selectionText) {
    //   console.log("SENDING TO LOCAL");
    //   chrome.storage.local.set({ highlightedText: info.selectionText });
    // }
    
  });