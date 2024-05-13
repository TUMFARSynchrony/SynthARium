import Typography from "@mui/material/Typography";
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import VideoCanvas from "../../components/organisms/VideoCanvas/VideoCanvas";
import ConnectionState from "../../networking/ConnectionState";
import { useAppSelector } from "../../redux/hooks";
import { selectCurrentSession } from "../../redux/slices/sessionsListSlice";
import {
  selectChatGptTab,
  selectChatTab,
  selectInstructionsTab
} from "../../redux/slices/tabsSlice";
import { InstructionsTab } from "../../components/molecules/InstructionsTab/InstructionsTab";
import "./Lobby.css";
import { ParticipantChatTab } from "../../components/molecules/ChatTab/ParticipantChatTab";
import { ChatGptTab } from "../../components/molecules/ChatGptTab/ChatGptTab";

function Lobby({ localStream, connection, onGetSession, onChat }) {
  const videoElement = useRef(null);
  const [connectionState, setConnectionState] = useState(null);
  const [connectedParticipants, setConnectedParticipants] = useState([]);
  const sessionData = useAppSelector(selectCurrentSession);
  const [participantStream, setParticipantStream] = useState(null);
  const isChatModalActive = useAppSelector(selectChatTab);
  const isInstructionsModalActive = useAppSelector(selectInstructionsTab);
  const isChatGptModalActive = useAppSelector(selectChatGptTab);
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionIdParam = searchParams.get("sessionId");
  const participantIdParam = searchParams.get("participantId");

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
    connection.on("remoteStreamChange", streamChangeHandler);
    connection.on("connectionStateChange", stateChangeHandler);
    connection.on("connectedPeersChange", connectedPeersChangeHandler);
    return () => {
      // Remove event handlers when component is deconstructed
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
      videoElement.current.muted = true;
    }
  }, [localStream, participantStream]);

  const streamChangeHandler = async () => {
    console.log("%cRemote Stream Change Handler", "color:blue");
  };
  /** Handle `connectionStateChange` event of {@link Connection} */
  const stateChangeHandler = async (state) => {
    setConnectionState(state);
  };

  return (
    <>
      {/* Grid takes up screen space left from the AppToolbar */}
      <div className="flex h-[calc(100vh-84px)]">
        <div className="px-6 py-4 w-3/4 flex flex-col"></div>
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
        <div className="w-1/4">
          {connectionState !== ConnectionState.CONNECTED && <div>Trying to connect...</div>}
          {connectionState === ConnectionState.CONNECTED && isChatModalActive && (
            <ParticipantChatTab
              onChat={onChat}
              onGetSession={onGetSession}
              currentUser="participant"
              participantId={participantIdParam}
            />
          )}

          {connectionState === ConnectionState.CONNECTED && isInstructionsModalActive && (
            <InstructionsTab />
          )}

          {connectionState === ConnectionState.CONNECTED && isChatGptModalActive && <ChatGptTab />}
        </div>
      </div>
    </>
  );
}

export default Lobby;
