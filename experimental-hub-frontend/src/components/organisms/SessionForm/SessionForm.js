import Button from "../../atoms/Button/Button";
import "./SessionForm.css";

function SessionForm({ closePopup }) {
  return (
    <div className="sessionFormContainer">
      <Button name="Close me" onClick={closePopup} />
    </div>
  );
}

export default SessionForm;
