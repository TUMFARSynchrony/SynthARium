import { instructionsList } from "../../../utils/constants";
import { FormControlLabel, Checkbox } from "@mui/material";
import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { ActionButton } from "../../atoms/Button";

export const InstructionsTab = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionIdParam = searchParams.get("sessionId");
  const participantIdParam = searchParams.get("participantId");

  const [checkedInstructions, setCheckedInstructions] = useState(
    instructionsList.map(() => false) // Initialize all checkboxes as unchecked
  );
  const [areInstructionsChecked, setAreInstructionsChecked] = useState(false);

  useEffect(() => {
    // Calculate whether all checkboxes are checked
    const allChecked = checkedInstructions.every((checked) => checked);
    setAreInstructionsChecked(allChecked);
  }, [checkedInstructions]);

  const handleCheckboxChange = (index: number) => {
    const newCheckedInstructions = [...checkedInstructions];
    newCheckedInstructions[index] = !newCheckedInstructions[index];
    setCheckedInstructions(newCheckedInstructions);
  };

  return (
    <div className="flex flex-col p-4 border-l-gray-100 border-l-2 h-full w-full items-center gap-y-5">
      <div className="text-3xl">Instructions</div>
      <div className="w-full flex flex-col h-full items-start space-y-6">
        {instructionsList.map((instruction, index) => (
          <FormControlLabel
            key={index}
            control={
              <Checkbox
                checked={checkedInstructions[index]}
                onChange={() => handleCheckboxChange(index)}
              />
            }
            label={instruction}
          />
        ))}
      </div>
      <div className="self-center h-fit">
        <ActionButton
          className={!areInstructionsChecked ? "pointer-events-none" : ""}
          text="Continue"
          variant="contained"
          disabled={!areInstructionsChecked}
          onClick={() => {
            window.location.href = `${window.location.origin}/meetingRoom?participantId=${participantIdParam}&sessionId=${sessionIdParam}`;
          }}
        />
      </div>
    </div>
  );
};
