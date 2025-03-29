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

    if (info.menuItemId === "sendToAPI") {
      const selectedText = info.selectionText;
  
      fetch("http://127.0.0.1:8000/api/analyze/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ tweet: selectedText })
      })
      .then(response => response.json())
      .then(data => {
        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: (responseText) => {
            alert("API response: " + responseText);
          },
          args: [JSON.stringify(data)]
        });
      })
      .catch(error => {
        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: (err) => {
            alert("Error: " + err);
          },
          args: [error.message]
        });
      });
    }
    
  });