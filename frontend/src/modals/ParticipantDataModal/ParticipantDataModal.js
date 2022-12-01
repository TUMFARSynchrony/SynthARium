import "./ParticipantDataModal.css";

import { ToastContainer, toast } from "react-toastify";
import Heading from "../../components/atoms/Heading/Heading";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import Checkbox from "../../components/molecules/Checkbox/Checkbox";
import Label from "../../components/atoms/Label/Label";
import Button from "../../components/atoms/Button/Button";
import { useState } from "react";
import { PARTICIPANT_HOST } from "../../utils/constants";

function ParticipantDataModal({
  originalParticipant,
  sessionId,
  index,
  showParticipantInput,
  setShowParticipantInput,
  handleParticipantChange,
  onDeleteParticipant,
}) {
  const [participantCopy, setParticipantCopy] = useState(originalParticipant);

  const handleChange = (objKey, objValue) => {
    const newParticipantData = { ...participantCopy };
    newParticipantData[objKey] = objValue;
    setParticipantCopy(newParticipantData);
  };

  const onCloseModalWithoutData = () => {
    setShowParticipantInput(!showParticipantInput);

    let newParticipantInputEmpty =
      participantCopy.first_name === "" && participantCopy.last_name === "";

    if (newParticipantInputEmpty) {
      onDeleteParticipant(index);
      toast.warning(
        "You did not enter any information. Participant will be deleted now."
      );
      return;
    }

    let requiredInformationMissing =
      participantCopy.first_name === "" || participantCopy.last_name === "";

    if (requiredInformationMissing) {
      onDeleteParticipant(index);
      toast.warning(
        "Required information (First Name/Last Name) missing. Participant will be deleted now."
      );
      return;
    }

    let participantOriginalEmpty =
      originalParticipant.first_name.length === 0 &&
      originalParticipant.last_name.length === 0;

    let newInputEqualsOld = participantCopy === originalParticipant;

    if (participantOriginalEmpty && !newInputEqualsOld) {
      onDeleteParticipant(index);
      toast.warning("You need to save the information first.");
      return;
    }

    if (!newInputEqualsOld) {
      toast.warning("You need to save the information first.");
      setParticipantCopy(originalParticipant);
      return;
    }
  };

  const onSaveParticipantData = () => {
    if (participantCopy.first_name === "" || participantCopy.last_name === "") {
      toast.error(
        "Failed to save participant since required fields are missing!"
      );
      return;
    }

    setShowParticipantInput(!showParticipantInput);
    handleParticipantChange(index, participantCopy);
  };

  return (
    <div className="additionalParticipantInfoContainer">
      <ToastContainer />

      <div className="additionalParticipantInfo">
        <div className="additionalParticipantInfoCard">
          <Heading heading={"General information:"} />

          <InputTextField
            title="First Name"
            value={participantCopy.first_name}
            placeholder={"Name of participant"}
            onChange={(newFirstName) => {
              handleChange("first_name", newFirstName);
            }}
            required={true}
          />
          <InputTextField
            title="Last Name"
            value={participantCopy.last_name}
            placeholder={"Name of participant"}
            onChange={(newLastName) => {
              handleChange("last_name", newLastName);
            }}
            required={true}
          />
          <InputTextField
            title="Link"
            value={
              !(participantCopy.id.empty && sessionId.empty)
                ? `${PARTICIPANT_HOST}?participantId=${participantCopy.id}&sessionId=${sessionId}`
                : "Save session to generate link."
            }
            readonly={true}
            required={false}
          />
          <div className="participantMuteCheckbox">
            <Checkbox
              title="Mute Audio"
              value={participantCopy.muted_audio}
              checked={participantCopy.muted_audio}
              onChange={() =>
                handleChange("muted_audio", !participantCopy.muted_audio)
              }
              required={false}
            />
            <Checkbox
              title="Mute Video"
              value={participantCopy.muted_video}
              checked={participantCopy.muted_video}
              onChange={() =>
                handleChange("muted_video", !participantCopy.muted_video)
              }
              required={false}
            />
          </div>
          <Heading heading={"Current video position and size:"} />
          <div className="participantVideoSize">
            <div className="participantPosition">
              <Label title={"x: "} /> {participantCopy.position.x}
            </div>
            <div className="participantPosition">
              <Label title={"y: "} /> {participantCopy.position.y}
            </div>
            <div className="participantPosition">
              <Label title={"Width: "} /> {participantCopy.size.width}
            </div>
            <div className="participantPosition">
              <Label title={"Height: "} /> {participantCopy.size.height}
            </div>
          </div>
          <Button name="Save" onClick={() => onSaveParticipantData()} />
          <Button
            name="Back"
            design={"negative"}
            onClick={() => {
              onCloseModalWithoutData();
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default ParticipantDataModal;
