import { LinkButton } from "../../components/atoms/Button";
import Heading from "../../components/atoms/Heading/Heading";
import VideoCanvas from "../../components/organisms/VideoCanvas/VideoCanvas";
import WatchingRoomTabs from "../../components/organisms/WatchingRoomTabs/WatchingRoomTabs";
import { useAppSelector } from "../../redux/hooks";
import { selectOngoingExperiment } from "../../redux/slices/ongoingExperimentSlice";
import { selectSessions } from "../../redux/slices/sessionsListSlice";
import { getSessionById } from "../../utils/utils";
import "./WatchingRoom.css";

function WatchingRoom({
  connectedParticipants,
  onKickBanParticipant,
  onChat,
  onGetSession,
  onAddNote,
  onLeaveExperiment,
  onMuteParticipant,
  onStartExperiment,
  onEndExperiment
}) {
  const ongoingExperiment = useAppSelector(selectOngoingExperiment);
  const state = ongoingExperiment.experimentState;
  const sessionsList = useAppSelector(selectSessions);
  const sessionData = getSessionById(ongoingExperiment.sessionId, sessionsList);

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
              <div className="appliedFilters">
                Filters applied on all participants
              </div>
            </div>
            <div className="watchingRoomTabs">
              <WatchingRoomTabs
                connectedParticipants={connectedParticipants}
                onKickBanParticipant={onKickBanParticipant}
                onAddNote={onAddNote}
                onChat={onChat}
                onGetSession={onGetSession}
                onLeaveExperiment={onLeaveExperiment}
                onStartExperiment={onStartExperiment}
                onMuteParticipant={onMuteParticipant}
                onEndExperiment={onEndExperiment}
              />
            </div>
          </div>
        </>
      ) : (
        <div className="noExperimentOngoing">
          <h2>You need to start/join an experiment first.</h2>
          <LinkButton
            text="Go to Session Overview"
            path="/"
            variant="contained"
            size="large"
          />
        </div>
      )}
    </div>
  );
}

export default WatchingRoom;
