import "./NotesTab.css";
import Heading from "../../atoms/Heading/Heading";
import { useState } from "react";
import Note from "../../atoms/Note/Note";
import TextAreaField from "../TextAreaField/TextAreaField";
import { INITIAL_NOTE_DATA } from "../../../utils/constants";
import { useSelector } from "react-redux";
import { getSessionById } from "../../../utils/utils";
import { ActionIconButton } from "../../atoms/Button";
import PlayArrowOutlined from "@mui/icons-material/PlayArrowOutlined";

function NotesTab({ onAddNote }) {
  const sessionId = useSelector(
    (state) => state.ongoingExperiment.value.sessionId
  );
  const sessionsList = useSelector((state) => state.sessionsList.value);
  const sessionData = getSessionById(sessionId, sessionsList)[0];

  const [notes, setNotes] = useState(
    sessionData.notes ? sessionData.notes : []
  );
  const [noteContent, setNoteContent] = useState("");

  const onContentChange = (newContent) => {
    setNoteContent(newContent);
  };

  const onSendNotes = () => {
    if (noteContent.length === 0) {
      return;
    }

    let newNote = { ...INITIAL_NOTE_DATA };
    newNote["content"] = noteContent;
    newNote["time"] = Date.now();

    let newNoteArray = [...notes, newNote];

    setNotes(newNoteArray);
    setNoteContent("");

    onAddNote(newNote, sessionId);
  };

  return (
    <div className="notesTabContainer">
      <Heading heading={"Notes"} />
      <div className="notes">
        {notes.length > 0
          ? notes.map((note, index) => {
              return (
                <Note content={note.content} date={note.time} key={index} />
              );
            })
          : "Your notes will show up here"}
      </div>
      <>
        <div className="notesEnteringContainer">
          <hr className="separatorLine"></hr>
          <div className="notesEntering">
            <div className="notesInputField">
              <TextAreaField
                placeholder={"Enter your notes here"}
                value={noteContent}
                onChange={(newContent) => onContentChange(newContent)}
              />
            </div>
            <ActionIconButton
              text="Send"
              variant="contained"
              color="primary"
              onClick={() => onSendNotes()}
              icon={<PlayArrowOutlined />}
            />
          </div>
        </div>
      </>
    </div>
  );
}

export default NotesTab;
