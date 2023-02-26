import { integerToDateTime, isFutureSession } from "../../../utils/utils";
import Button from "../../atoms/Button/Button";
import LinkButton from "../../atoms/LinkButton/LinkButton";
import IconButton from "../../atoms/IconButton/IconButton";
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
        "sessionPreviewContainer" +
        (selectedSession.creation_time > 0 && selectedSession.end_time === 0
          ? " ongoing"
          : "")
      }
    >
      <div className="sessionPreviewHeader">
        <div className="ongoingExperiment">
          {selectedSession.creation_time > 0 &&
            selectedSession.end_time === 0 && (
              <Heading heading={"Experiment ongoing."} />
            )}
        </div>
        <h3 className="sessionPreviewTitles">Title: {selectedSession.title}</h3>
        <hr />
        <h4 className="sessionPreviewTitles wrapper">
          Date: {integerToDateTime(selectedSession.date)}
        </h4>
        <h4 className="sessionPreviewTitles wrapper">
          Duration: {selectedSession.time_limit / 60000} minutes
        </h4>
        <h4 className="sessionPreviewTitles wrapper">
          Participant count: {selectedSession.participants.length}
        </h4>
      </div>
      <p className="sessionPreviewInformation">{selectedSession.description}</p>
      <>
        <div className="sessionPreviewButtons">
          {(selectedSession.creation_time === 0 ||
            selectedSession.end_time > 0) && (
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
          {!selectedSession.creation_time > 0 &&
            selectedSession.end_time === 0 &&
            isFutureSession(selectedSession) && (
              <>
                <LinkButton
                  name={"EDIT"}
                  to="/sessionForm"
                  onClick={() => dispatch(initializeSession(selectedSession))}
                />
                <LinkButton
                  name={"JOIN"}
                  to="/watchingRoom"
                  onClick={() => onCreateExperiment(selectedSession.id)}
                />
              </>
            )}
          {selectedSession.creation_time > 0 && selectedSession.end_time === 0 && (
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
