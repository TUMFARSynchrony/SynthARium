import Typography from "@mui/material/Typography";
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import ConnectionState from "../../networking/ConnectionState";
import { useAppSelector } from "../../redux/hooks";
import { selectCurrentSession } from "../../redux/slices/sessionsListSlice";
import { ChatTab } from "../../components/molecules/ChatTab/ChatTab";
import { selectChatTab, selectInstructionsTab } from "../../redux/slices/tabsSlice";
import InstructionsTab from "../../components/molecules/InstructionsTab/InstructionsTab";
import { ActionButton } from "../../components/atoms/Button";

function Lobby({ localStream, connection, onGetSession, onChat }) {
  const videoElement = useRef(null);
  const [connectionState, setConnectionState] = useState(null);
  const [connectedParticipants, setConnectedParticipants] = useState([]);
  const [responses, setResponses] = useState([]);
  const [highlightedResponse, setHighlightedResponse] = useState(0);
  const sessionData = useAppSelector(selectCurrentSession);
  const [participantStream, setParticipantStream] = useState(null);
  const isChatModalActive = useAppSelector(selectChatTab);
  const isInstructionsModalActive = useAppSelector(selectInstructionsTab);
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionIdParam = searchParams.get("sessionId");
  const participantIdParam = searchParams.get("participantId");
  const [areInstructionsChecked, setAreInstructionsChecked] = useState(false); // State to track checkbox status

  useEffect(() => {
    if (connection && connectionState === ConnectionState.CONNECTED) {
      onGetSession(sessionIdParam);
      if (participantStream && videoElement.current) {
        connection.sendMessage("GET_FILTERS_DATA_SEND_TO_PARTICIPANT", {
          participant_id: "all",
          filter_id: "simple-glasses-detection",
          filter_channel: "video",
          filter_name: "SIMPLE_GLASSES_DETECTION"
        });
        console.log("message sent");
      }
    }
  }, [connection, connectionState, onGetSession, sessionIdParam]);

  const handleGetFiltersDataSendToParticipant = (data) => {
    saveGenericApiResponse("GET_FILTERS_DATA_SEND_TO_PARTICIPANT", data);
    console.log("handleGetFiltersDataSendToParticipant", data);
  };
  const saveGenericApiResponse = async (endpoint, messageData) => {
    setResponses([{ endpoint, data: messageData }, ...responses]);
    setHighlightedResponse(0);
  };
  useEffect(() => {
    connection.on("remoteStreamChange", streamChangeHandler);
    connection.on("connectionStateChange", stateChangeHandler);
    connection.api.on(
      "GET_FILTERS_DATA_SEND_TO_PARTICIPANT",
      handleGetFiltersDataSendToParticipant
    );
    return () => {
      // Remove event handlers when component is deconstructed
      connection.off("remoteStreamChange", streamChangeHandler);
      connection.off("connectionStateChange", stateChangeHandler);
      connection.api.off(
        "GET_FILTERS_DATA_SEND_TO_PARTICIPANT",
        handleGetFiltersDataSendToParticipant
      );
    };
  }, [connection]);

  useEffect(() => {
    setParticipantStream(localStream);
  }, [localStream]);

  useEffect(() => {
    if (participantStream && videoElement.current) {
      videoElement.current.srcObject = localStream;
    }
  }, [localStream, participantStream]);

  const streamChangeHandler = async () => {
    console.log("%cRemote Stream Change Handler", "color:blue");
  };

  const stateChangeHandler = async (state) => {
    setConnectionState(state);
  };

  return (
    <>
      <div className="flex h-[calc(100vh-84px)]">
        <div className="px-6 py-4 w-3/4 flex flex-col">
          {participantStream ? (
            <div className="flex h-full justify-center gap-y-4 xl:w-1/2">
              <video ref={videoElement} autoPlay playsInline width="100%" height="100%"></video>
            </div>
          ) : (
            <Typography>
              Unable to access your video. Please check that you have allowed access to your camera
              and microphone.
            </Typography>
          )}
        </div>
        <div className="w-1/4">
          {connectionState !== ConnectionState.CONNECTED && <div>Trying to connect...</div>}
          {connectionState === ConnectionState.CONNECTED && isChatModalActive && (
            <ChatTab
              onChat={onChat}
              onGetSession={onGetSession}
              currentUser="participant"
              participantId={participantIdParam}
            />
          )}

          {connectionState === ConnectionState.CONNECTED && isInstructionsModalActive && (
            <InstructionsTab
              onInstructionsCheckChange={setAreInstructionsChecked}
              connection={connection}
            />
          )}
        </div>
      </div>
      <div className="self-center h-fit">
        <a
          href={`${window.location.origin}/meetingRoom?participantId=${participantIdParam}&sessionId=${sessionIdParam}`}
          className={!areInstructionsChecked ? "pointer-events-none" : ""}
        >
          <ActionButton text="Continue" variant="contained" disabled={!areInstructionsChecked} />
        </a>
      </div>
    </>
  );
}

export default Lobby;
