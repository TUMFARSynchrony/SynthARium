import { LinkButton } from "../../components/atoms/Button";
import VideoCanvas from "../../components/organisms/VideoCanvas/VideoCanvas";
import { useAppSelector } from "../../redux/hooks";
import { selectOngoingExperiment } from "../../redux/slices/ongoingExperimentSlice";
import { selectSessions } from "../../redux/slices/sessionsListSlice";
import { getSessionById } from "../../utils/utils";
import { ChatTab } from "../../components/molecules/ChatTab/ChatTab";
import {
  selectChatTab,
  selectInstructionsTab,
  selectParticipantsTab
} from "../../redux/slices/tabsSlice";
import ParticipantsTab from "../../components/molecules/ParticipantsTab/ParticipantsTab";
import { InstructionsTab } from "../../components/molecules/InstructionsTab/InstructionsTab";
import "./WatchingRoom.css";

function WatchingRoom({
  connectedParticipants,
  onKickBanParticipant,
  onChat,
  onGetSession,
  onLeaveExperiment,
  onMuteParticipant
}) {
  const ongoingExperiment = useAppSelector(selectOngoingExperiment);
  const sessionsList = useAppSelector(selectSessions);
  const sessionData = getSessionById(ongoingExperiment.sessionId, sessionsList);
  const isChatModalActive = useAppSelector(selectChatTab);
  const isInstructionsModalActive = useAppSelector(selectInstructionsTab);
  const isParticipantsModalActive = useAppSelector(selectParticipantsTab);

  return (
    <div>
      {sessionData ? (
        <div className="watchingRoom flex justify-between">
          <div className="participantLivestream w-full flex justify-center items-center">
            <div className="videoCanvas">
              <VideoCanvas
                connectedParticipants={connectedParticipants}
                sessionData={sessionData}
              />
              <hr className="separatorLine"></hr>
              <div className="appliedFilters">
                Filters applied on all participants
              </div>
            </div>
          </div>
          {isChatModalActive && (
            <div className="w-1/4">
              <ChatTab
                onChat={onChat}
                onLeaveExperiment={onLeaveExperiment}
                onGetSession={onGetSession}
                currentUser={"experimenter"}
              />
            </div>
          )}
          {isParticipantsModalActive && (
            <div className="w-1/4">
              <ParticipantsTab
                connectedParticipants={connectedParticipants}
                onKickBanParticipant={onKickBanParticipant}
                onMuteParticipant={onMuteParticipant}
              />
            </div>
          )}
          {isInstructionsModalActive && (
            <div className="w-1/4">
              <InstructionsTab />{" "}
            </div>
          )}
        </div>
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
