import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Typography from "@mui/material/Typography";
import { ActionButton } from "../../components/atoms/Button";
import { useState } from "react";

// This is used to take the consent of the participant before getting access to their microphone and camera.
function Consent() {
  const [openConsentDialog, setOpenConsentDialog] = useState(true);
  const [checkParticipation, setCheckParticipation] = useState(false);
  const [checkRecording, setCheckRecording] = useState(false);
  const consentTextParticipation =
    "I understand that I may terminate my participation in the study at any time.";
  const consentTextRecording =
    "I accept the recording of my audio and video and am also aware that the data will be kept anonymous and maybe used for research purposes.";

  return (
    <div className="h-screen flex flex-col mx-8 py-4 items-start text-left gap-y-4">
      <div className="header w-full pt-4">
        <div className="font-bold text-3xl">
          Synchrony Lab - {"*Experiment name*"}
        </div>
      </div>
      <div className="h-full overflow-y-scroll">
        <div className="text-justify">
          Study description... Lorem ipsum dolor sit amet, consectetur
          adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
          magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
          ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute
          irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
          fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
          sunt in culpa qui officia deserunt ollit anim id est laborum.
        </div>
        <FormControlLabel
          control={<Checkbox />}
          className="h-fit"
          label={consentTextParticipation}
          checked={checkParticipation}
          onChange={() => {
            setCheckParticipation(!checkParticipation);
          }}
        />
        <FormControlLabel
          control={<Checkbox />}
          className="h-fit"
          label={consentTextRecording}
          checked={checkRecording}
          onChange={() => {
            setCheckRecording(!checkRecording);
          }}
        />
      </div>
      <div className="self-center h-fit">
        <ActionButton
          text="I AGREE"
          variant="contained"
          onClick={() => {
            setOpenConsentDialog(!openConsentDialog);
          }}
          disabled={!checkParticipation || !checkRecording}
        />
      </div>
    </div>
  );
}

export default Consent;
