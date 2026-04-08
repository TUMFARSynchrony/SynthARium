import React, { ReactNode, useState } from "react";

interface TooltipProps {
  content: ReactNode;
  children: ReactNode;
  mode?: "dark" | "light";
  position?: "top" | "bottom" | "left" | "right";
}

const Tooltip: React.FC<TooltipProps> = ({
  content,
  children,
  mode = "light",
  position = "top"
}) => {
  const [isVisible, setIsVisible] = useState(false);

  const tooltipClasses = `absolute z-10 bg-${mode === "light" ? "white" : "gray-800"} text-${
    mode === "light" ? "black" : "white"
  } text-sm px-4 py-2 rounded whitespace-nowrap ${
    mode === "light" ? "border border-gray-300" : "border border-gray-600"
  }`;

  let positionClasses = "";

  switch (position) {
    case "top":
      positionClasses = "bottom-full left-1/2 transform -translate-x-1/2";
      break;
    case "bottom":
      positionClasses = "top-full left-1/2 transform -translate-x-1/2";
      break;
    case "left":
      positionClasses = "top-1/2 right-full transform -translate-y-1/2";
      break;
    case "right":
      positionClasses = "top-1/2 left-full transform -translate-y-1/2";
      break;
    default:
      positionClasses = "bottom-full left-1/2 transform -translate-x-1/2";
      break;
  }

  return (
    <div
      className="relative inline-block"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children}
      {isVisible && (
        <div className={`absolute ${tooltipClasses} ${positionClasses}`}>{content}</div>
      )}
    </div>
  );
};

export default Tooltip;
