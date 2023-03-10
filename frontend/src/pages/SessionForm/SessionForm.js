import Checkbox from "../../components/molecules/Checkbox/Checkbox";
import InputDateField from "../../components/molecules/InputDateField/InputDateField";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import ParticipantData from "../../components/organisms/ParticipantData/ParticipantData";
import DragAndDrop from "../../components/organisms/DragAndDrop/DragAndDrop";
import Heading from "../../components/atoms/Heading/Heading";
import { INITIAL_PARTICIPANT_DATA } from "../../utils/constants";
import {
  filterListByIndex,
  getRandomColor,
  getParticipantDimensions,
  formatDate,
  checkValidSession,
} from "../../utils/utils";
import TextAreaField from "../../components/molecules/TextAreaField/TextAreaField";

import "./SessionForm.css";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  addParticipant,
  changeParticipant,
  changeValue,
  deleteParticipant,
  initializeSession,
} from "../../features/openSession";
import { toast } from "react-toastify";
import { ActionButton, ActionIconButton, LinkButton } from "../../components/atoms/Button";
import ChevronLeft from "@mui/icons-material/ChevronLeft";
import ChevronRight from "@mui/icons-material/ChevronRight";

function SessionForm({ onSendSessionToBackend }) {
  const dispatch = useDispatch();
  let openSession = useSelector((state) => state.openSession.value);
  const [sessionData, setSessionData] = useState(openSession);
  const [timeLimit, setTimeLimit] = useState(sessionData.time_limit / 60000);

  useEffect(() => {
    setSessionData(openSession);
  }, [openSession]);

  const [participantDimensions, setParticipantDimensions] = useState(
    getParticipantDimensions(
      sessionData.participants ? sessionData.participants : []
    )
  );

  const [showSessionDataForm, setShowSessionDataForm] = useState(true);

  const onDeleteParticipant = (index) => {
    dispatch(deleteParticipant({ index: index }));
    setParticipantDimensions(filterListByIndex(participantDimensions, index));
  };

  const onAddParticipant = () => {
    dispatch(addParticipant(INITIAL_PARTICIPANT_DATA));

    const newParticipantDimensions = [
      ...participantDimensions,
      {
        shapes: {
          x: 0,
          y: 0,
          fill: getRandomColor(),
          z: 0,
        },
        groups: { x: 10, y: 10, z: 0, width: 300, height: 300 },
      },
    ];

    setParticipantDimensions(newParticipantDimensions);
  };

  const handleParticipantChange = (index, participant) => {
    dispatch(changeParticipant({ participant: participant, index: index }));

    let newParticipantDimensions = [...participantDimensions];
    newParticipantDimensions[index].shapes = {
      ...newParticipantDimensions[index].shapes,
      first_name: participant.first_name,
      last_name: participant.last_name,
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
      toast.error("Failed to save session since required fields are missing!");
      return;
    }

    onSendSessionToBackend(sessionData);

    console.log("sessionData", sessionData);
  };

  const addRandomSessionData = () => {
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
          first_name: "Max",
          last_name: "Mustermann",
          muted_audio: true,
          muted_video: true,
          banned: false,
          audio_filters: [],
          video_filters: [],
          chat: [],
          position: {
            x: 10,
            y: 10,
            z: 0,
          },
          size: {
            width: 300,
            height: 300,
          },
        },
      ],
      start_time: 0,
      end_time: 0,
      creation_time: 0,
      notes: [],
      log: "",
    };

    setTimeLimit(newSessionData.time_limit / 60000);
    dispatch(initializeSession(newSessionData));
    let dimensions = getParticipantDimensions(newSessionData.participants);
    setParticipantDimensions(dimensions);
  };

  return (
    <div className="sessionFormContainer">
      {showSessionDataForm && (
        <div className="sessionFormData">
          <div className="sessionForm">
            <Heading heading={"Session Data"} />
            <InputTextField
              title="Title"
              placeholder={"Your title"}
              value={sessionData.title}
              onChange={(newTitle) =>
                handleSessionDataChange("title", newTitle)
              }
              required={true}
            />
            <TextAreaField
              title="Description"
              value={sessionData.description}
              placeholder={"Short description of the session"}
              onChange={(newDescription) =>
                handleSessionDataChange("description", newDescription)
              }
              required={true}
            />
            <div className="timeInput">
              <InputTextField
                title="Time Limit (in minutes)"
                value={timeLimit}
                inputType={"number"}
                onChange={(newTimeLimit) => {
                  setTimeLimit(newTimeLimit);
                  handleSessionDataChange("time_limit", newTimeLimit * 60000);
                }}
                required={true}
                min={1}
              />
              <InputDateField
                title="Date"
                value={sessionData.date ? formatDate(sessionData.date) : ""}
                onChange={(newDate) =>
                  handleSessionDataChange(
                    "date",
                    newDate ? new Date(newDate).getTime() : 0
                  )
                }
                required={true}
              />
            </div>

            <Checkbox
              title="Record Session"
              value={sessionData.record}
              checked={sessionData.record}
              onChange={() =>
                handleSessionDataChange("record", !sessionData.record)
              }
              required={false}
            />
            <hr className="separatorLine"></hr>
            <Heading heading={"Participants"} />
            <div className="participantCheckboxes"></div>
            <div className="sessionFormParticipants">
              <div className="scrollableParticipants">
                {openSession.participants.map((participant, index) => {
                  return (
                    <ParticipantData
                      onDeleteParticipant={() => onDeleteParticipant(index)}
                      key={index}
                      index={index}
                      participantData={participant}
                      sessionId={sessionData.id}
                      handleParticipantChange={handleParticipantChange}
                    />
                  );
                })}
              </div>
              <ActionButton
                text="Add new participant"
                variant="contained"
                color="primary"
                size="large"
                onClick={() => onAddParticipant()}
              />
            </div>
            <hr className="separatorLine"></hr>
          </div>

          <div className="sessionFormButtons">
            <ActionButton text="Save" variant="contained" color="primary" size="large" onClick={() => onSaveSession()} />
            <LinkButton text="Start" variant="contained" size="large" path="/watchingRoom" />
            <ActionButton
              text="Random session data"
              variant="contained"
              color="primary"
              size="large"
              onClick={() => addRandomSessionData()}
            />
          </div>
        </div>
      )}
      <ActionIconButton
        text=""
        variant="text"
        color="primary"
        size="large"
        onClick={() => onShowSessionFormModal()}
        icon={showSessionDataForm ? <ChevronLeft /> : <ChevronRight />}
      />
      <div className="sessionFormCanvas">
        <DragAndDrop
          participantDimensions={participantDimensions}
          setParticipantDimensions={setParticipantDimensions}
        />
      </div>
    </div>
  );
}

export default SessionForm;
