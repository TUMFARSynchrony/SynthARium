import { Layer, Stage } from "react-konva";
import { Session } from "../../../types";
import { getParticipantById } from "../../../utils/utils";
import Video from "../../atoms/Video/Video";
import useMeasure from "react-use-measure";

type Props = {
  connectedParticipants: any;
  sessionData: Session;
};

function VideoCanvas({ connectedParticipants, sessionData }: Props) {
  const [ref, bounds] = useMeasure();
  return (
    <div className="h-full w-full" ref={ref}>
      <Stage width={bounds.width} height={bounds.height}>
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
    </div>
  );
}

export default VideoCanvas;
