import SendIcon from "@mui/icons-material/Send";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import Paper from "@mui/material/Paper";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import styled from "@mui/material/styles/styled";
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import AppToolbar from "../../components/atoms/AppToolbar/AppToolbar";
import { ActionIconButton } from "../../components/atoms/Button";
import ConsentModal from "../../modals/ConsentModal/ConsentModal";
import ConnectionState from "../../networking/ConnectionState";
import { useAppSelector } from "../../redux/hooks";
import { selectCurrentSession } from "../../redux/slices/sessionsListSlice";
import { instructionsList } from "../../utils/constants";
import Note from "../../components/atoms/Note/Note";

function Lobby({ localStream, connection, connectionState, onGetSession }) {
  const videoElement = useRef(null);
  const [message, setMessage] = useState("");
  const [participantStream, setParticipantStream] = useState(localStream);
  const currentSession = useAppSelector(selectCurrentSession);
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionIdParam = searchParams.get("sessionId");
  const participantIdParam = searchParams.get("participantId");

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

  const TabText = styled(Typography)(({ theme }) => ({
    color: theme.palette.primary.main
  }));

  return (
    <>
      <AppToolbar />
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
        <Paper
          elevation={2}
          sx={{
            backgroundColor: "whitesmoke",
            height: "100%",
            width: "25%",
            overflow: "auto"
          }}
        >
          <Box sx={{ py: 2 }}>
            {/* Displays instructions from constants.js */}
            <TabText variant="button">Instructions</TabText>
            <List sx={{ listStyleType: "disc", lineHeight: 1.3, pl: 4 }}>
              {instructionsList.map((instruction, index) => {
                return (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {instruction}
                  </ListItem>
                );
              })}
            </List>
          </Box>
          <Box
            sx={{
              py: 1,
              height: "90%",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between"
            }}
          >
            <Box>
              <TabText variant="button">Chat</TabText>
              {/* Placeholder for the chat feature (only with experimenter) */}
              {currentSession &&
                currentSession.participants
                  .find((participant) => participant.id === participantIdParam)
                  .chat.map((message, index) => (
                    <Note
                      key={index}
                      content={message.message}
                      date={message.time}
                    />
                  ))}
            </Box>

            <Box
              sx={{
                px: 1,
                py: 2,
                display: "flex",
                alignItems: "center",
                justifyContent: "space-around"
              }}
            >
              <TextField
                label="Type your message"
                value={message}
                size="small"
                onChange={(event) => {
                  setMessage(event.target.value);
                }}
              />
              <ActionIconButton
                text="Send"
                variant="contained"
                color="primary"
                size="small"
                icon={<SendIcon />}
              />
            </Box>
          </Box>
        </Paper>
      </Box>
    </>
  );
}

export default Lobby;
