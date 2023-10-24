import { ActionButton, LinkActionButton, LinkButton } from "../../components/atoms/Button";
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
import InstructionsTab from "../../components/molecules/InstructionsTab/InstructionsTab";
import "./WatchingRoom.css";
import StartVerificationModal from "../../modals/StartVerificationModal/StartVerificationModal";
import { useState, useEffect } from "react";
import EndVerificationModal from "../../modals/EndVerificationModal/EndVerificationModal";

function WatchingRoom({
  connectedParticipants,
  onKickBanParticipant,
  onChat,
  onGetSession,
  onLeaveExperiment,
  onMuteParticipant,
  onStartExperiment,
  onEndExperiment,
  connection
}) {
  const [startVerificationModal, setStartVerificationModal] = useState(false);
  const [endVerificationModal, setEndVerificationModal] = useState(false);
  const [connectionState, setConnectionState] = useState(null);
  const [responses, setResponses] = useState([]);
  const [highlightedResponse, setHighlightedResponse] = useState(0);
  const ongoingExperiment = useAppSelector(selectOngoingExperiment);
  const sessionsList = useAppSelector(selectSessions);
  const sessionData = getSessionById(ongoingExperiment.sessionId, sessionsList);
  const isChatModalActive = useAppSelector(selectChatTab);
  const isInstructionsModalActive = useAppSelector(selectInstructionsTab);
  const isParticipantsModalActive = useAppSelector(selectParticipantsTab);

  useEffect(() => {
    const recentlyJoinedParticipantId = getRecentlyJoinedParticipantId(connectedParticipants);
    console.log("connec", connection);
    if (recentlyJoinedParticipantId && connection) {
      connection.sendMessage("SET_FILTERS", {
        participant_id: recentlyJoinedParticipantId,
        audio_filters: [],
        video_filters: [
          {
            name: "SIMPLE_GLASSES_DETECTION",
            id: "simple-glasses-detection",
            channel: "video",
            groupFilter: false,
            config: {}
          }
        ]
      });
      console.log("Message send to participant");
    }
  }, [connectedParticipants, connection]);

  const onGetFiltersDataSendToParticipant = (data) => {
    connection.sendMessage("GET_FILTERS_DATA_SEND_TO_PARTICIPANT", data);
    // saveGenericApiResponse("GET_FILTERS_DATA_SEND_TO_PARTICIPANT", data);
  };

  useEffect(() => {
    if (connection && connectedParticipants.length > 0) {
      const data = {
        filter_id: "simple-glasses-detection",
        filter_channel: "video",
        filter_name: "SIMPLE_GLASSES_DETECTION"
      };
      for (let i = 0; i < connectedParticipants.length; i++) {
        const participant_id = connectedParticipants[i].summary;
        data.participant_id = participant_id;
        onGetFiltersDataSendToParticipant(data);
        console.log("Message send to participant", participant_id);
      }
    }
  }, [connection, connectedParticipants]);

  const saveGenericApiResponse = async (endpoint, messageData) => {
    setResponses([{ endpoint, data: messageData }, ...responses]);
    setHighlightedResponse(0);
  };
  const getRecentlyJoinedParticipantId = (connectedParticipants) => {
    if (connectedParticipants.length > 0) {
      const lastParticipant = connectedParticipants[connectedParticipants.length - 1];
      if (lastParticipant && lastParticipant.summary) {
        return lastParticipant.summary;
      }
    }
    return null;
  };
  return (
    <div className="h-[calc(100vh-84px)] w-full">
      {sessionData ? (
        <div className="flex justify-between w-full h-full">
          <div className="w-3/4 h-full flex flex-col justify-center items-center py-6 px-4">
            <div className="h-full w-full">
              <VideoCanvas
                connectedParticipants={connectedParticipants}
                sessionData={sessionData}
                localStream={null}
                ownParticipantId={null}
              />
            </div>
            <div className="py-2 border-gray-300 border-1 rounded-md px-4">
              Filters applied on all participants
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
          <div className="w-1/4">
            {isChatModalActive && (
              <ChatTab
                onChat={onChat}
                onLeaveExperiment={onLeaveExperiment}
                onGetSession={onGetSession}
                currentUser={"experimenter"}
              />
            )}
            {isParticipantsModalActive && (
              <ParticipantsTab
                connectedParticipants={connectedParticipants}
                onKickBanParticipant={onKickBanParticipant}
                onMuteParticipant={onMuteParticipant}
              />
            )}
            {isInstructionsModalActive && <InstructionsTab onInstructionsCheckChange={false} />}
          </div>
        </div>
      ) : (
        <div className="noExperimentOngoing">
          <h2>You need to start/join an experiment first.</h2>
          <LinkButton text="Go to Session Overview" path="/" variant="contained" size="large" />
        </div>
      )}
    </div>
  );
}

export default WatchingRoom;
