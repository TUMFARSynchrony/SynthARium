import { useSelector } from "react-redux";
import Heading from "../../components/atoms/Heading/Heading";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";
import VideoCanvas from "../../components/organisms/VideoCanvas/VideoCanvas";
import WatchingRoomTabs from "../../components/organisms/WatchingRoomTabs/WatchingRoomTabs";
import { getSessionById } from "../../utils/utils";
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
  const sessionsList = useSelector((state) => state.sessionsList.value);
  const sessionData = getSessionById(
    ongoingExperiment.sessionId,
    sessionsList
  )[0];

  return (
    <div className="watchingRoomContainer">
      {sessionData ? (
        <>
          <div className="watchingRoomHeader">
            <Heading heading={"State: " + state} />
          </div>
          <div className="watchingRoom">
            <div className="participantLivestream">
              <div className="videoCanvas">
                <VideoCanvas
                  connectedParticipants={connectedParticipants}
                  sessionData={sessionData}
                />
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
        </>
      ) : (
        <div className="noExperimentOngoing">
          <h2>You need to start/join an experiment first.</h2>
          <LinkButton name={"Go to Session Overview"} to="/" />
        </div>
      )}
    </div>
  );
}

export default WatchingRoom;
