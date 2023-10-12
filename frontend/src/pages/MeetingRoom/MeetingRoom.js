import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import VideoCanvas from "../../components/organisms/VideoCanvas/VideoCanvas";
import ConnectionState from "../../networking/ConnectionState";
import { useAppSelector } from "../../redux/hooks";
import { selectCurrentSession } from "../../redux/slices/sessionsListSlice";
import { ChatTab } from "../../components/molecules/ChatTab/ChatTab";
import {
  selectChatTab,
  selectInstructionsTab
} from "../../redux/slices/tabsSlice";
import { InstructionsTab } from "../../components/molecules/InstructionsTab/InstructionsTab";
import "./Lobby.css";

function MeetingRoom({ localStream, connection, onGetSession, onChat }) {
  const [connectionState, setConnectionState] = useState(null);
  const [connectedParticipants, setConnectedParticipants] = useState([]);
  const sessionData = useAppSelector(selectCurrentSession);
  const isChatModalActive = useAppSelector(selectChatTab);
  const isInstructionsModalActive = useAppSelector(selectInstructionsTab);
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionIdParam = searchParams.get("sessionId");
  const participantIdParam = searchParams.get("participantId");
  useEffect(() => {
    if (connection && connectionState === ConnectionState.CONNECTED) {
      onGetSession(sessionIdParam);
    }
  }, [connection, connectionState, onGetSession, sessionIdParam]);
  const connectedPeersChangeHandler = async (peers) => {
    console.groupCollapsed(
      "%cConnection peer streams change Handler",
      "color:blue"
    );
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

  const streamChangeHandler = async () => {
    console.log("%cRemote Stream Change Handler", "color:blue");
  };
  /** Handle `connectionStateChange` event of {@link Connection} */
  const stateChangeHandler = async (state) => {
    setConnectionState(state);
  };

  return (
    <>
      <div className="flex h-[calc(100vh-84px)]">
        <div className="px-6 py-4 w-3/4 flex flex-col">
          <VideoCanvas
            connectedParticipants={connectedParticipants}
            sessionData={sessionData}
            localStream={localStream}
            ownParticipantId={participantIdParam}
          />
        </div>
        <div className="w-1/4">
          {connectionState !== ConnectionState.CONNECTED && (
            <div>Trying to connect...</div>
          )}
          {connectionState === ConnectionState.CONNECTED &&
            isChatModalActive && (
              <ChatTab
                onChat={onChat}
                onGetSession={onGetSession}
                currentUser="participant"
                participantId={participantIdParam}
              />
            )}

          {connectionState === ConnectionState.CONNECTED &&
            isInstructionsModalActive && <InstructionsTab />}
        </div>
      </div>
    </>
  );
}

export default MeetingRoom;
