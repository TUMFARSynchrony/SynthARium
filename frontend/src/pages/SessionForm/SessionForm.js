import Checkbox from "../../components/molecules/Checkbox/Checkbox";
import InputDateField from "../../components/molecules/InputDateField/InputDateField";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";
import Button from "../../components/atoms/Button/Button";
import ParticipantData from "../../components/organisms/ParticipantData/ParticipantData";
import DragAndDrop from "../../components/organisms/DragAndDrop/DragAndDrop";
import Heading from "../../components/atoms/Heading/Heading";
import { INITIAL_PARTICIPANT_DATA } from "../../utils/constants";

import "./SessionForm.css";
import { useState } from "react";
import {
  filterListByIndex,
  getRandomColor,
  getShapesFromParticipants,
} from "../../utils/utils";
import TextField from "../../components/molecules/TextField/TextField";
import { FaAngleRight, FaAngleLeft } from "react-icons/fa";
import { useLocation } from "react-router-dom";

function SessionForm() {
  const location = useLocation();
  const participantShapesObject = getShapesFromParticipants(
    location.state.initialData.participants
  );

  const [participantList, setParticipantList] = useState(
    location.state.initialData.participants
  );
  const [sessionData, setSessionData] = useState(location.state.initialData);
  const [participantShapes, setParticipantShapes] = useState(
    participantShapesObject.shapesArray
  );
  const [participantGroups, setParticipantGroups] = useState(
    participantShapesObject.groupArray
  );
  const [showSessionDataForm, setShowSessionDataForm] = useState(true);

  const onDeleteParticipant = (index) => {
    setParticipantList(filterListByIndex(participantList, index));
    setParticipantShapes(filterListByIndex(participantShapes, index));
    setParticipantGroups(filterListByIndex(participantGroups, index));
  };

  const onAddParticipant = () => {
    const newParticipantList = [...participantList, INITIAL_PARTICIPANT_DATA];
    setParticipantList(newParticipantList);

    const newParticipantShapes = [
      ...participantShapes,
      {
        x: 0,
        y: 0,
        fill: getRandomColor(),
      },
    ];
    setParticipantShapes(newParticipantShapes);

    const newPartcipantGroup = [
      ...participantGroups,
      {
        x: 10,
        y: 10,
        width: 100,
        height: 100,
      },
    ];
    setParticipantGroups(newPartcipantGroup);
  };

  const handleParticipantChange = (index, participant) => {
    let newParticipantList = [...participantList];
    newParticipantList[index] = {
      ...newParticipantList[index],
      ...participant,
    };

    setParticipantList(newParticipantList);

    let newParticipantShapes = [...participantShapes];
    newParticipantShapes[index] = {
      ...participantShapes[index],
      first_name: participant.first_name,
      last_name: participant.last_name,
    };
    setParticipantShapes(newParticipantShapes);
  };

  const handleSessionDataChange = (objKey, newObj) => {
    let newObject = {};
    newObject[objKey] = newObj;
    setSessionData((sessionData) => ({
      ...sessionData,
      ...newObject,
    }));
  };

  const onShowSessionFormModal = () => {
    setShowSessionDataForm(!showSessionDataForm);
  };

  const onSaveSession = () => {
    //TODO: send data to backend... how will we do that? pass connection to session form?
    let newParticipantList = [];
    newParticipantList = participantList.forEach((participant, index) => {
      participant.position.x = participantGroups[index].x;
      participant.position.y = participantGroups[index].y;
      participant.size.width = participantGroups[index].width;
      participant.size.height = participantGroups[index].height;
    });
    setParticipantList(newParticipantList);

    let newSessionData = { ...sessionData };
    newSessionData.participants = participantList;
    newSessionData.time_limit *= 60000;
    setSessionData(newSessionData);

    return sessionData;
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
            ></InputTextField>
            <TextField
              title="Description"
              value={sessionData.description}
              placeholder={"Short description of the session"}
              onChange={(newDescription) =>
                handleSessionDataChange("description", newDescription)
              }
            ></TextField>
            <div className="timeInput">
              <InputTextField
                title="Time Limit (in minutes)"
                value={sessionData.time_limit}
                placeholder={"Input time limit in MINUTES"}
                inputType={"number"}
                onChange={(newTimeLimit) =>
                  handleSessionDataChange("time_limit", newTimeLimit)
                }
              ></InputTextField>
              <InputDateField
                title="Date"
                value={sessionData.date}
                onChange={(newDate) =>
                  handleSessionDataChange(
                    "date",
                    newDate ? new Date(newDate).getTime() : 0
                  )
                }
              ></InputDateField>
            </div>

            <Checkbox
              title="Record Session"
              value={sessionData.record}
              checked={sessionData.record}
              onChange={() =>
                handleSessionDataChange("record", !sessionData.record)
              }
            />
            <hr className="separatorLine"></hr>
            <Heading heading={"Participants"} />
            <div className="participantCheckboxes"></div>
            <div className="sessionFormParticipants">
              <div className="scrollableParticipants">
                {participantList.map((participant, index) => {
                  return (
                    <ParticipantData
                      onDeleteParticipant={() => onDeleteParticipant(index)}
                      key={index}
                      index={index}
                      onChange={handleParticipantChange}
                      first_name={participant.first_name}
                      last_name={participant.last_name}
                      link={participant.link}
                      muted_audio={participant.muted_audio}
                      muted_video={participant.muted_video}
                      parameters={participantGroups[index]}
                      showModal={
                        location.state.initialData.participants.length > 0
                          ? false
                          : true
                      }
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
            <LinkButton name="Save" to="/" onClick={() => onSaveSession()} />
            <LinkButton name="Start" to="/watchingRoom" />
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
          participantShapes={participantShapes}
          participantGroups={participantGroups}
          setParticipantGroups={setParticipantGroups}
        />
      </div>
    </div>
  );
}

export default SessionForm;
