import { useState } from "react";
import React from "react";

export default function WeightToggle({ onChange }) {
  const [selected, setSelected] = useState("light");

  const options = ["light", "medium", "heavy"];

  const handleSelect = (level) => {
    setSelected(level);
    onChange(level); // send back to parent
  };

  const selectedIndex = options.indexOf(selected);

  return (
    <div className="relative w-full max-w-xs mx-auto mb-4">
      <div className="flex bg-gray-200 rounded-full p-1 text-sm font-medium text-gray-600 justify-between relative">
        {/* Sliding highlight */}
        <div
          className="absolute top-1 left-1 h-8 w-1/3 bg-blue-500 rounded-full transition-all duration-300"
          style={{ transform: `translateX(${selectedIndex * 100}%)` }}
        ></div>

        {/* Options */}
        {options.map((level) => (
          <button
            key={level}
            className={`z-10 w-1/3 py-1.5 rounded-full transition text-center ${
              selected === level ? "text-white" : "text-gray-600"
            }`}
            onClick={() => handleSelect(level)}
          >
            {level.charAt(0).toUpperCase() + level.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
}