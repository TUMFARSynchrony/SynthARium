import { formatDate, integerToDateTime } from "../../../utils/utils";
import Button from "../../atoms/Button/Button";
import LinkButton from "../../atoms/LinkButton/LinkButton";
import "./SessionPreview.css";

import { useDispatch } from "react-redux";
import { initializeSession } from "../../../features/openSession";

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
    let copiedSession = { ...selectedSession };
    copiedSession.id = "";
    copiedSession.time_limit = copiedSession.time_limit / 60000;
    copiedSession.date = formatDate(copiedSession.date);
    console.log("copiedSession.date", copiedSession.date);
    dispatch(initializeSession(copiedSession));
  };

  const onEditSession = () => {
    let editSession = { ...selectedSession };
    editSession.time_limit = editSession.time_limit / 60000;
    editSession.date = formatDate(editSession.date);
    dispatch(initializeSession(editSession));
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
          <LinkButton
            name={"COPY"}
            to="/sessionForm"
            state={{
              initialData: selectedSession,
            }}
            onClick={() => onCopySession()}
          />
          <LinkButton
            name={"EDIT"}
            to="/sessionForm"
            state={{
              initialData: selectedSession,
            }}
            onClick={() => onEditSession()}
          />
          <LinkButton name={"START"} to="/watchingRoom" />
        </div>
        <Button
          name={"DELETE"}
          design={"negative"}
          onClick={() => deleteSession()}
        />
      </>
    </div>
  );
}

export default SessionPreview;
