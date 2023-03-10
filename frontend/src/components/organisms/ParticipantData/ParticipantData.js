import InputTextField from "../../molecules/InputTextField/InputTextField";
import "./ParticipantData.css";

import ParticipantDataModal from "../../../modals/ParticipantDataModal/ParticipantDataModal";
import { useState } from "react";
import { ActionButton, ActionIconButton } from "../../atoms/Button";
import DeleteOutline from "@mui/icons-material/DeleteOutline";

function ParticipantData({
  onDeleteParticipant,
  participantData,
  sessionId,
  index,
  handleParticipantChange,
}) {
  // I first name and last name of the participant are empty, then we have a newly created participant. The default value is then true.
  const [showParticipantInput, setShowParticipantInput] = useState(
    participantData.first_name === "" && participantData.last_name === ""
  );

  const onAddAdditionalInformation = () => {
    setShowParticipantInput(!showParticipantInput);
  };

  return (
    <div className="participantDataContainer">
      <InputTextField
        title="Participant Name"
        placeholder={"Enter the information"}
        value={[participantData.first_name, participantData.last_name]
          .filter((str) => str.length > 0)
          .join(" ")}
        readonly={true}
      />
      <div className="participantButtons">
        <ActionButton
          text="Enter participant information"
          variant="outlined"
          color="primary"
          size="medium"
          onClick={() => onAddAdditionalInformation()}
        />

        <ActionIconButton
          text=""
          variant="outline"
          color="error"
          size="medium"
          onClick={() => onDeleteParticipant()}
          icon={<DeleteOutline />}
        />
      </div>

      {showParticipantInput && (
        <ParticipantDataModal
          originalParticipant={participantData}
          sessionId={sessionId}
          index={index}
          showParticipantInput={showParticipantInput}
          setShowParticipantInput={setShowParticipantInput}
          handleParticipantChange={handleParticipantChange}
          onDeleteParticipant={onDeleteParticipant}
        />
      )}
    </div>
  );
}

export default ParticipantData;
