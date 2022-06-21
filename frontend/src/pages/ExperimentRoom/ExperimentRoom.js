import { useEffect, useState } from "react";
import Video from "../../components/atoms/Video/Video";
import "./ExperimentRoom.css";

function ExperimentRoom({ localStream }) {
  const [participantStream, setParticipantStream] = useState(localStream);

  useEffect(() => {
    setParticipantStream(localStream);
  }, [localStream]);
  return (
    <>
      <h1>Experiment Room</h1>

      {participantStream && (
        <Video
          title="local stream"
          srcObject={participantStream}
          ignoreAudio={true}
        />
      )}
    </>
  );
}

export default ExperimentRoom;
