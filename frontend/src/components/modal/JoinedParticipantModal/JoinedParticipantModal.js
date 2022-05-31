import Label from "../../atoms/Label/Label";
import Button from "../../atoms/Button/Button";
import InputTextField from "../../molecules/InputTextField/InputTextField";
import "./JoinedParticipantModal.css";

function JoinedParticipantModal({ participantData, showModal, setShowModal }) {
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
            value={participantData.link}
            readonly={true}
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
