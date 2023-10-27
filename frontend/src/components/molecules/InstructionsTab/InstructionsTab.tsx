import { instructionsList } from "../../../utils/constants";
import { FormControlLabel, Checkbox } from "@mui/material";
import React, { useState, useEffect } from "react";

interface InstructionsTabProps {
  onInstructionsCheckChange: (consent: boolean) => void;
  glassDetected: boolean;
}

const InstructionsTab = ({ onInstructionsCheckChange, glassDetected }: InstructionsTabProps) => {
  const [checkedInstructions, setCheckedInstructions] = useState(
    instructionsList.map(() => false) // Initialize all checkboxes as unchecked
  );

  useEffect(() => {
    // Calculate whether all checkboxes are checked
    checkedInstructions[0] = !glassDetected; // The first checkbox is always checked if glass is not detected
    const allChecked = checkedInstructions.every((checked) => checked);
    onInstructionsCheckChange(allChecked); // Pass the status to the parent component
  }, [checkedInstructions, onInstructionsCheckChange]);

  const handleCheckboxChange = (index: number) => {
    const newCheckedInstructions = [...checkedInstructions];
    newCheckedInstructions[index] = !newCheckedInstructions[index];
    setCheckedInstructions(newCheckedInstructions);
  };

  return (
    <div className="flex flex-col p-4 border-l-gray-100 border-l-2 h-[calc(100vh-4rem)] w-full items-center gap-y-5">
      <div className="text-3xl">Instructions</div>
      <div className="w-full flex flex-col h-full items-start space-y-6">
        {instructionsList.map((instruction, index) => (
          <div key={index} className="flex items-center space-x-3">
            {index === 0 ? (
              <div style={{ display: "flex", alignItems: "center" }}>
                <span style={{ color: glassDetected ? "red" : "green" }}>
                  {glassDetected ? "✗" : "✓"}
                </span>
                <span style={{ marginLeft: "8px", color: glassDetected ? "red" : "green" }}>
                  {instruction}
                </span>
              </div>
            ) : (
              <FormControlLabel
                control={
                  <Checkbox
                    checked={checkedInstructions[index]}
                    onChange={() => handleCheckboxChange(index)}
                  />
                }
                label={instruction}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default InstructionsTab;
