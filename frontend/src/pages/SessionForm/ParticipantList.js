import React from "react";
import Typography from "@mui/material/Typography";
import ParticipantData from "../../components/organisms/ParticipantData/ParticipantData";
import ActionIconButton from "../../components/atoms/Button/ActionIconButton";
import AddIcon from "@mui/icons-material/Add";

function ParticipantList({
  openSession,
  onAddParticipant,
  onDeleteParticipant,
  handleParticipantChange,
  setSnackbarResponse,
  handleCanvasPlacement,
  sessionData
}) {
  return (
    <div>
      <div className="flex">
        <Typography variant="h6" sx={{ my: 1, fontWeight: "bold" }}>
          Participant List
        </Typography>
        <ActionIconButton
          text="ADD"
          variant="outlined"
          color="primary"
          size="small"
          onClick={onAddParticipant}
          icon={<AddIcon />}
        />
      </div>
      <div className="overflow-y-auto h-[300px] shadow-lg bg-slate-50 pl-4 py-2">
        {openSession.participants.map((participant, index) => (
          <ParticipantData
            onDeleteParticipant={() => onDeleteParticipant(index)}
            key={index}
            index={index}
            participantData={participant}
            sessionId={sessionData.id}
            handleParticipantChange={handleParticipantChange}
            setSnackbarResponse={setSnackbarResponse}
            handleCanvasPlacement={handleCanvasPlacement}
          />
        ))}
      </div>
    </div>
  );
}

export default ParticipantList;
