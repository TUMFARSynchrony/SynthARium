import Button from "../../atoms/Button/Button";
import InputTextField from "../../molecules/InputTextField/InputTextField";
import "./ParticipantData.css";
import { FaRegTrashAlt } from "react-icons/fa";
import Checkbox from "../../molecules/Checkbox/Checkbox";

function ParticipantData({
  onDeleteParticipant,
  onChange,
  index,
  first_name,
  last_name,
  link,
  mute,
}) {
  const handleChange = (first_name, last_name, link, mute) => {
    onChange(index, { first_name, last_name, link, mute });
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
      <InputTextField
        title="Link"
        value={link}
        placeholder={"Invite link"}
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
          onChange={() => handleChange(first_name, last_name, link, !mute)}
        />
      </div>

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
