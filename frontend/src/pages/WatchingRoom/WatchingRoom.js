import { LinkButton } from "../../components/atoms/Button";
import Heading from "../../components/atoms/Heading/Heading";
import VideoCanvas from "../../components/organisms/VideoCanvas/VideoCanvas";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { selectOngoingExperiment } from "../../redux/slices/ongoingExperimentSlice";
import { selectSessions } from "../../redux/slices/sessionsListSlice";
import { getSessionById } from "../../utils/utils";
import "./WatchingRoom.css";
import { IconButton } from "../../components/atoms/Button/IconButton";
import { HiOutlineChatAlt2 } from "react-icons/hi";
import { BiTask } from "react-icons/bi";
import { HiOutlineUsers } from "react-icons/hi2";
import { ChatTab } from "../../components/molecules/ChatTab/ChatTab";
import {
  selectChatTab,
  selectInstructionsTab,
  selectParticipantsTab,
  toggleSingleTab
} from "../../redux/slices/tabsSlice";
import { Tabs } from "../../utils/enums";
import ParticipantsTab from "../../components/molecules/ParticipantsTab/ParticipantsTab";
import { InstructionsTab } from "../../components/molecules/InstructionsTab/InstructionsTab";

function WatchingRoom({
  connectedParticipants,
  onKickBanParticipant,
  onChat,
  onGetSession,
  onLeaveExperiment,
  onMuteParticipant
}) {
  const dispatch = useAppDispatch();
  const ongoingExperiment = useAppSelector(selectOngoingExperiment);
  const state = ongoingExperiment.experimentState;
  const sessionsList = useAppSelector(selectSessions);
  const sessionData = getSessionById(ongoingExperiment.sessionId, sessionsList);
  const isChatModalActive = useAppSelector(selectChatTab);
  const isInstructionsModalActive = useAppSelector(selectInstructionsTab);
  const isParticipantsModalActive = useAppSelector(selectParticipantsTab);

  const toggleModal = (modal) => {
    dispatch(toggleSingleTab(modal));
  };
  return (
    <div>
      {sessionData ? (
        <>
          <div className="watchingRoomHeader flex flex-row justify-between items-center h-16 px-6">
            <Heading heading={"State: " + state} />{" "}
            <div className="flex flex-row space-x-4">
              <IconButton
                icon={HiOutlineChatAlt2}
                size={24}
                onToggle={() => toggleModal(Tabs.CHAT)}
              />
              <IconButton
                icon={BiTask}
                size={24}
                onToggle={() => toggleModal(Tabs.INSTRUCTIONS)}
              />
              <IconButton
                icon={HiOutlineUsers}
                size={24}
                onToggle={() => toggleModal(Tabs.PARTICIPANTS)}
              />
            </div>
          </div>
          <div className="flex flex-row h-[calc(100vh-4rem)]">
            <div className="flex flex-row w-3/4">
              <div className="participantLivestream p-6">
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
