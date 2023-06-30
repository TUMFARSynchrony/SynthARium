import { Layer, Stage } from "react-konva";
import { Session } from "../../../types";
import { CANVAS_SIZE } from "../../../utils/constants";
import Video from "../../atoms/Video/Video";
import { getParticipantById } from "../../../utils/utils";

type Props = {
  connectedParticipants: any;
  sessionData: Session;
};

function VideoCanvas({ connectedParticipants, sessionData }: Props) {
  return (
    <Stage width={CANVAS_SIZE.width} height={CANVAS_SIZE.height}>
      <Layer>
        {connectedParticipants?.map((peer: any, i: number) => (
          <Video
            key={i}
            src={peer.stream}
            participantData={getParticipantById(peer.summary, sessionData)}
          />
        ))}
      </Layer>
    </Stage>
  );
}

export default VideoCanvas;
