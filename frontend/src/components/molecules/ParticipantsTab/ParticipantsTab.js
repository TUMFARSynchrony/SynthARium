import "./ParticipantsTab.css";
import Heading from "../../atoms/Heading/Heading";
import { getJoinedParticipants } from "../../../utils/mockServer";
import { useState } from "react";
import JoinedParticipantCard from "../../atoms/JoinedParticipantCard/JoinedParticipantCard";

function ParticipantsTab() {
  const [participants, setParticipants] = useState(getJoinedParticipants());

  return (
    <div className="participantsTabContainer">
      <Heading heading={"Joined participants"} />
      <div className="joinedParticipants">
        {participants.length > 0
          ? participants.map((participantData, index) => {
              return (
                <JoinedParticipantCard
                  participantData={participantData}
                  key={index}
                />
              );
            })
          : "No participant joined yet."}
      </div>
    </div>
  );
}

export default ParticipantsTab;
