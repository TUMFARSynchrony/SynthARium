import { useEffect, useState } from "react";
import { Layer, Stage } from "react-konva";
import { useSelector } from "react-redux";
import Video from "../../components/atoms/Video/Video";
import VideoCanvas from "../../components/organisms/VideoCanvas/VideoCanvas";
import { CANVAS_SIZE } from "../../utils/constants";
import { getSessionById, getParticipantById } from "../../utils/utils";
import "./ExperimentRoom.css";

function ExperimentRoom({ localStream, onJoinExperimentParticipant, connection }) {
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

  useEffect(() => {
    setParticipantStream(localStream);
    onJoinExperimentParticipant();
  }, [localStream]);

  return (
    <>
      <h1>Experiment Room</h1>
      {state === "WAITING" && participantStream && connection.participantSummary && (
        <Stage width={CANVAS_SIZE.width} height={CANVAS_SIZE.height}>
          <Layer>
            <Video
              src={participantStream}
              participantData={connection.participantSummary}
            />
          </Layer>
        </Stage>
      )}
      {state === "ONGOING" && (
        // TODO: Redirect to watching room when experiment state is ONGOING
        <p>Redirect to watching room please.</p>
      )}
    </>
  );
}

export default ExperimentRoom;
