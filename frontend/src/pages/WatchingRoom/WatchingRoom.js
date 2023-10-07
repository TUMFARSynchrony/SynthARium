import {
  ActionButton,
  LinkActionButton,
  LinkButton
} from "../../components/atoms/Button";
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
import StartVerificationModal from "../../modals/StartVerificationModal/StartVerificationModal";
import { useState } from "react";
import EndVerificationModal from "../../modals/EndVerificationModal/EndVerificationModal";

function WatchingRoom({
  connectedParticipants,
  onKickBanParticipant,
  onChat,
  onGetSession,
  onLeaveExperiment,
  onMuteParticipant,
  onStartExperiment,
  onEndExperiment
}) {
  const [startVerificationModal, setStartVerificationModal] = useState(false);
  const [endVerificationModal, setEndVerificationModal] = useState(false);
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
          <div className="participantLivestream w-3/4 flex flex-col justify-center px-6">
            <div className="videoCanvas">
              <VideoCanvas
                connectedParticipants={connectedParticipants}
                sessionData={sessionData}
                localStream={null}
                ownParticipantId={null}
              />
              <hr className="separatorLine"></hr>
              <div className="appliedFilters">
                Filters applied on all participants
              </div>
            </div>
            <div className="flex flex-row justify-center gap-x-4 pt-5">
              <LinkActionButton
                text="LEAVE EXPERIMENT"
                variant="outlined"
                path="/"
                size="large"
                color="primary"
                onClick={() => onLeaveExperiment()}
              />
              {sessionData.start_time === 0 ? (
                <ActionButton
                  text="START EXPERIMENT"
                  variant="contained"
                  color="success"
                  size="large"
                  onClick={() => {
                    setStartVerificationModal(true);
                  }}
                />
              ) : (
                <ActionButton
                  text="END EXPERIMENT"
                  variant="contained"
                  color="error"
                  size="large"
                  onClick={() => {
                    setEndVerificationModal(true);
                  }}
                />
              )}

              {startVerificationModal && (
                <StartVerificationModal
                  setShowModal={setStartVerificationModal}
                  onStartExperiment={onStartExperiment}
                />
              )}

              {endVerificationModal && (
                <EndVerificationModal
                  setShowModal={setEndVerificationModal}
                  onEndExperiment={onEndExperiment}
                />
              )}
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
