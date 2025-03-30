import { useEffect, useState } from "react";
import "./popup.css";
import React from 'react';
import WeightToggle from "./WeightToggle";

function App() {
  const [highlighted, setHighlighted] = useState("");
  const [result, setResult] = useState("");
  const [typedTitle, setTypedTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [weight, setWeight] = useState("light");

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const word = "Result:";
  const title = "Facts Analyzer";

  useEffect(() => {
    if (chrome?.storage?.local) {
      chrome.storage.local.get(["highlightedText"], (result) => {
        setHighlighted(result.highlightedText || "");
      });
    }
  }, []);

  useEffect(() => {
    let i = 0;
    let message="";
    const interval = setInterval(() => {
      if (i >= title.length) {
        clearInterval(interval);
        return;
      }
      message += title[i];
      setTypedTitle(message);
      i++;
    }, 125);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (!highlighted) return;

    const analyze = async () => {
      setLoading(true);
      await sleep(5000); // for testing loading animation

      try {
        const res = await fetch("http://127.0.0.1:8000/api/analyze/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            text: highlighted,
            weight: weight
          })
        });
        const data = await res.json();
        console.log(data);
        //setResult(JSON.stringify(data, null, 2));
        setResult(data || "No response");
      } catch (err) {
        setResult("Error fetching from backend.");
        //console.log("ERROR:", err);
      }
      setLoading(false);
    };

    analyze(); //call fetch function
  }, [highlighted]);

  function LoadingDots() {
    const [dotCount, setDotCount] = useState(0);
    const dotStates = ["", ".", "..", "..."];
  
    useEffect(() => {
      const interval = setInterval(() => {
        setDotCount((prev) => (prev + 1) % dotStates.length);
      }, 300);
  
      return () => clearInterval(interval);
    }, []);
  
    return (
      <span className="text-blue-500 font-medium tracking-wide">
        Analyzing{dotStates[dotCount]}
      </span>
    );
  }

  return (
    <div className="w-[800px] h-[500px] max-w-full p-4 font-sans text-sm text-gray-800 bg-white">
      <h1 className="text-lg font-semibold mb-2 text-blue-700">{typedTitle}</h1>

      <div className="flex items-center justify-center w-full">
        <WeightToggle onChange={setWeight} />
      </div>

      <div className="mb-3">
        <p className="text-xs text-gray-500 mb-1">Highlighted Text:</p>
        <div className="border rounded bg-gray-100 p-2 h-[80px] overflow-y-auto text-gray-700 text-sm">
          {highlighted || <span className="text-gray-400">No text selected yet</span>}
        </div>
      </div>

      {loading && <LoadingDots />}

      {result && !loading &&(
        <div className="mt-4 space-y-3 text-sm text-gray-800">
          <div className="text-lg font-semibold text-blue-700">
            Label: <span className="text-black">{result.label}</span>
          </div>
      
          <div>
            <p className="font-medium text-gray-600">Ratings:</p>
            <ul className="list-disc pl-5 text-gray-700">
              {result.ratings.map((rating, i) => (
                <li key={i}>{rating}</li>
              ))}
            </ul>
          </div>
      
          <div>
            <p className="font-medium text-gray-600">Analysis:</p>
            <ul className="list-disc pl-5 text-gray-700">
              {result.analysis.map((point, i) => (
                <li key={i}>{point}</li>
              ))}
            </ul>
          </div>
      
          <div>
            <p className="font-medium text-gray-600">Sources:</p>
            <ul className="list-disc pl-5 text-blue-600 underline">
              {result.sources.map((url, i) => (
                <li key={i}>
                  <a href={url} target="_blank" rel="noopener noreferrer">{url}</a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;