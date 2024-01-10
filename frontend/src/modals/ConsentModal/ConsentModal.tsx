import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Typography from "@mui/material/Typography";
import { ActionButton } from "../../components/atoms/Button";
import { useState } from "react";

// This is used to take the consent of the participant before getting access to their microphone and camera.
// TO DO: establish the participant connection with backend only after getting consent.
interface ConsentModalProps {
  onConsentGiven: (consent: boolean) => void;
}

function ConsentModal({ onConsentGiven }: ConsentModalProps) {
  const [openConsentDialog, setOpenConsentDialog] = useState(true);
  const [checkParticipation, setCheckParticipation] = useState(false);
  const [checkRecording, setCheckRecording] = useState(false);
  const consentTextParticipation =
    "I understand that I may terminate my participation in the study at any time whereupon my data will be deleted.";
  const consentTextRecording = "I accept the recording of my audio and video.";

  return (
    <Dialog open={openConsentDialog} PaperProps={{ sx: { width: "50%" } }}>
      <DialogTitle sx={{ textAlign: "center", fontWeight: "bold" }}>
        Welcome to the Ranking Task Study!
      </DialogTitle>
      <DialogContent>
        <Typography variant="body1" align="justify" sx={{ mb: 3 }}>
          By proceeding, you confirm that you have have been informed about the study purpose
          involved. You agree to the terms of consent and any questions you may have had about about
          the study have been answered until now.
        </Typography>
        <FormControlLabel
          control={<Checkbox />}
          label={consentTextRecording}
          checked={checkRecording}
          sx={{ alignItems: "flex-start" }}
          onChange={() => {
            setCheckRecording(!checkRecording);
          }}
        />
        <FormControlLabel
          control={<Checkbox />}
          label={consentTextParticipation}
          checked={checkParticipation}
          sx={{ alignItems: "flex-start" }}
          onChange={() => {
            setCheckParticipation(!checkParticipation);
          }}
        />
      </DialogContent>
      <DialogActions sx={{ alignSelf: "center" }}>
        <ActionButton
          text="I AGREE"
          variant="contained"
          color="success"
          size="medium"
          onClick={() => {
            const userConsent = checkParticipation && checkRecording;
            onConsentGiven(userConsent);
            setOpenConsentDialog(!openConsentDialog);
          }}
          disabled={!checkParticipation || !checkRecording}
        />
      </DialogActions>
    </Dialog>
  );
}

export default ConsentModal;
