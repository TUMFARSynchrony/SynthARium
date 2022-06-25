import { useState } from "react";
import Heading from "../../components/atoms/Heading/Heading";
import Video from "../../components/atoms/Video/Video";
import WatchingRoomTabs from "../../components/organisms/WatchingRoomTabs/WatchingRoomTabs";
import "./WatchingRoom.css";

function WatchingRoom({
  connectedParticipants,
  onKickBanParticipant,
  onAddNote,
  onLeaveExperiment,
  onMuteParticipant,
}) {
  const [state, setState] = useState("WAITING");
  const onStartExperiment = () => {
    setState("ONGOING");
  };

  const getVideoTitle = (peer, index) => {
    if (peer.summary) {
      return `${peer.summary.first_name} ${peer.summary.last_name}`;
    }
    return `Peer stream ${index + 1}`;
  };

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
                //TODO: map to coordinates
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
          />
        </div>
      </div>
    </div>
  );
}

export default WatchingRoom;
