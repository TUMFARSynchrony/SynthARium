import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import ConsentModal from "../../modals/ConsentModal/ConsentModal";
import ConnectionState from "../../networking/ConnectionState";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { ChatTab } from "../../components/molecules/ChatTab/ChatTab";
import Heading from "../../components/atoms/Heading/Heading";
import { IconButton } from "../../components/atoms/Button/IconButton";
import { HiOutlineChatAlt2 } from "react-icons/hi";
import { Tabs } from "../../utils/enums";
import { BiTask } from "react-icons/bi";
import {
  selectChatTab,
  selectInstructionsTab,
  toggleSingleTab
} from "../../redux/slices/tabsSlice";
import { InstructionsTab } from "../../components/molecules/InstructionsTab/InstructionsTab";
import { initialSnackbar } from "../../utils/constants";

function Lobby({
  localStream,
  connection,
  connectionState,
  onGetSession,
  onChat
}) {
  const videoElement = useRef(null);
  const [participantStream, setParticipantStream] = useState(localStream);
  const [snackbar, setSnackbar] = useState(initialSnackbar);
  const isChatModalActive = useAppSelector(selectChatTab);
  const isInstructionsModalActive = useAppSelector(selectInstructionsTab);
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionIdParam = searchParams.get("sessionId");
  const participantIdParam = searchParams.get("participantId");
  const dispatch = useAppDispatch();
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

  const toggleModal = (modal) => {
    dispatch(toggleSingleTab(modal));
  };

  return (
    <>
      <div className="watchingRoomHeader flex flex-row justify-between items-center h-16 px-6">
        <Heading heading={"SYNCHRONY HUB"} />{" "}
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
        </div>
      </div>
      <ConsentModal />
      {/* Grid takes up screen space left from the AppToolbar */}
      <Box sx={{ height: "92vh", display: "flex" }}>
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
      </Box>
    </>
  );
}

export default Lobby;
