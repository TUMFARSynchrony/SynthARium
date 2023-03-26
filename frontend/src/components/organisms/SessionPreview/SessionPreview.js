import { integerToDateTime, isFutureSession } from "../../../utils/utils";
import { useDispatch } from "react-redux";
import { useState } from "react";
import { copySession, initializeSession } from "../../../features/openSession";
import { ActionIconButton, LinkActionIconButton } from "../../atoms/Button";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import List from '@mui/material/List';
import ListItem from "@mui/material/ListItem";
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import Chip from "@mui/material/Chip";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DeleteOutlined from '@mui/icons-material/DeleteOutlined';
import EditOutlined from "@mui/icons-material/EditOutlined";
import PlayArrowOutlined from "@mui/icons-material/PlayArrowOutlined";
import { getParticipantInviteLink } from "../../../utils/utils";
import CustomSnackbar from "../../molecules/CustomSnackbar";
// REMOVE: Use temporarily until fiters backend API connection is established
// import sessionData from '../../../bbbef1d7d0.json';

function SessionPreview({
  selectedSession,
  setSelectedSession,
  onDeleteSession,
  onJoinExperiment,
  onCreateExperiment,
}) {
  const dispatch = useDispatch();
  const deleteSession = () => {
    const sessionId = selectedSession.id;
    onDeleteSession(sessionId);
    setSelectedSession(null);
  };

  const [allParticipantsShow, setAllParticipantsShow] = useState(false);
  const [expandedParticipant, setExpandedParticipant] = useState("");
  const [openInviteLinkFeedback, setOpenInviteLinkFeedback] = useState(false);

  const handleParticipantsClick = () => {
    setAllParticipantsShow(!allParticipantsShow);
  };

  const handleSingleParticipantClick = (participantIndex) => {
    setExpandedParticipant(expandedParticipant === participantIndex ? "" : participantIndex);
  };

  const handleCopyParticipantInviteLink = (participantId, sessionId) => {
    const participantInviteLink = getParticipantInviteLink(participantId, sessionId);
    navigator.clipboard.writeText(participantInviteLink);
    setOpenInviteLinkFeedback(true);
  };

  const handleCloseParticipantInviteLinkFeedback = (event, reason) => {
    setOpenInviteLinkFeedback(false);
  };

  const experimentOngoing = selectedSession.creation_time > 0 && selectedSession.end_time === 0;
  // REMOVE: Use temporarily until fiters backend API connection is established
  // selectedSession = sessionData;

  return (
    <Card sx={{
      backgroundColor: experimentOngoing ? 'rgb(252, 232, 211)' : 'white',
      borderTop: experimentOngoing ? '3px solid rgb(255, 119, 0)' : '3px solid dodgerblue'
    }}>
      {
        experimentOngoing ? (
          <CardHeader title={`Experiment Ongoing: ${selectedSession.title}`}
            titleTypographyProps={{ fontWeight: 'bold', fontSize: '24px', color: 'rgb(255, 119, 0)' }} />
        ) :
          (
            <CardHeader title={`${selectedSession.title}`}
              titleTypographyProps={{ fontWeight: 'bold', fontSize: '24px' }} />
          )
      }
      <CardContent>
        <List>
          <ListItem>
            <ListItemText primary={`Date: ${integerToDateTime(selectedSession.date)}`} />
          </ListItem>
          <ListItemButton onClick={handleParticipantsClick}>
            <ListItemText primary={`Participants (${selectedSession.participants.length})`} />
            {allParticipantsShow ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
          <Collapse in={allParticipantsShow} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {
                selectedSession.participants.map((participant, participantIndex) => {
                  return (
                    <div key={participantIndex}>
                      <ListItemButton sx={{ pl: 4 }} onClick={() => handleSingleParticipantClick(participantIndex)}>
                        <ListItemText primary={`${participant.first_name} ${participant.last_name}`} />
                        {expandedParticipant === participantIndex ? <ExpandLess /> : <ExpandMore />}
                      </ListItemButton>
                      <Collapse in={expandedParticipant === participantIndex} timeout="auto" unmountOnExit>
                        <List component="div" disablePadding>
                          <ListItem sx={{ pl: 4, display: "flex", justifyContent: "space-between" }}>
                            <Typography variant="overline">Filters : </Typography>
                            {participant.audio_filters.length === 0 && participant.video_filters.length === 0 && <Typography>No filters applied!</Typography>}
                            <Box>
                              {
                                participant.audio_filters.map((audioFilter, audioFilterIndex) => {
                                  return (
                                    <Chip key={audioFilterIndex} variant="outlined" label={audioFilter.id} size="small" color="secondary" />
                                  )
                                })
                              }
                              {
                                participant.video_filters.map((videoFilter, videoFilterindex) => {
                                  return (
                                    <Chip key={videoFilterindex} variant="outlined" label={videoFilter.id} size="small" color="secondary" />
                                  )
                                })
                              }
                            </Box>
                            <ActionIconButton text="INVITE" variant="outlined" color="primary" size="small" onClick={() => handleCopyParticipantInviteLink(participant.id, selectedSession.id)} icon={<ContentCopyIcon />} />
                            <CustomSnackbar open={openInviteLinkFeedback} text={`Copied ${participant.first_name} ${participant.last_name}'s invite link to clipboard`}
                              severity="success" handleClose={handleCloseParticipantInviteLinkFeedback} />
                          </ListItem>
                        </List>
                      </Collapse>
                    </div>
                  )
                })
              }
            </List>
          </Collapse>
        </List>
        <Typography>
          {selectedSession.description}
        </Typography>
      </CardContent>
      <CardActions sx={{ display: 'flex', justifyContent: 'space-between' }}>
        {(selectedSession.creation_time === 0 ||
          selectedSession.end_time > 0) && (
            <ActionIconButton text="DELETE" variant="outlined" color="error" size="medium" onClick={() => deleteSession()} icon={<DeleteOutlined />} />
          )}
        <Box>
          <LinkActionIconButton text="DUPLICATE" variant="outlined" color="primary" size="medium" path="/sessionForm" onClick={() => dispatch(copySession(selectedSession))} icon={<ContentCopyIcon />} />
          {!selectedSession.creation_time > 0 &&
            selectedSession.end_time === 0 &&
            isFutureSession(selectedSession) && (
              <>
                <LinkActionIconButton text="EDIT" variant="outlined" color="primary" size="medium" path="/sessionForm" onClick={() => dispatch(initializeSession(selectedSession))} icon={<EditOutlined />} />
                <LinkActionIconButton text="JOIN" variant="contained" color="primary" size="medium" path="/watchingRoom" onClick={() => onCreateExperiment(selectedSession.id)} icon={<PlayArrowOutlined />} />
              </>
            )}
          {selectedSession.creation_time > 0 && selectedSession.end_time === 0 && (
            <LinkActionIconButton text="JOIN" variant="contained" size="medium" path="/watchingRoom" onClick={() => onJoinExperiment(selectedSession.id)} icon={<PlayArrowOutlined />} />
          )}
        </Box>
      </CardActions>
    </Card>
  );
}

export default SessionPreview;
