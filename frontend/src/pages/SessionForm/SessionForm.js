import Checkbox from "../../components/molecules/Checkbox/Checkbox";
import InputDateField from "../../components/molecules/InputDateField/InputDateField";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";
import Button from "../../components/atoms/Button/Button";
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
import { FaAngleRight, FaAngleLeft } from "react-icons/fa";
import { useDispatch, useSelector } from "react-redux";
import {
  addParticipant,
  changeParticipant,
  changeValue,
  deleteParticipant,
  initializeSession,
} from "../../features/openSession";
import { toast } from "react-toastify";

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
  const [showParticipantInput, setShowParticipantInput] = useState(false);

  const onDeleteParticipant = (index) => {
    dispatch(deleteParticipant({ index: index }));
    setParticipantDimensions(filterListByIndex(participantDimensions, index));
  };

  const onAddParticipant = () => {
    setShowParticipantInput(true);

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
  };

  const addRandomSessionData = () => {
    let newSessionData = {
      id: "",
      title: "Hello World",
      description: "Randomly created session",
      date: new Date().getTime(),
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
          filters: [],
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
      notes: [],
      log: "",
    };

    setTimeLimit(newSessionData.time_limit / 60000);
    dispatch(initializeSession(newSessionData));
    let dimensions = getParticipantDimensions(newSessionData.participants);
    setParticipantDimensions(dimensions);
  };

  return (
    <form className="sessionFormContainer">
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
                      showParticipantInput={showParticipantInput}
                      setShowParticipantInput={setShowParticipantInput}
                      handleParticipantChange={handleParticipantChange}
                    />
                  );
                })}
              </div>
              <Button
                name="Add new participant"
                design={"positive"}
                onClick={() => onAddParticipant()}
              />
            </div>
            <hr className="separatorLine"></hr>
          </div>

          <div className="sessionFormButtons">
            <Button name="Save" onClick={() => onSaveSession()} />
            <LinkButton name="Start" to="/watchingRoom" />
            <Button
              name="Random session data"
              onClick={() => addRandomSessionData()}
            />
          </div>
        </div>
      )}
      <Button
        name={""}
        icon={showSessionDataForm ? <FaAngleLeft /> : <FaAngleRight />}
        design={"close"}
        onClick={() => onShowSessionFormModal()}
        title={"Show/Close session form"}
      />
      <div className="sessionFormCanvas">
        <DragAndDrop
          participantDimensions={participantDimensions}
          setParticipantDimensions={setParticipantDimensions}
        />
      </div>
    </form>
  );
}

export default SessionForm;
