import { integerToDateTime } from "../../../utils/utils";
import "./Note.css";

function Note({ content, date }) {
  return (
    <div className="noteContainer">
      <div className="noteDate">{integerToDateTime(date)}</div>
      <div className="noteContent">{content}</div>
    </div>
  );
}

export default Note;
