import { Layer, Stage } from "react-konva";
import { Session } from "../../../types";
import { CANVAS_SIZE } from "../../../utils/constants";
import { getParticipantById } from "../../../utils/utils";
import type { ConnectedPeer } from "../../../networking/typing";
import Video from "../../atoms/Video/Video";

type Props = {
  connectedParticipants: any;
  sessionData: Session;
  localStream?: any;
  ownParticipantId?: string; // Add a prop for the participant's own ID
};

/** Get the title displayed in a {@link Video} element for `peer`. */
const getVideoTitle = (
  peer: ConnectedPeer,
  index: number,
  ownParticipantId: string
) => {
  if (peer.summary) {
    if (peer.summary instanceof Object) {
      return `${peer.summary.participant_name}`;
    }
    return `UserID: ${peer.summary}`;
  }
  return ownParticipantId ? "You" : `Peer stream ${index + 1}`;
};

function VideoCanvas({
  connectedParticipants,
  sessionData,
  ownParticipantId,
  localStream
}: Props) {
  return (
    <Stage width={CANVAS_SIZE.width} height={CANVAS_SIZE.height}>
      <Layer>
        {/* Render the video for the participant themselves */}
        {ownParticipantId ? (
          <Video
            key="0"
            src={localStream}
            participantData={getParticipantById(ownParticipantId, sessionData)}
            title="You"
          />
        ) : null}
        {/* Render videos for other connected participants */}
        {connectedParticipants?.map((peer: any, i: number) => {
          if (peer.id === ownParticipantId) {
            return null; // Skip rendering the participant's own video again
          }
          const participantData =
            typeof peer.summary === "string"
              ? getParticipantById(peer.summary, sessionData)
              : peer.summary;

          return (
            <Video
              key={i}
              src={peer.stream}
              participantData={participantData}
              title={getVideoTitle(peer, i, ownParticipantId)}
            />
          );
        })}
      </Layer>
    </Stage>
  );
}

export default VideoCanvas;
