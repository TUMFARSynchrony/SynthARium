import React, { useState, useEffect } from "react";
import ChevronLeft from "@mui/icons-material/ChevronLeft";
import ChevronRight from "@mui/icons-material/ChevronRight";
import CardContent from "@mui/material/CardContent";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import {
  addParticipant,
  changeParticipant,
  changeValue,
  deleteParticipant,
  selectNumberOfParticipants,
  selectOpenSession
} from "../../redux/slices/openSessionSlice";
import { INITIAL_PARTICIPANT_DATA, initialSnackbar } from "../../utils/constants";
import { checkValidSession, filterListByIndex, getParticipantDimensions, getRandomColor } from "../../utils/utils";
import DragAndDrop from "../../components/organisms/DragAndDrop/DragAndDrop";
import ParticipantList from "./ParticipantList";
import SessionDetails from "./SessionDetails";
import { ActionButton, ActionIconButton, LinkButton } from "../../components/atoms/Button";
import CustomSnackbar from "../../components/atoms/CustomSnackbar/CustomSnackbar";

function SessionForm({ onSendSessionToBackend }) {
  const dispatch = useAppDispatch();
  const { openSession, numberOfParticipants } = useAppSelector((state) => ({
    openSession: selectOpenSession(state),
    numberOfParticipants: selectNumberOfParticipants(state)
  }));

  const [sessionData, setSessionData] = useState(openSession);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const [snackbar, setSnackbar] = useState(initialSnackbar);
  const [showSessionDataForm, setShowSessionDataForm] = useState(true);
  const [participantDimensions, setParticipantDimensions] = useState(
    getParticipantDimensions(sessionData.participants || [])
  );

  const [snackbarResponse, setSnackbarResponse] = useState({
    newParticipantInputEmpty: false,
    requiredInformationMissing: false,
    participantOriginalEmpty: false,
    newInputEqualsOld: false
  });

  useEffect(() => {
    setSessionData(openSession);
    if (openSession.participants.length === 0) {
      setPosition({ x: 0, y: 0 });
    }
  }, [openSession]);

  useEffect(() => {
    const snackbarMessages = {
      newParticipantInputEmpty: "You did not enter any information. Participant will be deleted now.",
      requiredInformationMissing:
        "Required information (Participant Name) is missing. Participant will be deleted now.",
      participantOriginalEmpty: "You need to save the information first!"
    };

    for (const condition in snackbarResponse) {
      if (
        snackbarResponse[condition] ||
        (condition === "participantOriginalEmpty" && !snackbarResponse.newInputEqualsOld)
      ) {
        setSnackbar({
          open: true,
          text: snackbarMessages[condition],
          severity: "warning"
        });
        return;
      }
    }
  }, [snackbarResponse]);

  const handleCanvasPlacement = (participantCount) => {
    if (participantCount !== 0 && participantCount % 20 === 0) {
      setPosition({ x: (participantCount / 20) * 250, y: 0 });
    } else {
      setPosition((prevPosition) => ({ x: prevPosition.x + 25, y: prevPosition.y + 25 }));
    }
  };

  const onDeleteParticipant = (index) => {
    dispatch(deleteParticipant(index));
    setParticipantDimensions((prevDimensions) => filterListByIndex(prevDimensions, index));
  };

  const onAddParticipant = () => {
    dispatch(
      addParticipant({
        ...INITIAL_PARTICIPANT_DATA,
        position: { ...position, z: 0 }
      })
    );
    const newParticipantDimensions = [
      ...participantDimensions,
      {
        shapes: {
          x: position.x,
          y: position.y,
          fill: getRandomColor(),
          z: 0
        },
        groups: {
          x: 0,
          y: 0,
          z: 0,
          width: 250,
          height: 250
        }
      }
    ];
    setParticipantDimensions(newParticipantDimensions);
  };

  const handleParticipantChange = (index, participant) => {
    dispatch(changeParticipant({ participant: participant, index: index }));
    setParticipantDimensions((prevDimensions) => {
      const newDimensions = [...prevDimensions];
      newDimensions[index].shapes = {
        ...newDimensions[index].shapes,
        participant_name: participant.participant_name
      };
      return newDimensions;
    });
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
    } else {
      onSendSessionToBackend(sessionData);
    }
  };

  return (
    <>
      <div className="flex h-[calc(100vh-84px)] flex-row px-4 py-8 items-start">
        {showSessionDataForm && (
          <div className="shadow-lg rounded-md h-full">
            <div className="px-4 flex flex-col h-full">
              <div className="flex justify-start items-center">
                <ChevronLeft sx={{ color: "gray" }} />
                <LinkButton text="Back to Session Overview" variant="text" size="small" path="/" />
              </div>
              <CardContent>
                <SessionDetails
                  sessionData={sessionData}
                  handleSessionDataChange={handleSessionDataChange}
                  numberOfParticipants={numberOfParticipants}
                />
                <ParticipantList
                  openSession={openSession}
                  onAddParticipant={onAddParticipant}
                  onDeleteParticipant={onDeleteParticipant}
                  handleParticipantChange={handleParticipantChange}
                  setSnackbarResponse={setSnackbarResponse}
                  handleCanvasPlacement={handleCanvasPlacement}
                  sessionData={sessionData}
                />
              </CardContent>
              <div className="flex justify-center h-full pb-2">
                <div className="self-end">
                  <ActionButton
                    text="SAVE SESSION"
                    variant="contained"
                    color="success"
                    size="medium"
                    onClick={onSaveSession}
                  />
                </div>
              </div>
            </div>
          </div>
        )}
        <div>
          <ActionIconButton
            text=""
            variant="text"
            color="primary"
            size="large"
            onClick={onShowSessionFormModal}
            icon={showSessionDataForm ? <ChevronLeft /> : <ChevronRight />}
          />
        </div>
        <div>
          <DragAndDrop
            participantDimensions={participantDimensions}
            setParticipantDimensions={setParticipantDimensions}
          />
        </div>
      </div>
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
