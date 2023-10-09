import { Layer, Stage } from "react-konva";
import { Session } from "../../../types";
import { getParticipantById } from "../../../utils/utils";
import type { ConnectedPeer } from "../../../networking/typing";
import Video from "../../atoms/Video/Video";
import useMeasure from "react-use-measure";

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
  ownParticipantId: string,
  sessionData: Session
) => {
  if (peer.summary) {
    if (peer.summary instanceof Object) {
      return `${peer.summary.participant_name}`;
    }
    return ` ${getParticipantById(peer.summary, sessionData).participant_name}`;
  }
  return ownParticipantId ? "You" : `Peer stream ${index + 1}`;
};

function VideoCanvas({
  connectedParticipants,
  sessionData,
  ownParticipantId,
  localStream
}: Props) {
  const [ref, bounds] = useMeasure();
  return (
    <div className="h-full w-full" ref={ref}>
      <Stage width={bounds.width} height={bounds.height} className="p-4">
        <Layer>
          {/* Render the video for the participant themselves */}
          {ownParticipantId ? (
            <Video
              key="0"
              src={localStream}
              participantData={getParticipantById(
                ownParticipantId,
                sessionData
              )}
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
                title={getVideoTitle(peer, i, ownParticipantId, sessionData)}
              />
            );
          })}
        </Layer>
      </Stage>
    </div>
  );
}

export default VideoCanvas;
