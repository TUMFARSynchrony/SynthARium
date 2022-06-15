import { integerToDateTime, isFutureSession } from "../../../utils/utils";
import Button from "../../atoms/Button/Button";
import LinkButton from "../../atoms/LinkButton/LinkButton";
import "./SessionPreview.css";

import { useDispatch } from "react-redux";
import { copySession, initializeSession } from "../../../features/openSession";
import { createExperiment } from "../../../features/ongoingExperiment";

function SessionPreview({
  selectedSession,
  setSelectedSession,
  onDeleteSession,
}) {
  const dispatch = useDispatch();

  const deleteSession = () => {
    const sessionId = selectedSession.id;
    onDeleteSession(sessionId);
    setSelectedSession(null);
  };

  const onCopySession = () => {
    dispatch(copySession(selectedSession));
  };

  const onEditSession = () => {
    dispatch(initializeSession(selectedSession));
  };

  const onCreateExperiment = () => {
    dispatch(createExperiment(selectedSession));
  };

  return (
    <div className="sessionPreviewContainer">
      <div className="sessionPreviewHeader">
        <h3 className="sessionPreviewTitles">Title: {selectedSession.title}</h3>
        <h3 className="sessionPreviewTitles">
          Date: {integerToDateTime(selectedSession.date)}
        </h3>
        <h3 className="sessionPreviewTitles">
          Time Limit: {selectedSession.time_limit / 60000} minutes
        </h3>
      </div>
      <p className="sessionPreviewInformation">{selectedSession.description}</p>
      <>
        <div className="sessionPreviewButtons">
          <Button
            name={"DELETE"}
            design={"negative"}
            onClick={() => deleteSession()}
          />
          <LinkButton
            name={"COPY"}
            to="/sessionForm"
            onClick={() => onCopySession()}
          />

          {isFutureSession(selectedSession) && (
            <>
              <LinkButton
                name={"EDIT"}
                to="/sessionForm"
                onClick={() => onEditSession()}
              />
              <LinkButton
                name={"START"}
                to="/watchingRoom"
                onClick={() => onCreateExperiment()}
              />
            </>
          )}
        </div>
      </>
    </div>
  );
}

export default SessionPreview;
