import DragAndDrop from "../../components/organisms/DragAndDrop/DragAndDrop";
import ParticipantData from "../../components/organisms/ParticipantData/ParticipantData";
import { CANVAS_SIZE, INITIAL_PARTICIPANT_DATA } from "../../utils/constants";
import {
  checkValidSession,
  filterListByIndex,
  formatDate,
  getParticipantDimensions,
  getRandomColor
} from "../../utils/utils";

import AddIcon from "@mui/icons-material/Add";
import ChevronLeft from "@mui/icons-material/ChevronLeft";
import ChevronRight from "@mui/icons-material/ChevronRight";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { useEffect, useState } from "react";
import {
  ActionButton,
  ActionIconButton,
  LinkButton
} from "../../components/atoms/Button";
import CustomSnackbar from "../../components/atoms/CustomSnackbar/CustomSnackbar";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import {
  addParticipant,
  changeParticipant,
  changeValue,
  deleteParticipant,
  initializeSession,
  selectNumberOfParticipants,
  selectOpenSession
} from "../../redux/slices/openSessionSlice";
import { initialSnackbar } from "../../utils/constants";
import { Button } from "@mui/material";

function SessionForm({ onSendSessionToBackend }) {
  const dispatch = useAppDispatch();
  const openSession = useAppSelector(selectOpenSession);
  const [sessionData, setSessionData] = useState(openSession);
  const numberOfParticipants = useAppSelector(selectNumberOfParticipants);
  const [xAxis, setXAxis] = useState(0);
  const [yAxis, setYAxis] = useState(0);
  // TO DO: remove the field time_limit from session.json
  const [timeLimit, setTimeLimit] = useState(sessionData.time_limit / 60000);
  // const [numOfParticipants, setNumOfParticipants] = useState();
  const [snackbar, setSnackbar] = useState(initialSnackbar);
  const [showSessionDataForm, setShowSessionDataForm] = useState(true);
  const [participantDimensions, setParticipantDimensions] = useState(
    getParticipantDimensions(
      sessionData.participants ? sessionData.participants : []
    )
  );
  const [participantDimensionPast, setParticipantDimensionPast] = useState([
    []
  ]);
  const [participantDimensionFuture, setParticipantDimensionFuture] = useState(
    []
  );

  // It is used as flags to display warning notifications upon entry of incorrect data/not saved in the Participant Modal.
  // It is displayed here instead of in the Participant Modal itself, since upon closing the modal it is no longer
  // available to display the warnings.
  const [snackbarResponse, setSnackbarResponse] = useState({
    newParticipantInputEmpty: false,
    requiredInformationMissing: false,
    participantOriginalEmpty: false,
    newInputEqualsOld: false
  });

  useEffect(() => {
    setSessionData(openSession);
    if (openSession.participants.length === 0) {
      setXAxis(0);
      setYAxis(0);
    }
  }, [openSession]);

  useEffect(() => {
    if (snackbarResponse.newParticipantInputEmpty) {
      setSnackbar({
        open: true,
        text: "You did not enter any information. Participant will be deleted now.",
        severity: "warning"
      });
      return;
    }

    if (snackbarResponse.requiredInformationMissing) {
      setSnackbar({
        open: true,
        text: "Required information (Participant Name) is missing. Participant will be deleted now.",
        severity: "warning"
      });
      return;
    }

    if (
      snackbarResponse.participantOriginalEmpty &&
      !snackbarResponse.newInputEqualsOld
    ) {
      setSnackbar({
        open: true,
        text: "You need to save the information first!",
        severity: "warning"
      });
      return;
    }
  }, [snackbarResponse]);

  const handleUndo = () => {
    if (participantDimensionPast.length === 0) {
      return;
    }

    setParticipantDimensionFuture([
      ...participantDimensionFuture,
      participantDimensions
    ]);
    const lastElement = participantDimensionPast.pop();
    setParticipantDimensions(lastElement);
    setParticipantDimensionPast([...participantDimensionPast]);
  };

  const handleRedo = () => {
    if (participantDimensionFuture.length === 0) {
      return;
    }

    setParticipantDimensionPast([
      ...participantDimensionPast,
      participantDimensions
    ]);
    const lastElement = participantDimensionFuture.pop();
    setParticipantDimensions(lastElement);
    setParticipantDimensionFuture([...participantDimensionFuture]);
  };

  const handleCanvasPlacement = () => {
    setXAxis(xAxis + 25);
    setYAxis(yAxis + 25);
  };

  const addDimensionToHistory = () => {
    let dimensions = [];
    participantDimensions.map((participantDimension) => {
      dimensions = [
        ...dimensions,
        {
          groups: participantDimension.groups,
          shapes: participantDimension.shapes
        }
      ];
    });
    setParticipantDimensionPast([...participantDimensionPast, dimensions]);
    setParticipantDimensionFuture([]);
  };

  const onDeleteParticipant = (index) => {
    dispatch(deleteParticipant(index));
    addDimensionToHistory();
    setParticipantDimensions(filterListByIndex(participantDimensions, index));
  };

  const onAddParticipant = () => {
    dispatch(addParticipant(INITIAL_PARTICIPANT_DATA));
    const newParticipantDimensions = [
      ...participantDimensions,
      {
        shapes: {
          x: xAxis,
          y: yAxis,
          fill: getRandomColor(),
          z: 0
        },
        groups: { x: 0, y: 0, z: 0, width: 300, height: 300 }
      }
    ];
    setParticipantDimensions(newParticipantDimensions);
    // TODO: automatically select the new participant
  };

  const handleParticipantChange = (index, participant) => {
    addDimensionToHistory();
    dispatch(changeParticipant({ participant: participant, index: index }));

    let newParticipantDimensions = [...participantDimensions];
    newParticipantDimensions[index].shapes = {
      ...newParticipantDimensions[index].shapes,
      participant_name: participant.participant_name
    };
    setParticipantDimensions(newParticipantDimensions);
  };

  const handleSessionDataChange = (objKey, newObj) => {
    dispatch(changeValue({ objKey: objKey, objValue: newObj }));
  };

  const onShowSessionFormModal = () => {
    setShowSessionDataForm(!showSessionDataForm);
  };

  const onSaveSession = () => {
    if (!checkValidSession(sessionData)) {
      setSnackbar({
        open: true,
        text: "Failed to save session since required fields are missing!",
        severity: "error"
      });
      return;
    }
    onSendSessionToBackend(sessionData);
  };

  const addRandomSessionData = () => {
    addDimensionToHistory();
    const futureDate = new Date().setDate(new Date().getDate() + 7);

    let newSessionData = {
      id: "",
      title: "Hello World",
      description: "Randomly created session",
      date: new Date(futureDate).getTime(),
      time_limit: 3600000,
      record: true,
      participants: [
        {
          id: "",
          participant_name: "Max Mustermann",
          muted_audio: true,
          muted_video: true,
          banned: false,
          audio_filters: [],
          video_filters: [],
          chat: [],
          position: {
            x: 10,
            y: 10,
            z: 0
          },
          size: {
            width: 300,
            height: 300
          }
        }
      ],
      start_time: 0,
      end_time: 0,
      creation_time: 0,
      notes: [],
      log: ""
    };

    setTimeLimit(newSessionData.time_limit / 60000);
    dispatch(initializeSession(newSessionData));
    let dimensions = getParticipantDimensions(newSessionData.participants);
    setParticipantDimensions(dimensions);
  };

  // TO DO: auto create x no. of participants.
  // const handleCreateParticipants = () => {
  //   for (let i = 0; i < numOfParticipants; i++) {
  //     onAddParticipant();
  //     console.log(sessionData);
  //   }
  // };
  return (
    <>
      <Grid container sx={{ mx: 4, my: 2 }}>
        {showSessionDataForm && (
          <Grid item sm={5}>
            <Box sx={{ display: "flex", justifyContent: "flex-start", mb: 1 }}>
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <ChevronLeft sx={{ color: "gray" }} />
              </Box>
              <LinkButton
                text="Back to Session Overview"
                variant="text"
                size="small"
                path="/"
              />
            </Box>
            <Card elevation={3}>
              <Typography variant="h6" sx={{ mt: 2, fontWeight: "bold" }}>
                Session Details
              </Typography>
              <Box sx={{ height: "74vh", overflowY: "auto" }}>
                <CardContent>
                  {/* Override text fields' margin and width using MUI classnames */}
                  <Box
                    component="form"
                    sx={{ "& .MuiTextField-root": { m: 1 } }}
                    noValidate
                    autoComplete="off"
                  >
                    <Box sx={{ "& .MuiTextField-root": { width: "38vw" } }}>
                      <TextField
                        label="Title"
                        value={sessionData.title}
                        size="small"
                        required
                        onChange={(event) =>
                          handleSessionDataChange("title", event.target.value)
                        }
                      />
                      <TextField
                        label="Description"
                        value={sessionData.description}
                        size="small"
                        required
                        onChange={(event) =>
                          handleSessionDataChange(
                            "description",
                            event.target.value
                          )
                        }
                      />
                    </Box>
                    <Box sx={{ "& .MuiTextField-root": { width: "18.5vw" } }}>
                      <TextField
                        value={
                          sessionData.date ? formatDate(sessionData.date) : ""
                        }
                        type="datetime-local"
                        size="small"
                        required
                        onChange={(event) =>
                          handleSessionDataChange(
                            "date",
                            event.target.value
                              ? new Date(event.target.value).getTime()
                              : 0
                          )
                        }
                      />
                      <TextField
                        label="Number of Participants"
                        value={numberOfParticipants}
                        type="number"
                        size="small"
                        disabled
                      />
                    </Box>
                    <Box sx={{ mt: 1, mb: 3 }}>
                      <FormControlLabel
                        control={<Checkbox />}
                        label="Record Session"
                        checked={sessionData.record}
                        onChange={() =>
                          handleSessionDataChange("record", !sessionData.record)
                        }
                      />
                      {/* <ActionIconButton text="Create participants" variant="contained" color="primary" size="small" onClick={() => handleCreateParticipants()} icon={<PeopleOutline />} /> */}
                    </Box>
                  </Box>

                  <Box sx={{ display: "flex", justifyContent: "center" }}>
                    <Typography variant="h6" sx={{ my: 1, fontWeight: "bold" }}>
                      Participants
                    </Typography>
                    <ActionIconButton
                      text="ADD"
                      variant="outlined"
                      color="primary"
                      size="small"
                      onClick={() => onAddParticipant()}
                      icon={<AddIcon />}
                    />
                  </Box>

                  {openSession.participants.map((participant, index) => {
                    return (
                      <ParticipantData
                        onDeleteParticipant={() => onDeleteParticipant(index)}
                        key={index}
                        index={index}
                        participantData={participant}
                        sessionId={sessionData.id}
                        handleParticipantChange={handleParticipantChange}
                        setSnackbarResponse={setSnackbarResponse}
                        handleCanvasPlacement={handleCanvasPlacement}
                      />
                    );
                  })}
                </CardContent>
              </Box>
              <Box sx={{ my: 1 }}>
                {/* <ActionButton text="RANDOM SESSION DATA" variant="contained" color="primary" size="medium" onClick={() => addRandomSessionData()} /> */}
                <ActionButton
                  text="SAVE SESSION"
                  variant="contained"
                  color="success"
                  size="medium"
                  onClick={() => onSaveSession()}
                />
              </Box>
            </Card>
          </Grid>
        )}
        <Grid item>
          <ActionIconButton
            text=""
            variant="text"
            color="primary"
            size="large"
            onClick={() => onShowSessionFormModal()}
            icon={showSessionDataForm ? <ChevronLeft /> : <ChevronRight />}
          />
        </Grid>
        <Grid item sm={5}>
          <Button onClick={handleUndo}>undo</Button>
          <Button onClick={handleRedo}>redo</Button>
          <Box sx={{ display: "flex", justifyContent: "flex-start" }}>
            {/* <Link variant="body2" sx={{ color: "gray", textDecorationColor: "gray", fontWeight: "bold" }}>
              Expand Video Canvas
            </Link> */}
          </Box>
          <Paper
            elevation={2}
            sx={{
              backgroundColor: "whitesmoke",
              width: CANVAS_SIZE.width,
              height: CANVAS_SIZE.height
            }}
          >
            <DragAndDrop
              participantDimensions={participantDimensions}
              setParticipantDimensions={setParticipantDimensions}
              addDimensionToHistory={addDimensionToHistory}
            />
          </Paper>
        </Grid>
      </Grid>
      <CustomSnackbar
        open={snackbar.open}
        text={snackbar.text}
        severity={snackbar.severity}
        handleClose={() => setSnackbar(initialSnackbar)}
      />
    </>
  );
}

export default SessionForm;
