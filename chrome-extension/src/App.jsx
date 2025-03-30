import { useEffect, useState } from "react";
import "./popup.css";
import React from 'react'

function App() {
  const [highlighted, setHighlighted] = useState("");
  const [result, setResult] = useState("");
  const [typedResult, setTypedResult] = useState("");
  const [loading, setLoading] = useState(false);

  const word = "Result:"

  useEffect(() => {
    if (chrome?.storage?.local) {
      chrome.storage.local.get(["highlightedText"], (result) => {
        setHighlighted(result.highlightedText || "");
      });
    }
  }, []);

  useEffect(() => {
    if (!highlighted) return;

    const analyze = async () => {
      setLoading(true);
      try {
        const res = await fetch("http://127.0.0.1:8000/api/analyze/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: highlighted })
        });
        const data = await res.json();
        //setResult(JSON.stringify(data, null, 2));
        setResult(data.response || "No response");
      } catch (err) {
        setResult("Error fetching from backend.");
        //console.log("ERROR:", err);
      }
      setLoading(false);
    };

    analyze(); //call fetch function
  }, [highlighted]);

  useEffect(() => {
    if (!result) return;

    setTypedResult("");
    let i = 0;
    let message="";
    const interval = setInterval(() => {
      if (i >= result.length) {
        clearInterval(interval);
        return;
      }
      message += result[i];
      setTypedResult(message);
      //setTypedResult((prev) => prev + result.charAt(i));
      //console.log("I:", i, result.charAt(i));
      i++;
    }, 30);

    return () => clearInterval(interval);
  }, [result]);

  return (
    <div className="w-[320px] p-4 font-sans text-sm text-gray-800 bg-white">
      <h1 className="text-lg font-semibold mb-2 text-blue-700">Facts Analyzer</h1>

      <div className="mb-3">
        <p className="text-xs text-gray-500 mb-1">Highlighted Text:</p>
        <div className="border rounded bg-gray-100 p-2 h-[80px] overflow-y-auto text-gray-700 text-sm">
          {highlighted || <span className="text-gray-400">No text selected yet</span>}
        </div>
      </div>

      {loading && <p className="text-xs text-blue-600">Analyzing...</p>}

      {typedResult && !loading && (
        <div className="border-t pt-3 mt-2">
          <h2 className="text-sm font-medium text-green-700 flex items-center gap-1">
            {word.split("").map((char, i) => (
            <span
              key={i}
              className={`inline-block animate-bounce-loop`}
              style={{ animationDelay: `${i * 100}ms` }}
            >
              {char}
            </span>
            ))}          
          </h2>
          <p className="mt-2 bg-green-50 text-green-900 p-3 rounded text-sm">
            {typedResult}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;