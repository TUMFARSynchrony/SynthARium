import { Layer, Stage } from "react-konva";
import { getParticipantById } from "../../../utils/utils";
import { CANVAS_SIZE } from "../../../utils/constants";
import Video from "../../atoms/Video/Video";

function VideoCanvas({ connectedParticipants, sessionData }) {
  return (
    <>
      <Stage width={CANVAS_SIZE.width} height={CANVAS_SIZE.height}>
        <Layer>
          {connectedParticipants?.map((peer, i) => (
            <Video
              key={i}
              src={peer.stream}
              participantData={getParticipantById(peer.summary, sessionData)}
            />
          ))}
        </Layer>
      </Stage>
    </>
  );
}

export default VideoCanvas;
