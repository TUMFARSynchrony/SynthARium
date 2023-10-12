import { integerToDateTime } from "../../../utils/utils";
import "./Note.css";

type NoteProps = {
  content: string;
  date: number;
};

function Note({ content, date }: NoteProps) {
  return (
    <div className="noteContainer flex flex-row">
      <div className="noteDate self-end">{integerToDateTime(date)}</div>
      <div className="noteContent self-end">{content}</div>
    </div>
  );
}

export default Note;
