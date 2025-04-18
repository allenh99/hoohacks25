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
  const [openDropdowns, setOpenDropdowns] = useState([]);
  const [submitted, setSubmitted] = useState(false);
  const [prevData, setPrevData] = useState(false);

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const title = "CheckMate";

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
    chrome.storage.local.get(["prevData"], (result) => {
      if (result.prevData) {
        setPrevData(true);
        setResult(result.prevData);
      }
    });
  }, []);

  // useEffect(() => {
  //   if (!highlighted) return;

  const analyze = async () => {
    setSubmitted(true);
    setLoading(true);
    setPrevData(false);
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
      chrome.storage.local.set({ prevData: data });
    } catch (err) {
      setResult("Error fetching from backend.");
      //console.log("ERROR:", err);
    }
    setLoading(false);
  };

  //analyze(); //call fetch function
  // }, [highlighted]);

  useEffect(() => {
    if (result?.ratings?.length) {
      setOpenDropdowns(Array(result.ratings.length).fill(false));
    }
  }, [result]);

  const toggleDropdown = (index) => {
    setOpenDropdowns((prev) =>
      prev.map((isOpen, i) => (i === index ? !isOpen : isOpen))
    );
  };

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
      <span className="text-emerald-600 font-medium tracking-wide">
        Analyzing{dotStates[dotCount]}
      </span>
    );
  }

  return (
    <div className={`w-[1000px] ${submitted || prevData ? "h-[500px]" : "h-[300px]"} max-w-full p-4 font-sans text-sm text-gray-800 bg-white`}>
      <h1 className="text-lg font-semibold mb-2 text-green-600">{typedTitle}</h1>

      <div className="flex items-center justify-center w-full">
        <WeightToggle onChange={setWeight} />
      </div>

      <div className="mb-3">
        <p className="text-xs text-gray-500 mb-1">Highlighted Text:</p>
        <div className="border rounded bg-gray-100 p-2 h-[80px] overflow-y-auto text-gray-700 text-sm">
          {highlighted || <span className="text-gray-400">No text selected yet</span>}
        </div>
      </div>

      {!submitted && (
        <button
          onClick={analyze}
          className="bg-green-500 text-white px-4 py-2 rounded-md shadow hover:bg-green-600 transition duration-200 w-full font-medium text-sm mb-4"
        >
          Analyze
        </button>
      )}

      {prevData && (
        <div className="mt-4">      
          Past Results:  
          <div className="flex flex-wrap items-center justify-center bg-emerald-100 border border-emerald-300 text-emerald-700 p-3 rounded-md mb-4 text-sm font-semibold">
            {result.label.split("").map((char, i) => (
              <span
                key={i}
                className="inline-block animate-bounce-loop"
                style={{ animationDelay: `${i * 100}ms` }}
              >
                {char}
              </span>
            ))}
          </div>

          <div className="grid grid-cols-1 gap-4">
            {result.ratings.map((rating, i) => (
              <div
                key={i}
                className="rounded-xl bg-white shadow-md p-4 border border-gray-200 text-sm"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-green-500 font-semibold underline">
                    <a
                      href={result.sources[i]}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Source {i + 1}
                    </a>
                  </h3>
                  <button onClick={() => toggleDropdown(i)}>
                    {openDropdowns[i] ? "Less": "More"}
                  </button>
                </div>

                <p className="mb-1">
                  <span className="font-medium text-gray-600">Rating:</span>{" "}
                  {rating}/10
                </p>

                {openDropdowns[i] && (<p className="mb-1">
                    {result.analysis[i]}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {loading && <LoadingDots />}

      {result && !loading && !prevData && (
        <div className="mt-4">      
          Results:  
          <div className="flex flex-wrap items-center justify-center bg-emerald-100 border border-emerald-300 text-emerald-700 p-3 rounded-md mb-4 text-sm font-semibold">
            {result.label.split("").map((char, i) => (
              <span
                key={i}
                className="inline-block animate-bounce-loop"
                style={{ animationDelay: `${i * 100}ms` }}
              >
                {char}
              </span>
            ))}
          </div>

          <div className="grid grid-cols-1 gap-4">
            {result.ratings.map((rating, i) => (
              <div
                key={i}
                className="rounded-xl bg-white shadow-md p-4 border border-gray-200 text-sm"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-green-500 font-semibold underline">
                    <a
                      href={result.sources[i]}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Source {i + 1}
                    </a>
                  </h3>
                  <button onClick={() => toggleDropdown(i)}>
                    {openDropdowns[i] ? "Less": "More"}
                  </button>
                </div>

                <p className="mb-1">
                  <span className="font-medium text-gray-600">Rating:</span>{" "}
                  {rating}/10
                </p>

                {/* <p className="text-blue-500 underline break-all">
                  <a
                    href={result.sources[i]}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Link {i + 1}
                  </a>
                </p> */}

                {openDropdowns[i] && (<p className="mb-1">
                    {result.analysis[i]}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;