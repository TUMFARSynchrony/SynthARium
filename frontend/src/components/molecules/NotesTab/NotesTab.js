import "./NotesTab.css";
import Heading from "../../atoms/Heading/Heading";
import { useState } from "react";
import Note from "../../atoms/Note/Note";
import TextField from "../TextField/TextField";
import Button from "../../atoms/Button/Button";
import { INITIAL_NOTE_DATA } from "../../../utils/constants";

function NotesTab() {
  const [notes, setNotes] = useState([]);
  const [noteContent, setNoteContent] = useState("");

  const onContentChange = (newContent) => {
    setNoteContent(newContent);
  };

  const onSendNotes = () => {
    if (noteContent.length === 0) {
      return;
    }

    let newNote = {
      ...INITIAL_NOTE_DATA,
      content: noteContent,
      date: Date.now(),
    };
    let newNoteArray = [...notes, newNote];

    setNotes(newNoteArray);
    setNoteContent("");
  };

  return (
    <div className="notesTabContainer">
      <Heading heading={"Notes"} />
      <div className="notes">
        {notes.length > 0
          ? notes.map((note, index) => {
              return (
                <Note content={note.content} date={note.date} key={index} />
              );
            })
          : "Your notes will show up here"}
      </div>
      <>
        <div className="notesEnteringContainer">
          <hr className="separatorLine"></hr>
          <div className="notesEntering">
            <div className="notesInputField">
              <TextField
                placeholder={"Enter your notes here"}
                value={noteContent}
                onChange={(newContent) => onContentChange(newContent)}
              />
            </div>
            <Button
              name={"Send"}
              design={"secondary"}
              onClick={() => onSendNotes()}
            />
          </div>
        </div>
      </>
    </div>
  );
}

export default NotesTab;
