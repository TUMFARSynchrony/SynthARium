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
function ConsentModal() {
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
          DESCRIPTION: You are invited to participate in a study about usability
          of the experimental hub. The study investigates the experimental hub,
          a self-hosted video conferencing tool to conduct customizable online
          experiments.
          <br />
          <br />
          TIME INVOLVEMENT: The study takes about 30min including filling out
          the survey and conducting the experiment.
          <br />
          <br />
          DATA COLLECTION: For this study, we will collect your demographics and
          evaluation using the online survey. During the study, we will record
          the video conversation through the experimental hub which will only be
          accessed by our research group team.
          <br />
          <br />
          RISKS AND BENEFITS: There are no known risk for this user study. The
          benefits would be to support me in my Master&apos;s Thesis and the
          students in our research team.
          <br />
          <br />
          PAYMENT: You will receive the opportunity to help developing a
          groundbreaking unique experimental tool that will hopefully help
          numerous researchers to conduct online experiments customized to their
          experiment requirements.
          <br />
          <br />
          PARTICIPANT&apos;S RIGHTS: If you have read this form and have decided
          to participate in this project, please understand that although your
          participation is voluntary, we would like your involvement as much as
          you can afford. That being said, you have the right to withdraw your
          consent or discontinue participation at any time without penalty or
          loss of benefits to which you are otherwise entitled. You have the
          right to refuse to answer particular questions. The results of this
          research study may be presented at scientific or professional meetings
          or published in scientific journals. Your identity is not disclosed
          unless we directly inform and ask for your permission.
          <br />
          <br />
          CONTACT INFORMATION: If you have any questions, concerns or complaints
          about this research, its procedures, risks and benefits, contact the
          following persons:
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
            setOpenConsentDialog(!openConsentDialog);
          }}
          disabled={!checkParticipation || !checkRecording}
        />
      </DialogActions>
    </Dialog>
  );
}

export default ConsentModal;
