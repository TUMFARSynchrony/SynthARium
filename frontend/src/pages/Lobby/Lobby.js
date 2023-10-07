import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import ConsentModal from "../../modals/ConsentModal/ConsentModal";
import ConnectionState from "../../networking/ConnectionState";
import { useAppSelector } from "../../redux/hooks";
import { ChatTab } from "../../components/molecules/ChatTab/ChatTab";
import {
  selectChatTab,
  selectInstructionsTab
} from "../../redux/slices/tabsSlice";
import { InstructionsTab } from "../../components/molecules/InstructionsTab/InstructionsTab";

function Lobby({
  localStream,
  connection,
  connectionState,
  onGetSession,
  onChat
}) {
  const videoElement = useRef(null);
  const [participantStream, setParticipantStream] = useState(localStream);
  const isChatModalActive = useAppSelector(selectChatTab);
  const isInstructionsModalActive = useAppSelector(selectInstructionsTab);
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionIdParam = searchParams.get("sessionId");
  const participantIdParam = searchParams.get("participantId");
  console.log(sessionIdParam);

  useEffect(() => {
    if (connection && connectionState === ConnectionState.CONNECTED) {
      onGetSession(sessionIdParam);
    }
  }, [connection, connectionState, sessionIdParam]);

  useEffect(() => {
    setParticipantStream(localStream);
  }, [localStream]);

  useEffect(() => {
    if (participantStream) {
      videoElement.current.srcObject = localStream;
    }
  }, [participantStream]);

  return (
    <>
      <ConsentModal />
      {/* Grid takes up screen space left from the AppToolbar */}
      <div className="flex h-[calc(100vh-84px]]">
        <Paper
          elevation={2}
          sx={{ backgroundColor: "whitesmoke", height: "100%", width: "75%" }}
        >
          {participantStream ? (
            // Displaying local stream of participant
            <video
              ref={videoElement}
              autoPlay
              playsInline
              width="100%"
              height="100%"
            ></video>
          ) : (
            <Typography>
              Unable to access your video. Please check that you have allowed
              access to your camera and microphone.
            </Typography>
          )}
        </Paper>
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

export default Lobby;
