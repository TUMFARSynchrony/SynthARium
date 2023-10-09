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
    "I understand that I may terminate my participation in the study at any time.";
  const consentTextRecording =
    "I accept the recording of my audio and video and am also aware that the data will be kept anonymous and maybe used for research purposes.";

  return (
    <Dialog open={openConsentDialog} PaperProps={{ sx: { width: "50%" } }}>
      <DialogTitle sx={{ textAlign: "center", fontWeight: "bold" }}>
        Welcome to the Synchrony Hub!
      </DialogTitle>
      <DialogContent>
        <Typography variant="body1" align="justify" sx={{ mb: 3 }}>
          Study description... Lorem ipsum dolor sit amet, consectetur
          adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
          magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
          ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute
          irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
          fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
          sunt in culpa qui officia deserunt mollit anim id est laborum.
        </Typography>
        <FormControlLabel
          control={<Checkbox />}
          label={consentTextParticipation}
          checked={checkParticipation}
          sx={{ alignItems: "flex-start" }}
          onChange={() => {
            setCheckParticipation(!checkParticipation);
          }}
        />
        <FormControlLabel
          control={<Checkbox />}
          label={consentTextRecording}
          checked={checkRecording}
          sx={{ alignItems: "flex-start" }}
          onChange={() => {
            setCheckRecording(!checkRecording);
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
