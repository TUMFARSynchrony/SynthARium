import { useState } from "react";
import JoinedParticipantModal from "../../../modals/JoinedParticipantModal/JoinedParticipantModal";
import KickParticipantModal from "../../../modals/KickParticipantModal/KickParticipantModal";
import { getParticipantById } from "../../../utils/utils";
import Button from "../Button/Button";
import Label from "../Label/Label";
import "./JoinedParticipantCard.css";

function JoinedParticipant({
  participantId,
  sessionData,
  onKickBanParticipant,
  onMuteParticipant,
}) {
  const [showModal, setShowModal] = useState(false);
  const [showKickBanReason, setShowKickBanReason] = useState(false);
  const [action, setAction] = useState("");
  const participantData = getParticipantById(participantId, sessionData);

  return (
    <div className="joinedParticipantContainer">
      <div className="participantSummary">
        <Label
          title={participantData.first_name + " " + participantData.last_name}
        />
        <Button
          name={"Info"}
          design={"small-secondary"}
          onClick={() => setShowModal(!showModal)}
        />
        <Button
          name={"Kick"}
          design={"small-negative"}
          onClick={() => {
            setShowKickBanReason(true);
            setAction("Kick");
          }}
        />
        <Button
          name={"Ban"}
          design={"small-negative"}
          onClick={() => {
            setShowKickBanReason(true);
            setAction("Ban");
          }}
        />
      </div>
      {showModal && (
        <JoinedParticipantModal
          participantData={participantData}
          showModal={showModal}
          setShowModal={setShowModal}
          sessionId={sessionData.id}
          onMuteParticipant={onMuteParticipant}
        />
      )}
      {showKickBanReason && (
        <KickParticipantModal
          participantId={participantData.id}
          showModal={showKickBanReason}
          setShowModal={setShowKickBanReason}
          onKickBanParticipant={onKickBanParticipant}
          action={action}
          sessionId={sessionData.id}
        />
      )}
    </div>
  );
}

export default JoinedParticipant;
