import Button from "../../components/atoms/Button/Button";
import Label from "../../components/atoms/Label/Label";
import Chat from "../../components/molecules/Chat/Chat";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import { PARTICIPANT_HOST } from "../../utils/constants";

import "./JoinedParticipantModal.css";

function JoinedParticipantModal({
  participantData,
  showModal,
  setShowModal,
  sessionId,
  onMuteParticipant,
  onSendChat,
}) {
  const muteParticipant = (muteAudio, muteVideo) => {
    onMuteParticipant({
      participant_id: participantData.id,
      mute_video: muteVideo,
      mute_audio: muteAudio,
    });
  };

  return (
    <div className="joinedParticipantModalContainer">
      <div className="joinedParticipantModalData">
        <Label
          title={participantData.first_name + " " + participantData.last_name}
        />
        <hr className="separatorLine"></hr>
        <Button
          name={"Mute Audio"}
          design={"secondary"}
          onClick={() => muteParticipant(true, participantData.muted_video)}
        />
        <Button
          name={"Mute Video"}
          design={"secondary"}
          onClick={() => muteParticipant(participantData.muted_audio, true)}
        />
        <Button
          name={"Unmute"}
          design={"secondary"}
          onClick={() => muteParticipant(false, false)}
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
          <div className="joinedParticipantChat">
            <Chat
              participantId={participantData.id}
              chat={participantData.chat}
              onSendChat={onSendChat}
            />
          </div>
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
