import { integerToDateTime } from "../../../utils/utils";
import "./Note.css";

type NoteProps = {
  content: string;
  date: number;
};

function Note({ content, date }: NoteProps) {
  return (
    <div className="noteContainer">
      <div className="noteDate">{integerToDateTime(date)}</div>
      <div className="noteContent">{content}</div>
    </div>
  );
}

export default Note;
