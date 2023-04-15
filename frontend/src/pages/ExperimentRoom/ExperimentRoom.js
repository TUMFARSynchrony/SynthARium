import { useEffect, useState, useRef } from "react";
import AppToolbar from "../../components/atoms/AppToolbar/AppToolbar";
import ConsentModal from "../../modals/ConsentModal/ConsentModal";
import { ActionIconButton } from "../../components/atoms/Button";
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import styled from '@mui/material/styles/styled';
import SendIcon from '@mui/icons-material/Send';
import { instructionsList } from "../../utils/constants";


function ExperimentRoom({ localStream, connection }) {
  const videoElement = useRef(null);
  const [message, setMessage] = useState("");
  const [participantStream, setParticipantStream] = useState(localStream);

  useEffect(() => {
    setParticipantStream(localStream);
  }, [localStream]);

  useEffect(() => {
    if (participantStream) {
      videoElement.current.srcObject = localStream;
    }
  }, [participantStream])

  const TabText = styled(Typography)(({ theme }) => ({
    color: theme.palette.primary.main,
  }));

  return (
    <>
      <AppToolbar />
      <ConsentModal />
      {/* Grid takes up screen space left from the AppToolbar */}
      <Grid container sx={{ height: "92vh" }}>
        <Grid item sm={9}>
          <Paper elevation={2} sx={{ backgroundColor: "whitesmoke", height: "100%" }}>
            {
              participantStream ? (
                // Displaying local stream of participant
                <video ref={videoElement} autoPlay playsInline width="auto" height="100%">
                </video>
              ) : (
                <Typography>
                  Unable to access your video. Please check that you have allowed access to your camera and microphone.
                </Typography>
              )
            }
          </Paper>
        </Grid>
        <Grid item sm={3}>
          <Paper elevation={2} sx={{ backgroundColor: "whitesmoke", height: "48%", m: 2, overflow: "auto" }}>
            <Box sx={{ py: 2 }}>
              {/* Displays instructions from constants.js */}
              <TabText variant="button">Instructions</TabText>
              <List sx={{ listStyleType: 'disc', lineHeight: 1.3, pl: 4 }}>
                {
                  instructionsList.map((instruction, index) => {
                    return (
                      <ListItem key={index} sx={{ display: 'list-item' }}>
                        {instruction}
                      </ListItem>
                    )
                  })
                }
              </List>
            </Box>
          </Paper>
          <Paper elevation={2} sx={{ backgroundColor: "whitesmoke", height: "48%", m: 2 }}>
            <Box sx={{ py: 2, height: "90%", display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
              <TabText variant="button">Chat</TabText>
              {/* Placeholder for the chat feature (only with experimenter) */}
              <Box sx={{ px: 1, display: "flex", alignItems: "center", justifyContent: "space-around" }}>
                <TextField label="Type your message" value={message} size="small" onChange={(event) => { setMessage(event.target.value) }} />
                <ActionIconButton text="Send" variant="contained" color="primary" size="small" onClick={() => { }} icon={<SendIcon />} />
              </Box>
            </Box>
          </Paper>
        </Grid>
      </Grid >
    </>
  );
}

export default ExperimentRoom;
