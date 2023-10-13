import { useState } from "react";
import { ActionButton } from "../../components/atoms/Button";
import CustomSnackbar from "../../components/atoms/CustomSnackbar/CustomSnackbar";
import TextAreaField from "../../components/molecules/TextAreaField/TextAreaField";
import { useAppDispatch } from "../../redux/hooks";
import { banMuteUnmuteParticipant } from "../../redux/slices/sessionsListSlice";
import { initialSnackbar } from "../../utils/constants";
import "./KickParticipantModal.css";
import { BanMuteUnmuteActions } from "../../utils/enums";

type KickParticipant = {
  participant_id: string;
  reason: string;
};

type Props = {
  participantId: string;
  sessionId: string;
  showModal: boolean;
  setShowModal: React.Dispatch<React.SetStateAction<boolean>>;
  onKickBanParticipant: (participant: KickParticipant, action: string) => void;
  action: string;
};

function KickParticipantModal({
  participantId,
  sessionId,
  showModal,
  setShowModal,
  onKickBanParticipant,
  action
}: Props) {
  const [reason, setReason] = useState("");
  const dispatch = useAppDispatch();
  const [snackbar, setSnackbar] = useState(initialSnackbar);

  const onChange = (newReason: string) => {
    setReason(newReason);
  };

  const kickBanParticipant = () => {
    if (!reason) {
      setSnackbar({
        open: true,
        text: "Please specify the reason!",
        severity: "warning"
      });
      return;
    }

    onKickBanParticipant(
      {
        participant_id: participantId,
        reason
      },
      action
    );
    setShowModal(!showModal);

    if (action === "Ban") {
      dispatch(
        banMuteUnmuteParticipant({
          participantId,
          action: BanMuteUnmuteActions.BANNED,
          value: true,
          sessionId
        })
      );
    }
  };

  return (
    <div className="kickParticipantModalContainer">
      <div className="kickParticipantModal">
        <TextAreaField
          title="Enter your reason for kicking/banning here:"
          value={reason}
          placeholder=""
          onChange={(newReason: string) => onChange(newReason)}
          required
        />
        <ActionButton
          variant="contained"
          color="error"
          size="medium"
          text={action}
          onClick={() => kickBanParticipant()}
        />
        <ActionButton
          text="Cancel"
          variant="contained"
          color="primary"
          size="medium"
          onClick={() => setShowModal(false)}
        />
      </div>
      <CustomSnackbar
        open={snackbar.open}
        text={snackbar.text}
        severity={snackbar.severity}
        handleClose={() => setSnackbar(initialSnackbar)}
      />
    </div>
  );
}

export default KickParticipantModal;
