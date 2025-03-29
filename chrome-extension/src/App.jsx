import { useEffect, useState } from "react";
import "./popup.css";

function App() {
  const [highlighted, setHighlighted] = useState("");
  const [response, setResponse] = useState("");

  useEffect(() => {
    chrome.storage.local.get(["highlightedText"], async (result) => {
      const text = result.highlightedText;
      setHighlighted(text);

      if (text) {
        try {
          const res = await fetch("http://127.0.0.1:8000/api/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
          });
          const data = await res.json();
          setResponse(JSON.stringify(data));
        } catch (error) {
          setResponse("Error: " + error.message);
        }
      }
    });
  }, []);

  return (
    <div className="popup">
      <h3>Highlighted Text:</h3>
      <p>{highlighted || "(none selected yet)"}</p>
      <h3>Response:</h3>
      <pre>{response}</pre>
    </div>
  );
}

export default App;