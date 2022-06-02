import { integerToDateTime } from "../../../utils/utils";
import Button from "../../atoms/Button/Button";
import LinkButton from "../../atoms/LinkButton/LinkButton";
import "./SessionPreview.css";

function SessionPreview({
  selectedSession,
  setSelectedSession,
  onDeleteSession,
}) {
  const deleteSession = () => {
    const sessionId = selectedSession.id;
    onDeleteSession(sessionId);
    setSelectedSession(null);
  };

  return (
    <div className="sessionPreviewContainer">
      <div className="sessionPreviewHeader">
        <h3 className="sessionPreviewTitles">Title: {selectedSession.title}</h3>
        <h3 className="sessionPreviewTitles">
          Date: {integerToDateTime(selectedSession.date)}
        </h3>
        <h3 className="sessionPreviewTitles">
          Time Limit: {selectedSession.time_limit}
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
          />
          <LinkButton
            name={"EDIT"}
            to="/sessionForm"
            state={{
              initialData: selectedSession,
            }}
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
