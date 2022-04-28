import Checkbox from "../../components/molecules/Checkbox/Checkbox";
import InputDateField from "../../components/molecules/InputDateField/InputDateField";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";
import Button from "../../components/atoms/Button/Button";
import ParticipantData from "../../components/organisms/ParticipantData/ParticipantData";
import DragAndDrop from "../../components/organisms/DragAndDrop/DragAndDrop";
import Heading from "../../components/atoms/Heading/Heading";
import {
  INITIAL_PARTICIPANT_DATA,
  INITIAL_SESSION_DATA,
} from "../../utils/constants";

import "./SessionForm.css";
import { useState } from "react";
import { filterListByIndex, getRandomColor } from "../../utils/utils";

function SessionForm() {
  const [participantList, setParticipantList] = useState([]);
  const [sessionData, setSessionData] = useState(INITIAL_SESSION_DATA);
  const [participantShapes, setParticipantShapes] = useState([]);
  const [participantGroups, setParticipantGroups] = useState([]);

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

  const onSaveSession = () => {
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
    setSessionData(newSessionData);

    return sessionData;
  };

  return (
    <div className="sessionFormContainer">
      <div className="sessionFormData">
        <div className="sessionForm">
          <Heading heading={"Session Data"} />
          <InputTextField
            title="Title"
            placeholder={"Your title"}
            value={sessionData.title}
            onChange={(newTitle) => handleSessionDataChange("title", newTitle)}
          ></InputTextField>
          <InputTextField
            title="Description"
            value={sessionData.description}
            placeholder={"Short description of the session"}
            onChange={(newDescription) =>
              handleSessionDataChange("description", newDescription)
            }
          ></InputTextField>
          <div className="timeInput">
            <InputTextField
              title="Time Limit"
              value={sessionData.time_limit}
              placeholder={"Your time limit in ms"}
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
                    muted={participant.muted}
                    parameters={participantGroups[index]}
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
