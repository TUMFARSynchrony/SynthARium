import Button from "../../atoms/Button/Button";
import InputTextField from "../../molecules/InputTextField/InputTextField";
import "./ParticipantData.css";
import { FaRegTrashAlt } from "react-icons/fa";
import Checkbox from "../../molecules/Checkbox/Checkbox";
import { useState } from "react";
import Heading from "../../atoms/Heading/Heading";
import Label from "../../atoms/Label/Label";

function ParticipantData({
  onDeleteParticipant,
  onChange,
  index,
  first_name,
  last_name,
  link,
  muted,
  parameters,
}) {
  const [showAdditionalInput, setShowAdditionalInput] = useState(false);

  const handleChange = (first_name, last_name, link, muted) => {
    onChange(index, { first_name, last_name, link, muted });
  };

  const onAddAdditionalInformation = () => {
    setShowAdditionalInput(!showAdditionalInput);
  };

  return (
    <div className="participantDataContainer">
      <InputTextField
        title="First Name"
        value={first_name}
        placeholder={"Name of participant"}
        onChange={(newFirstName) =>
          handleChange(newFirstName, last_name, link, muted)
        }
      />
      <InputTextField
        title="Last Name"
        value={last_name}
        placeholder={"Name of participant"}
        onChange={(newLastName) =>
          handleChange(first_name, newLastName, link, muted)
        }
      />
      <Button
        name="Add additional information"
        design={"secondary"}
        onClick={() => onAddAdditionalInformation()}
      />
      {showAdditionalInput && (
        <div className="additionalParticipantInfoContainer">
          <div className="additionalParticipantInfo">
            <div className="additionalParticipantInfoCard">
              <Heading heading={"General information:"} />

              <InputTextField
                title="First Name"
                value={first_name}
                placeholder={"Name of participant"}
                onChange={(newFirstName) =>
                  handleChange(newFirstName, last_name, link, muted)
                }
              />
              <InputTextField
                title="Last Name"
                value={last_name}
                placeholder={"Name of participant"}
                onChange={(newLastName) =>
                  handleChange(first_name, newLastName, link, muted)
                }
              />
              <InputTextField
                title="Link"
                value={link}
                placeholder={"Created by backend"}
                readonly={true}
                onChange={(newLink) =>
                  handleChange(first_name, last_name, newLink, muted)
                }
              />
              <div className="participantMuteCheckbox">
                <Checkbox
                  title="Mute"
                  value={muted}
                  checked={muted}
                  onChange={() =>
                    handleChange(first_name, last_name, link, !muted)
                  }
                />
              </div>
              <Heading heading={"Current video position and size:"} />
              <div className="participantVideoSize">
                <div className="participantPosition">
                  <Label title={"x: "} /> {parameters.x}
                </div>
                <div className="participantPosition">
                  <Label title={"y: "} /> {parameters.y}
                </div>
                <div className="participantPosition">
                  <Label title={"Width: "} /> {parameters.width}
                </div>
                <div className="participantPosition">
                  <Label title={"Height: "} /> {parameters.height}
                </div>
              </div>
              <Button
                name="Finish"
                design={"secondary"}
                onClick={() => onAddAdditionalInformation()}
              />
            </div>
          </div>
        </div>
      )}

      <Button
        name=""
        design={"negative"}
        onClick={() => onDeleteParticipant()}
        icon={<FaRegTrashAlt />}
      />
    </div>
  );
}

export default ParticipantData;
