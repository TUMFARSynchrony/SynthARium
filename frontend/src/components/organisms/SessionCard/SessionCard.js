import { integerToDateTime } from "../../../utils/utils";
import "./SessionCard.css";

function SessionCard({ title, date, description, onClick, selected }) {
  return (
    <div
      className={
        !selected ? "sessionCardContainer" : "sessionCardContainer active"
      }
      onClick={onClick}
    >
      <div className="sessionCardHeader">
        <h3 className="sessionCardHeaderTitle">{title}</h3>
        <h3 className="sessionCardHeaderDate">{integerToDateTime(date)}</h3>
      </div>
      <p className="sessionMetaInformation">{description}</p>
    </div>
  );
}

export default SessionCard;
