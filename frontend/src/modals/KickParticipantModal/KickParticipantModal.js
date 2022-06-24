import { useState } from "react";
import { toast } from "react-toastify";
import Button from "../../components/atoms/Button/Button";
import TextAreaField from "../../components/molecules/TextAreaField/TextAreaField";
import "./KickParticipantModal.css";

function KickParticipantModal({
  participantData,
  showModal,
  setShowModal,
  onKickBanParticipant,
  action,
}) {
  const [reason, setReason] = useState("");
  const onChange = (newReason) => {
    setReason(newReason);
  };

  const kickBanParticipant = () => {
    //TODO: where to get participant_id?
    if (!reason) {
      toast.warn("Please specify the reason!");
      return;
    }

    onKickBanParticipant({
      // participant_id: participantData.id,
      participant_id: "0f2f37dad7",
      reason: "lalala",
    });
    setShowModal(!showModal);
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
        <Button name={action} onClick={() => kickBanParticipant()} />
        <Button
          name={"Cancel"}
          design={"negative"}
          onClick={() => setShowModal(false)}
        />
      </div>
    </div>
  );
}

export default KickParticipantModal;
