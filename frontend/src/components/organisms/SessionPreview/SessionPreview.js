import { integerToDateTime, isFutureSession } from "../../../utils/utils";
import Button from "../../atoms/Button/Button";
import LinkButton from "../../atoms/LinkButton/LinkButton";
import IconButton from "../../atoms/IconButton/IconButton";
import "./SessionPreview.css";

import { useDispatch } from "react-redux";
import { copySession, initializeSession } from "../../../features/openSession";
import { createExperiment } from "../../../features/ongoingExperiment";

import { FaRegCopy, FaRegEdit, FaRegPlayCircle, FaRegTrashAlt } from "react-icons/fa";

function SessionPreview({
  selectedSession,
  setSelectedSession,
  onDeleteSession,
  onCreateExperiment,
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

  const onStartSelectedSession = () => {
    onCreateExperiment(selectedSession.id);
    dispatch(createExperiment(selectedSession));
  };

  const copyIcon = FaRegCopy, editIcon = FaRegEdit, startIcon = FaRegPlayCircle;

  return (
    <div className="sessionPreviewContainer">
      <div className="sessionPreviewHeader">
        <div>
        <h2 className="sessionPreviewTitles">{selectedSession.title}</h2>
        </div>
        <hr />
        <h4 className="sessionPreviewTitles">
          Date: {integerToDateTime(selectedSession.date)}
        </h4>
        <h4 className="sessionPreviewTitles">
          Duration: {selectedSession.time_limit / 60000} minutes
        </h4>
      </div>
      <p className="sessionPreviewInformation">{selectedSession.description}</p>
      <>
        <div className="sessionPreviewButtons">
          <Button
            name={""}
            design={"negative"}
            onClick={() => deleteSession()}
            icon={<FaRegTrashAlt />}
          />
          <IconButton
            to="/sessionForm"
            onClick={() => onCopySession()}
            IconName={copyIcon}
          />

          {isFutureSession(selectedSession) && (
            <>
              <IconButton
                to="/sessionForm"
                onClick={() => onEditSession()}
                IconName={editIcon}
              />
              <IconButton
                name={""}
                to="/watchingRoom"
                onClick={() => onStartSelectedSession()}
                IconName={startIcon}
              />
            </>
          )}
        </div>
      </>
    </div>
  );
}

export default SessionPreview;
