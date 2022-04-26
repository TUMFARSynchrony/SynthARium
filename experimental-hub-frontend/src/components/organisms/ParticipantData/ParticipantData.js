import Button from "../../atoms/Button/Button";
import InputTextField from "../../molecules/InputTextField/InputTextField";
import "./ParticipantData.css";
import { FaRegTrashAlt } from "react-icons/fa";
import Checkbox from "../../molecules/Checkbox/Checkbox";
import { useState } from "react";

function ParticipantData({
  onDeleteParticipant,
  onChange,
  index,
  first_name,
  last_name,
  link,
  mute,
}) {
  const [showAdditionalInput, setShowAdditionalInput] = useState(false);

  const handleChange = (first_name, last_name, link, mute) => {
    onChange(index, { first_name, last_name, link, mute });
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
        required={true}
        onChange={(newFirstName) =>
          handleChange(newFirstName, last_name, link, mute)
        }
      />
      <InputTextField
        title="Last Name"
        value={last_name}
        placeholder={"Name of participant"}
        required={true}
        onChange={(newLastName) =>
          handleChange(first_name, newLastName, link, mute)
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
              <InputTextField
                title="First Name"
                value={first_name}
                placeholder={"Name of participant"}
                required={true}
                onChange={(newFirstName) =>
                  handleChange(newFirstName, last_name, link, mute)
                }
              />
              <InputTextField
                title="Last Name"
                value={last_name}
                placeholder={"Name of participant"}
                required={true}
                onChange={(newLastName) =>
                  handleChange(first_name, newLastName, link, mute)
                }
              />
              <InputTextField
                title="Link"
                value={link}
                placeholder={"Created by backend"}
                readonly={true}
                required={true}
                onChange={(newLink) =>
                  handleChange(first_name, last_name, newLink, mute)
                }
              />
              <div className="participantMuteCheckbox">
                <Checkbox
                  title="Mute"
                  value={mute}
                  onChange={() =>
                    handleChange(first_name, last_name, link, !mute)
                  }
                />
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
