import Checkbox from "../../components/molecules/Checkbox/Checkbox";
import InputDateField from "../../components/molecules/InputDateField/InputDateField";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";
import Button from "../../components/atoms/Button/Button";
import ParticipantData from "../../components/organisms/ParticipantData/ParticipantData";
import DragAndDrop from "../../components/organisms/DragAndDrop/DragAndDrop";
import Heading from "../../components/atoms/Heading/Heading";
import { CANVAS_SIZE, INITIAL_SESSION_DATA } from "../../utils/constants";

import "./SessionForm.css";
import { useState } from "react";

function SessionForm() {
  const [participantList, setParticipantList] = useState([]);
  const [sessionData, setSessionData] = useState(INITIAL_SESSION_DATA);
  const [participantShapes, setParticipantShapes] = useState([]);
  const [participantGroup, setParticipantGroup] = useState([]);

  const [canvasSize, setCanvasSize] = useState(CANVAS_SIZE);

  const onDeleteParticipant = (index) => {
    setParticipantList(filterListByIndex(participantList, index));
    setParticipantShapes(filterListByIndex(participantShapes, index));
    setParticipantGroup(filterListByIndex(participantGroup, index));

    setCanvasSize({
      ...canvasSize,
      height: canvasSize.height - 150,
    });
  };

  const filterListByIndex = (list, index) => {
    let filteredList = list.filter((obj, i) => {
      return i !== index;
    });

    return filteredList;
  };

  const onAddParticipant = () => {
    const newParticipantList = [...participantList, { name: "", link: "" }];
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
      ...participantGroup,
      {
        x: 10,
        y: 10,
        width: 100,
        height: 100,
      },
    ];
    setParticipantGroup(newPartcipantGroup);

    setCanvasSize({
      ...canvasSize,
      height: canvasSize.height + 150,
    });
  };

  const handleParticipantChange = (index, participant) => {
    let newParticipantList = [...participantList];
    newParticipantList[index] = participant;
    setParticipantList(newParticipantList);

    let newParticipantShapes = [...participantShapes];
    newParticipantShapes[index] = {
      ...participantShapes[index],
      text: participant.name,
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

  const getRandomColor = () => {
    let letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  };

  console.log("SessionData", sessionData);
  return (
    <div className="sessionFormContainer">
      <div className="sessionFormCard">
        <div className="sessionPlanningForm">
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
          <InputTextField
            title="Time Limit"
            value={sessionData.time_limit}
            placeholder={"Your time limit in ms"}
            onChange={(newTimeLimit) =>
              handleSessionDataChange("time_limit", newTimeLimit)
            }
          ></InputTextField>
          <div className="timeInput">
            <InputDateField
              title="Date"
              value={sessionData.date}
              onChange={(newDate) => handleSessionDataChange("date", newDate)}
            ></InputDateField>
            <InputTextField
              title="Start Time"
              inputType={"time"}
              value={sessionData.start_time}
              onChange={(newStartTime) =>
                handleSessionDataChange("start_time", newStartTime)
              }
            ></InputTextField>
            <InputTextField
              title="End Time"
              inputType={"time"}
              value={sessionData.end_time}
              onChange={(newEndTime) =>
                handleSessionDataChange("end_time", newEndTime)
              }
            ></InputTextField>
          </div>
          <Checkbox
            title="Record Session"
            value={sessionData.record_session}
            onChange={(newRecord) =>
              handleSessionDataChange("record", newRecord)
            }
          />
          <hr className="separatorLine"></hr>
          <Heading heading={"Participants"} />
          <div className="participantCheckboxes">
            <Checkbox
              title="Mute Audio"
              value={sessionData.mute_audio}
              onChange={(newMuteAudio) =>
                handleSessionDataChange("mute_audio", newMuteAudio)
              }
            />
            <Checkbox
              title="Mute Video"
              value={sessionData.mute_video}
              onChange={(newMuteVideo) =>
                handleSessionDataChange("mute_video", newMuteVideo)
              }
            />
          </div>
          <div className="sessionFormParticipants">
            {participantList.map((participant, index) => {
              return (
                <ParticipantData
                  onDeleteParticipant={() => onDeleteParticipant(index)}
                  key={index}
                  index={index}
                  onChange={handleParticipantChange}
                  name={participant.name}
                  link={participant.link}
                />
              );
            })}
            <Button
              name="Add new participant"
              design={"positive"}
              onClick={() => onAddParticipant()}
            />
          </div>
          <div className="sessionFormCanvas">
            <DragAndDrop
              width={canvasSize.width}
              height={canvasSize.height}
              rectangles={participantShapes}
              participantGroup={participantGroup}
              setParticipantGroup={setParticipantGroup}
            />
          </div>
          <hr className="separatorLine"></hr>
        </div>

        <div className="sessionFormButtons">
          <LinkButton name="Save" to="/" />
          <LinkButton name="Start" to="/watchingRoom" />
        </div>
      </div>
    </div>
  );
}

export default SessionForm;
