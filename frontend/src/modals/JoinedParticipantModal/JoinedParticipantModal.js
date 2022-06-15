import Button from "../../components/atoms/Button/Button";
import Label from "../../components/atoms/Label/Label";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import { PARTICIPANT_HOST } from "../../utils/constants";

import "./JoinedParticipantModal.css";

function JoinedParticipantModal({
  participantData,
  showModal,
  setShowModal,
  sessionId,
}) {
  return (
    <div className="joinedParticipantModalContainer">
      <div className="joinedParticipantModalData">
        <Label
          title={participantData.first_name + " " + participantData.last_name}
        />
        <hr className="separatorLine"></hr>

        <div className="joinedParticipantModalInfo">
          <InputTextField
            title="Link"
            readonly={true}
            value={`${PARTICIPANT_HOST}?participantId=${participantData.id}&sessionId=${sessionId}`}
          />
          <div className="participantPosition">
            <Label title={"x: "} /> {participantData.position.x}
          </div>
          <div className="participantPosition">
            <Label title={"y: "} /> {participantData.position.y}
          </div>
          <div className="participantPosition">
            <Label title={"Width: "} /> {participantData.size.width}
          </div>
          <div className="participantPosition">
            <Label title={"Height: "} /> {participantData.size.height}
          </div>
        </div>
        <hr className="separatorLine"></hr>
        <div className="joinedParticipantActions">
          <div className="joinedParticipantFilters">Filter List</div>
          <div className="joinedParticipantChat">Chat with participant</div>
        </div>
        <hr className="separatorLine"></hr>
        <div className="joinedParticipantButtons">
          <Button
            name={"Cancel"}
            design={"negative"}
            onClick={() => setShowModal(!showModal)}
          />
          <Button
            name={"Finish"}
            design={"positive"}
            onClick={() => setShowModal(!showModal)}
          />
        </div>
      </div>
    </div>
  );
}

export default JoinedParticipantModal;
