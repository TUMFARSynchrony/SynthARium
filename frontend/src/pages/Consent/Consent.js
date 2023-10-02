import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import { ActionButton } from "../../components/atoms/Button";
import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useAppSelector } from "../../redux/hooks";
import { selectCurrentSession } from "../../redux/slices/sessionsListSlice";

// This is used to take the consent of the participant before getting access to their microphone and camera.
function Consent() {
  const [checkParticipation, setCheckParticipation] = useState(false);
  const [checkRecording, setCheckRecording] = useState(false);
  const consentTextParticipation =
    "I understand that I may terminate my participation in the study at any time.";
  const consentTextRecording =
    "I accept the recording of my audio and video and am also aware that the data will be kept anonymous and maybe used for research purposes.";
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionId = searchParams.get("sessionId");
  const participantId = searchParams.get("participantId");
  const session = useAppSelector(selectCurrentSession);
    //TODO: dynamic page (experiment name) - find a way to get the information without actually streaming in the session

  return (
    <div className="h-screen flex flex-col mx-8 py-4 items-start text-left gap-y-4 xl:items-center">
      <div className="header py-4 font-bold text-3xl xl:w-1/2">
        Synchrony Lab - {}
      </div>
      <hr className="w-screen -mx-8 border-2 border-gray-200" />
      <div className="flex flex-col h-full overflow-y-auto justify-center gap-y-4 xl:w-1/2">
        <div className="font-bold text-lg">Consent Form</div>
        <p className="text-justify">
          Study description... Lorem ipsum dolor sit amet, consectetur
          adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
          magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
          ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute
          irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
          fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
          sunt in culpa qui officia deserunt ollit anim id est laborum.
        </p>
        <div className="flex flex-col">
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
      </div>
      <div className="self-center h-fit">
        <a
          href={`${window.location.origin}/lobby?participantId=${participantId}&sessionId=${sessionId}`}
          className={
            !checkParticipation || !checkRecording ? "pointer-events-none" : ""
          }
        >
          <ActionButton
            text="Continue"
            variant="contained"
            disabled={!checkParticipation || !checkRecording}
          />
        </a>
      </div>
    </div>
  );
}

export default Consent;
