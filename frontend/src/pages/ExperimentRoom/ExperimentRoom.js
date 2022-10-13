import { useEffect, useState } from "react";
import { Layer, Stage } from "react-konva";
import { useSelector } from "react-redux";
import Video from "../../components/atoms/Video/Video";
import VideoCanvas from "../../components/organisms/VideoCanvas/VideoCanvas";
import { CANVAS_SIZE } from "../../utils/constants";
import { getSessionById } from "../../utils/utils";
import "./ExperimentRoom.css";

function ExperimentRoom({ localStream, connectedParticipants }) {
  const ongoingExperiment = useSelector(
    (state) => state.ongoingExperiment.value
  );
  const state = ongoingExperiment.experimentState;
  const sessionsList = useSelector((state) => state.sessionsList.value);
  const sessionData = getSessionById(
    ongoingExperiment.sessionId,
    sessionsList
  )[0];
  const [participantStream, setParticipantStream] = useState(localStream);
  console.log("connectedParticipants", connectedParticipants);
  console.log("state", state);

  useEffect(() => {
    setParticipantStream(localStream);
  }, [localStream]);

  return (
    <>
      <h1>Experiment Room</h1>
      {state === "WAITING" && participantStream && (
        <Stage width={CANVAS_SIZE.width} height={CANVAS_SIZE.height}>
          <Layer>
            {connectedParticipants?.map((peer, i) => (
              <Video src={localStream} />
            ))}
          </Layer>
        </Stage>
      )}
      {state === "ONGOING" && (
        <VideoCanvas
          connectedParticipants={connectedParticipants}
          sessionData={sessionData}
        />
      )}
    </>
  );
}

export default ExperimentRoom;
