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
  muted,
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
