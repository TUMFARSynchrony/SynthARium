import { ActionButton } from "../../components/atoms/Button";
import { useAppSelector } from "../../redux/hooks";
import { selectCurrentSession } from "../../redux/slices/sessionsListSlice";

// This is used to take the consent of the participant before getting access to their microphone and camera.
function End() {
  const session = useAppSelector(selectCurrentSession);

  // TODO: dynamic page (thank you vs end survey)
  // TODO: close the connection

  return (
    <div className="h-screen flex flex-col mx-8 py-4 items-start text-left gap-y-4 xl:items-center">
      <div className="header py-4 font-bold text-3xl xl:w-1/2">SynthARium - {session.title}</div>
      <hr className="w-screen -mx-8 border-2 border-gray-200" />
      <div className="flex flex-col h-full overflow-y-auto justify-center gap-y-4 xl:w-1/2">
        <div className="font-bold text-lg">
          {session.end_survey_title.length === 0
            ? "Thank You for Participating!"
            : session.end_survey_title}
        </div>
        <p className="text-justify">
          {session.end_survey_description.length === 0 ? (
            <div>
              This marks the end of the experiment.
              <br />
              We appreciate you taking the time to complete this study. Your insights are invaluable
              to our research!{" "}
              {session.end_survey_link.length === 0 ? (
                ""
              ) : (
                <>
                  To provide your feedback, please click on the Continue button below. The{" "}
                  <b>end survey</b> will open in a new tab. <br />
                </>
              )}
              Thank you once again for your contribution.
            </div>
          ) : (
            session.end_survey_description
          )}
        </p>
      </div>
      <div className="self-center h-fit">
        <ActionButton
          text="Continue"
          variant="contained"
          onClick={() => window.open(new URL(session.end_survey_link), "_blank")}
        />
      </div>
    </div>
  );
}

export default End;
