import Heading from "../../atoms/Heading/Heading";
import JoinedParticipantCard from "../../atoms/JoinedParticipantCard/JoinedParticipantCard";
import { useSelector } from "react-redux";
import "./ParticipantsTab.css";
import { getSessionById } from "../../../utils/utils";

function ParticipantsTab({
  connectedParticipants,
  onKickBanParticipant,
  onMuteParticipant,
  onSendChat,
}) {
  const ongoingExperiment = useSelector(
    (state) => state.ongoingExperiment.value
  );
  const sessionId = ongoingExperiment.sessionId;
  const sessionsList = useSelector((state) => state.sessionsList.value);
  const sessionData = getSessionById(sessionId, sessionsList)[0];

  return (
    <>
      <Heading heading={"Joined participants"} />
      <div className="joinedParticipants">
        {connectedParticipants.length > 0
          ? connectedParticipants.map((participant, index) => {
              return (
                <JoinedParticipantCard
                  participantId={participant.summary}
                  key={index}
                  sessionData={sessionData}
                  onKickBanParticipant={onKickBanParticipant}
                  onMuteParticipant={onMuteParticipant}
                  onSendChat={onSendChat}
                />
              );
            })
          : "No participants joined yet."}
      </div>
    </>
  );
}

export default ParticipantsTab;
