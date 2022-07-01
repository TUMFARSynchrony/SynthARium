import { useSelector } from "react-redux";
import Heading from "../../components/atoms/Heading/Heading";
import Video from "../../components/atoms/Video/Video";
import WatchingRoomTabs from "../../components/organisms/WatchingRoomTabs/WatchingRoomTabs";
import { getVideoTitle } from "../../utils/utils";
import "./WatchingRoom.css";

function WatchingRoom({
  connectedParticipants,
  onKickBanParticipant,
  onAddNote,
  onLeaveExperiment,
  onMuteParticipant,
  onStartExperiment,
  onEndExperiment,
  onSendChat,
}) {
  const ongoingExperiment = useSelector(
    (state) => state.ongoingExperiment.value
  );
  const state = ongoingExperiment.experimentState;

  return (
    <div className="watchingRoomContainer">
      <div className="watchingRoomHeader">
        <Heading heading={"State: " + state} />
      </div>
      <div className="watchingRoom">
        <div className="participantLivestream">
          <div className="livestream">
            <div className="connectedParticipants">
              {connectedParticipants.map((peer, i) => (
                <Video
                  title={getVideoTitle(peer, i)}
                  srcObject={peer.stream}
                  key={i}
                />
              ))}
            </div>
          </div>
          <hr className="separatorLine"></hr>
          <div className="applieadFilters">
            Filters applied on all participants
          </div>
        </div>
        <div className="watchingRoomTabs">
          <WatchingRoomTabs
            connectedParticipants={connectedParticipants}
            onKickBanParticipant={onKickBanParticipant}
            onAddNote={onAddNote}
            onLeaveExperiment={onLeaveExperiment}
            onStartExperiment={onStartExperiment}
            onMuteParticipant={onMuteParticipant}
            onEndExperiment={onEndExperiment}
            onSendChat={onSendChat}
          />
        </div>
      </div>
    </div>
  );
}

export default WatchingRoom;
