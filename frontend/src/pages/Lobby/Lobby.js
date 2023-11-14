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
  const sessionData = useAppSelector(selectCurrentSession);
  const [participantStream, setParticipantStream] = useState(null);
  const isChatModalActive = useAppSelector(selectChatTab);
  const isInstructionsModalActive = useAppSelector(selectInstructionsTab);
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionIdParam = searchParams.get("sessionId");
  const participantIdParam = searchParams.get("participantId");
  const [areInstructionsChecked, setAreInstructionsChecked] = useState(false);

  useEffect(() => {
    if (connection && connectionState === ConnectionState.CONNECTED) {
      onGetSession(sessionIdParam);
    }
  }, [connection, connectionState, onGetSession, sessionIdParam]);

  const connectedPeersChangeHandler = async (peers) => {
    console.groupCollapsed("%cConnection peer streams change Handler", "color:blue");
    console.groupEnd();
    setConnectedParticipants(peers);
  };

  useEffect(() => {
    if (sessionData && connectedParticipants) {
      // If sessionData and connectedParticipants are available,
      // redirect to the meeting room page
      window.location.href = `/meetingRoom?participantId=${participantIdParam}&sessionId=${sessionIdParam}`;
    }
  }, [sessionData, connectedParticipants, participantIdParam, sessionIdParam]);

  useEffect(() => {
    connection.on("remoteStreamChange", streamChangeHandler);
    connection.on("connectionStateChange", stateChangeHandler);
    connection.on("connectedPeersChange", connectedPeersChangeHandler);
    return () => {
      connection.off("remoteStreamChange", streamChangeHandler);
      connection.off("connectionStateChange", stateChangeHandler);
      connection.off("connectedPeersChange", connectedPeersChangeHandler);
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

  // Determine the href for the "Continue" button based on conditions
  const continueButtonHref =
    !areInstructionsChecked || !sessionData || !connectedParticipants
      ? null
      : `/meetingRoom?participantId=${participantIdParam}&sessionId=${sessionIdParam}`;

  return (
    <>
      <div className="flex h-[calc(100vh-84px)]">
        <div className="px-6 py-4 w-3/4 flex flex-col">
          {participantStream ? (
            <video
              ref={videoElement}
              autoPlay
              playsInline
              width="50%"
              height="auto"
              className="mx-auto" // Center the video horizontally
            ></video>
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
            <InstructionsTab onInstructionsCheckChange={setAreInstructionsChecked} />
          )}
        </div>
      </div>
      <div className="self-center h-fit">
        <a
          href={continueButtonHref}
          className={!areInstructionsChecked ? "pointer-events-none" : ""}
        >
          <ActionButton
            text={
              continueButtonHref ? "Continue" : "Experimenter is waiting to start the experiment"
            }
            variant="contained"
            disabled={!areInstructionsChecked || !continueButtonHref}
          />
        </a>
      </div>
    </>
  );
}

export default Lobby;
