import { integerToDateTime, isFutureSession } from "../../../utils/utils";
import "./SessionPreview.css";

import { useDispatch } from "react-redux";
import { copySession, initializeSession } from "../../../features/openSession";
import Heading from "../../atoms/Heading/Heading";
import DeleteOutline from "@mui/icons-material/DeleteOutline";
import ContentCopy from "@mui/icons-material/ContentCopy";
import EditOutlined from "@mui/icons-material/EditOutlined";
import PlayArrowOutlined from "@mui/icons-material/PlayArrowOutlined";
import { ActionIconButton, LinkActionIconButton } from "../../atoms/Button";


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
              <ActionIconButton text="DELETE" variant="outlined" color="error" onClick={() => deleteSession()} icon={<DeleteOutline />} />
            )}
          <LinkActionIconButton
            text="DUPLICATE"
            variant="outlined"
            path="/sessionForm"
            onClick={() => dispatch(copySession(selectedSession))}
            icon={<ContentCopy />}
          />
          {!selectedSession.creation_time > 0 &&
            selectedSession.end_time === 0 &&
            isFutureSession(selectedSession) && (
              <>
                <LinkActionIconButton
                  text="EDIT"
                  variant="outlined"
                  path="/sessionForm"
                  onClick={() => dispatch(initializeSession(selectedSession))}
                  icon={<EditOutlined />}
                />
                <LinkActionIconButton
                  text="JOIN"
                  variant="contained"
                  path="/watchingRoom"
                  onClick={() => onCreateExperiment(selectedSession.id)}
                  icon={<PlayArrowOutlined />}
                />
              </>
            )}
          {selectedSession.creation_time > 0 && selectedSession.end_time === 0 && (
            <>
              <LinkActionIconButton
                text="JOIN EXPERIMENT"
                variant="contained"
                path="/watchingRoom"
                onClick={() => onJoinExperiment(selectedSession.id)}
                icon={<PlayArrowOutlined />}
              />
            </>
          )}
        </div>
      </>
    </div>
  );
}

export default SessionPreview;
