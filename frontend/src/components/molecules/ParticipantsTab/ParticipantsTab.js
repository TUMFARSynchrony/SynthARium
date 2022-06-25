import Heading from "../../atoms/Heading/Heading";
import JoinedParticipantCard from "../../atoms/JoinedParticipantCard/JoinedParticipantCard";
import { useSelector } from "react-redux";
import "./ParticipantsTab.css";

function ParticipantsTab({
  connectedParticipants,
  onKickBanParticipant,
  onMuteParticipant,
}) {
  const sessionId = useSelector((state) => state.ongoingExperiment.value);

  return (
    <>
      <Heading heading={"Joined participants"} />
      <div className="joinedParticipants">
        {connectedParticipants.length > 0
          ? connectedParticipants.map((participantData, index) => {
              return (
                <JoinedParticipantCard
                  participantData={participantData.summary}
                  key={index}
                  sessionId={sessionId}
                  onKickBanParticipant={onKickBanParticipant}
                  onMuteParticipant={onMuteParticipant}
                />
              );
            })
          : "No participant joined yet."}
      </div>
    </>
  );
}

export default ParticipantsTab;
