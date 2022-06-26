import { integerToDateTime, isFutureSession } from "../../../utils/utils";
import Button from "../../atoms/Button/Button";
import LinkButton from "../../atoms/LinkButton/LinkButton";
import "./SessionPreview.css";

import { useDispatch } from "react-redux";
import { copySession, initializeSession } from "../../../features/openSession";
import Heading from "../../atoms/Heading/Heading";

function SessionPreview({
  selectedSession,
  setSelectedSession,
  onDeleteSession,
  onJoinExperiment,
  onCreateExperiment,
  isOngoingExperiment,
}) {
  const dispatch = useDispatch();

  const deleteSession = () => {
    const sessionId = selectedSession.id;
    onDeleteSession(sessionId);
    setSelectedSession(null);
  };

  return (
    <div
      className={
        "sessionPreviewContainer" + (isOngoingExperiment ? " ongoing" : "")
      }
    >
      <div className="sessionPreviewHeader">
        <div className="ongoingExperiment">
          {isOngoingExperiment && <Heading heading={"Experiment ongoing."} />}
        </div>
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
          {!isOngoingExperiment && (
            <Button
              name={"DELETE"}
              design={"negative"}
              onClick={() => deleteSession()}
            />
          )}
          <LinkButton
            name={"COPY"}
            to="/sessionForm"
            onClick={() => dispatch(copySession(selectedSession))}
          />

          {!isOngoingExperiment && isFutureSession(selectedSession) && (
            <>
              <LinkButton
                name={"EDIT"}
                to="/sessionForm"
                onClick={() => dispatch(initializeSession(selectedSession))}
              />
              <LinkButton
                name={"START"}
                to="/watchingRoom"
                onClick={() => onCreateExperiment(selectedSession.id)}
              />
            </>
          )}

          {isOngoingExperiment && (
            <>
              <LinkButton
                name={"JOIN EXPERIMENT"}
                to="/watchingRoom"
                onClick={() => onJoinExperiment(selectedSession.id)}
              />
            </>
          )}
        </div>
      </>
    </div>
  );
}

export default SessionPreview;
