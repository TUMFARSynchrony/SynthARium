import Heading from "../../atoms/Heading/Heading";
import { getJoinedParticipants } from "../../../utils/mockServer";
import { useState } from "react";
import JoinedParticipantCard from "../../atoms/JoinedParticipantCard/JoinedParticipantCard";
import { useSelector } from "react-redux";

function ParticipantsTab() {
  const [participants, setParticipants] = useState(getJoinedParticipants());
  const sessionData = useSelector((state) => state.ongoingExperiment.value);

  return (
    <>
      <Heading heading={"Joined participants"} />
      {participants.length > 0
        ? participants.map((participantData, index) => {
            return (
              <JoinedParticipantCard
                participantData={participantData}
                key={index}
                sessionId={sessionData.id}
              />
            );
          })
        : "No participant joined yet."}
    </>
  );
}

export default ParticipantsTab;
