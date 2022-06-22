import { useState } from "react";
import JoinedParticipantModal from "../../../modals/JoinedParticipantModal/JoinedParticipantModal";
import KickParticipantModal from "../../../modals/KickParticipantModal/KickParticipantModal";
import Button from "../Button/Button";
import Label from "../Label/Label";
import "./JoinedParticipantCard.css";

function JoinedParticipant({
  participantData,
  sessionId,
  onKickBanParticipant,
}) {
  const [showModal, setShowModal] = useState(false);
  const [showKickBanReason, setShowKickBanReason] = useState(false);
  const [action, setAction] = useState("");

  console.log("participantData", participantData);
  return (
    <div className="joinedParticipantContainer">
      <div className="participantSummary">
        <Label
          title={participantData.first_name + " " + participantData.last_name}
        />
        <Button
          name={"More info"}
          design={"secondary"}
          onClick={() => setShowModal(!showModal)}
        />
        <Button
          name={"Kick"}
          design={"negative"}
          onClick={() => {
            setShowKickBanReason(true);
            setAction("Kick");
          }}
        />
        <Button
          name={"Ban"}
          design={"negative"}
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
          sessionId={sessionId}
        />
      )}
      {showKickBanReason && (
        <KickParticipantModal
          participantData={participantData}
          showModal={showKickBanReason}
          setShowModal={setShowKickBanReason}
          onKickBanParticipant={onKickBanParticipant}
          action={action}
        />
      )}
    </div>
  );
}

export default JoinedParticipant;
