import Checkbox from "../../components/molecules/Checkbox/Checkbox";
import InputDateField from "../../components/molecules/InputDateField/InputDateField";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";
import Button from "../../components/atoms/Button/Button";

import "./SessionForm.css";
import ParticipantData from "../../components/organisms/ParticipantData/ParticipantData";
import { useState } from "react";
import Heading from "../../components/atoms/Heading/Heading";

function SessionForm() {
  const [participantList, setParticipantList] = useState([]);

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

  return (
    <div className="sessionFormContainer">
      <div className="sessionFormCard">
        <div className="sessionPlanningForm">
          <Heading heading={"Session Data"} />
          <InputTextField
            title="Title"
            placeholder={"Your title"}
          ></InputTextField>
          <InputDateField title="Date"></InputDateField>
          <InputTextField
            title="Time Limit"
            placeholder={"Your time limit in ms"}
          ></InputTextField>
          <Checkbox title="Record Session" />
          <hr className="separatorLine"></hr>
          <Heading heading={"Participants"} />
          <div className="participantCheckboxes">
            <Checkbox title="Mute Audio" />
            <Checkbox title="Mute Video" />
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
