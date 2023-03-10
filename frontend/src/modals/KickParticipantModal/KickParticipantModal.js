import { useState } from "react";
import { useDispatch } from "react-redux";
import { toast } from "react-toastify";
import { ActionButton } from "../../components/atoms/Button";
import TextAreaField from "../../components/molecules/TextAreaField/TextAreaField";
import { banMuteUnmuteParticipant } from "../../features/sessionsList";
import "./KickParticipantModal.css";

function KickParticipantModal({
  participantId,
  sessionId,
  showModal,
  setShowModal,
  onKickBanParticipant,
  action,
}) {
  const [reason, setReason] = useState("");
  const dispatch = useDispatch();

  const onChange = (newReason) => {
    setReason(newReason);
  };

  const kickBanParticipant = () => {
    if (!reason) {
      toast.warn("Please specify the reason!");
      return;
    }

    onKickBanParticipant(
      {
        participant_id: participantId,
        reason: reason,
      },
      action
    );
    setShowModal(!showModal);

    if (action === "Ban") {
      dispatch(
        banMuteUnmuteParticipant({
          participantId: participantId,
          action: "banned",
          value: true,
          sessionId: sessionId,
        })
      );
    }
  };

  return (
    <div className="kickParticipantModalContainer">
      <div className="kickParticipantModal">
        <TextAreaField
          title={`Enter your reason for kicking/banning here:`}
          value={reason}
          onChange={(newReason) => onChange(newReason)}
          required={true}
        />
        <ActionButton variant="contained" color="error" size="medium" text={action} onClick={() => kickBanParticipant()} />
        <ActionButton
          text="Cancel"
          variant="contained"
          color="primary"
          size="medium"
          onClick={() => setShowModal(false)}
        />
      </div>
    </div>
  );
}

export default KickParticipantModal;
