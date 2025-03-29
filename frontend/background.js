chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: "sendToAPI",
      title: "Send highlighted text to API",
      contexts: ["selection"]
    });
  });

  chrome.contextMenus.onClicked.addListener((info, tab) => {
    console.log("TEST")
    console.log(info.selectionText);
  });