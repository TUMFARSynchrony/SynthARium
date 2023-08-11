import { ActionButton } from "../../components/atoms/Button";
import Label from "../../components/atoms/Label/Label";
import InputTextField from "../../components/molecules/InputTextField/InputTextField";
import { PARTICIPANT_HOST } from "../../utils/constants";

import { useAppDispatch } from "../../redux/hooks";
import { banMuteUnmuteParticipant } from "../../redux/slices/sessionsListSlice";
import "./JoinedParticipantModal.css";
import { Participant } from "../../types";
import { BanMuteUnmuteActions } from "../../utils/enums";

type Props = {
  participantData: Participant;
  showModal: boolean;
  setShowModal: React.Dispatch<React.SetStateAction<boolean>>;
  sessionId: string;
  onMuteParticipant: (data: any) => void;
};

function JoinedParticipantModal({
  participantData,
  showModal,
  setShowModal,
  sessionId,
  onMuteParticipant
}: Props) {
  const dispatch = useAppDispatch();

  const muteParticipant = (muteAudio: boolean, muteVideo: boolean) => {
    onMuteParticipant({
      participant_id: participantData.id,
      mute_video: muteVideo,
      mute_audio: muteAudio
    });

    dispatch(
      banMuteUnmuteParticipant({
        participantId: participantData.id,
        action: BanMuteUnmuteActions.MUTED_AUDIO,
        value: muteAudio,
        sessionId: sessionId
      })
    );

    dispatch(
      banMuteUnmuteParticipant({
        participantId: participantData.id,
        action: BanMuteUnmuteActions.MUTED_VIDEO,
        value: muteVideo,
        sessionId: sessionId
      })
    );
  };

  console.log("participantData", participantData);
  return (
    <div className="joinedParticipantModalContainer">
      <div className="joinedParticipantModalData">
        <Label title={participantData.participant_name} />
        <hr className="separatorLine"></hr>
        <ActionButton
          text={participantData.muted_audio ? "Unmute Audio" : "Mute Audio"}
          variant="outlined"
          color="primary"
          size="medium"
          onClick={() =>
            muteParticipant(
              !participantData.muted_audio,
              participantData.muted_video
            )
          }
        />
        <ActionButton
          text={participantData.muted_video ? "Unmute Video" : "Mute Video"}
          variant="outlined"
          color="primary"
          size="medium"
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
          <ActionButton
            text="Cancel"
            variant="outlined"
            color="primary"
            size="medium"
            onClick={() => setShowModal(!showModal)}
          />
          <ActionButton
            text="Finish"
            variant="outlined"
            color="success"
            size="medium"
            onClick={() => setShowModal(!showModal)}
          />
        </div>
      </div>
    </div>
  );
}

export default JoinedParticipantModal;
