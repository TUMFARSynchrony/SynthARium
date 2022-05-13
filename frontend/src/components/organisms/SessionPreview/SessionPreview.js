import { integerToDateTime } from "../../../utils/utils";
import Button from "../../atoms/Button/Button";
import LinkButton from "../../atoms/LinkButton/LinkButton";
import "./SessionPreview.css";

function SessionPreview({ onDeleteSession, sessionInformation }) {
  return (
    <div className="sessionPreviewContainer">
      <div className="sessionPreviewHeader">
        <h3 className="sessionPreviewTitles">
          Title: {sessionInformation.title}
        </h3>
        <h3 className="sessionPreviewTitles">
          Date: {integerToDateTime(sessionInformation.date)}
        </h3>
        <h3 className="sessionPreviewTitles">
          Time Limit: {sessionInformation.time_limit}
        </h3>
      </div>
      <p className="sessionPreviewInformation">
        {sessionInformation.description}
      </p>
      <>
        <div className="sessionPreviewButtons">
          <LinkButton
            name={"COPY"}
            to="/sessionForm"
            state={{
              initialData: sessionInformation,
            }}
          />
          <LinkButton
            name={"EDIT"}
            to="/sessionForm"
            state={{
              initialData: sessionInformation,
            }}
          />
          <LinkButton name={"START"} to="/watchingRoom" />
        </div>
        <Button
          name={"DELETE"}
          design={"negative"}
          onClick={() => onDeleteSession(sessionInformation.id)}
        />
      </>
    </div>
  );
}

export default SessionPreview;
