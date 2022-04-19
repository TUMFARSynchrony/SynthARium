import Checkbox from "../../components/molecules/Checkbox/Checkbox";
import InputDateField from "../../components/molecules/InputDateField/InputDateField";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";
import Button from "../../components/atoms/Button/Button";

import "./SessionForm.css";
import ParticipantData from "../../components/organisms/ParticipantData/ParticipantData";
import { useState } from "react";
import Heading from "../../components/atoms/Heading/Heading";

const sessionFormData = {
  id: "",
  title: "",
  description: "",
  date: 0,
  time_limit: 0,
  record: false,
  participants: [],
  start_time: 0,
  end_time: 0,
  notes: [],
};

function SessionForm() {
  const [participantList, setParticipantList] = useState([]);
  const [sessionData, setSessionData] = useState(sessionFormData);

  const onDeleteParticipant = (index) => {
    var filteredparticipantList = participantList.filter((participant, i) => {
      return i !== index;
    });
    setParticipantList(filteredparticipantList);
  };

  const onAddParticipant = () => {
    const newParticipantList = [...participantList, { name: "", link: "" }];
    setParticipantList(newParticipantList);
  };

  const handleChange = (index, participant) => {
    let newParticipantList = [...participantList];
    newParticipantList[index] = participant;
    setParticipantList(newParticipantList);
  };

  const handleDataChange = (objKey, newObj) => {
    let newObject = {};
    newObject[objKey] = newObj;
    setSessionData((sessionData) => ({
      ...sessionData,
      ...newObject,
    }));
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
            onChange={(newTitle) => handleDataChange("title", newTitle)}
          ></InputTextField>
          <InputDateField
            title="Date"
            value={sessionData.date}
            onChange={(newDate) => handleDataChange("date", newDate)}
          ></InputDateField>
          <InputTextField
            title="Time Limit"
            value={sessionData.time_limit}
            placeholder={"Your time limit in ms"}
            onChange={(newTimeLimit) =>
              handleDataChange("time_limit", newTimeLimit)
            }
          ></InputTextField>
          <Checkbox
            title="Record Session"
            value={sessionData.record_session}
            onChange={(newRecord) => handleDataChange("record", newRecord)}
          />
          <hr className="separatorLine"></hr>
          <Heading heading={"Participants"} />
          <div className="participantCheckboxes">
            <Checkbox
              title="Mute Audio"
              value={sessionData.mute_audio}
              onChange={(newMuteAudio) =>
                handleDataChange("mute_audio", newMuteAudio)
              }
            />
            <Checkbox
              title="Mute Video"
              value={sessionData.mute_video}
              onChange={(newMuteVideo) =>
                handleDataChange("mute_video", newMuteVideo)
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
                  onChange={handleChange}
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
            //TODO: Konva for drag and drop!!
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
