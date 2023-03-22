import ParticipantDataModal from "../../../modals/ParticipantDataModal/ParticipantDataModal";
import { useState } from "react";
import { ActionIconButton } from "../../atoms/Button";
import DeleteOutline from "@mui/icons-material/DeleteOutline";
import EditOutlined from "@mui/icons-material/EditOutlined";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";

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
    <>
      <Box sx={{ display: "flex", justifyContent: "flex-start", mb: 1 }}>
        <TextField
          label="Participant Name"
          value={[participantData.first_name, participantData.last_name]
            .filter((str) => str.length > 0)
            .join(" ")}
          inputProps={{ readOnly: true }}
          size="small"
          sx={{ marginTop: '5px' }}
        />
        <ActionIconButton text="EDIT" variant="outlined" color="primary" size="medium" onClick={() => onAddAdditionalInformation()} icon={<EditOutlined />} />
        <ActionIconButton text="DELETE" variant="outlined" color="error" size="medium" onClick={() => onDeleteParticipant()} icon={<DeleteOutline />} />
      </Box>

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
    </>
  );
}

export default ParticipantData;
