import { useDispatch } from "react-redux";
import Button from "../../components/atoms/Button/Button";
import Label from "../../components/atoms/Label/Label";
import Chat from "../../components/molecules/Chat/Chat";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import { banMuteUnmuteParticipant } from "../../features/sessionsList";
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
  const dispatch = useDispatch();

  const muteParticipant = (muteAudio, muteVideo) => {
    onMuteParticipant({
      participant_id: participantData.id,
      mute_video: muteVideo,
      mute_audio: muteAudio,
    });

    dispatch(
      banMuteUnmuteParticipant({
        participantId: participantData.id,
        action: "muted_audio",
        value: muteAudio,
        sessionId: sessionId,
      })
    );

    dispatch(
      banMuteUnmuteParticipant({
        participantId: participantData.id,
        action: "muted_video",
        value: muteVideo,
        sessionId: sessionId,
      })
    );
  };

  console.log("participantData", participantData);
  return (
    <div className="joinedParticipantModalContainer">
      <div className="joinedParticipantModalData">
        <Label
          title={participantData.first_name + " " + participantData.last_name}
        />
        <hr className="separatorLine"></hr>
        <Button
          name={participantData.muted_audio ? "Unmute Audio" : "Mute Audito"}
          design={"secondary"}
          onClick={() =>
            muteParticipant(
              !participantData.muted_audio,
              participantData.muted_video
            )
          }
        />
        <Button
          name={participantData.muted_video ? "Unmute Video" : "Mute Video"}
          design={"secondary"}
          onClick={() =>
            muteParticipant(
              participantData.muted_audio,
              !participantData.muted_video
            )
          }
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
          <div className="joinedParticipantChat">Chat</div>
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
