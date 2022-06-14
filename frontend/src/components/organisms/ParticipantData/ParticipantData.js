import Button from "../../atoms/Button/Button";
import InputTextField from "../../molecules/InputTextField/InputTextField";
import "./ParticipantData.css";

import { useForm } from "react-hook-form";
import { FaRegTrashAlt } from "react-icons/fa";
import ParticipantDataModal from "../../../modals/ParticipantDataModal";

function ParticipantData({
  onDeleteParticipant,
  participantData,
  sessionId,
  index,
  showParticipantInput,
  setShowParticipantInput,
  handleParticipantChange,
}) {
  const { register } = useForm();
  const onAddAdditionalInformation = () => {
    setShowParticipantInput(!showParticipantInput);
  };

  return (
    <div className="participantDataContainer">
      <InputTextField
        title="Participant Name"
        placeholder={"Enter the information"}
        value={[participantData.first_name, participantData.last_name]
          .filter((str) => str.length > 0)
          .join(" ")}
        readonly={true}
        register={register}
        label={"name"}
        required={false}
      />
      <div className="participantButtons">
        <Button
          name="Enter participant information"
          design={"secondary"}
          onClick={() => onAddAdditionalInformation()}
        />

        <Button
          name={""}
          design={"negative"}
          onClick={() => onDeleteParticipant()}
          icon={<FaRegTrashAlt />}
        />
      </div>

      {showParticipantInput && (
        <ParticipantDataModal
          originalParticipant={participantData}
          sessionId={sessionId}
          index={index}
          showParticipantInput={showParticipantInput}
          setShowParticipantInput={setShowParticipantInput}
          handleParticipantChange={handleParticipantChange}
          onDeleteParticipant={onDeleteParticipant}
        />
      )}
    </div>
  );
}

export default ParticipantData;
