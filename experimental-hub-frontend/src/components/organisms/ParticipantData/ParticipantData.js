import Button from "../../atoms/Button/Button";
import InputTextField from "../../molecules/InputTextField/InputTextField";
import "./ParticipantData.css";
import { FaRegTrashAlt } from "react-icons/fa";

function ParticipantData({ onDeleteParticipant, onChange, index, name, link }) {
  const handleChange = (name, link) => {
    onChange(index, { name, link });
  };

  return (
    <div className="participantDataContainer">
      <InputTextField
        title="Name"
        value={name}
        onChange={(newName) => handleChange(newName, link)}
      />
      <InputTextField
        title="Link"
        value={link}
        onChange={(newLink) => handleChange(name, newLink)}
      />
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
