import { useEffect, useState } from "react";
import { Layer, Stage } from "react-konva";
import { useSelector } from "react-redux";
import Video from "../../components/atoms/Video/Video";
import { CANVAS_SIZE } from "../../utils/constants";
import "./ExperimentRoom.css";

function ExperimentRoom({ localStream, connection }) {
  const [participantStream, setParticipantStream] = useState(localStream);
  const [participantVideoData, setParticipantVideoData] = useState();

  useEffect(() => {
    setParticipantStream(localStream);
  }, [localStream]);

  useEffect(() => {
    let participantData = {
      size: {
        width: CANVAS_SIZE.width,
        height: CANVAS_SIZE.height
      },
      position: {
        x: 0,
        y: 0
      }
    }

    setParticipantVideoData(participantData);
  }, [])

  return (
    <>
      <h1>Experiment Room</h1>
      {participantStream && connection.participantSummary && (
        <Stage width={CANVAS_SIZE.width} height={CANVAS_SIZE.height}>
          <Layer>
            <Video
              src={participantStream}
              participantData={participantVideoData}
            />
          </Layer>
        </Stage>
      )}
    </>
  );
}

export default ExperimentRoom;
