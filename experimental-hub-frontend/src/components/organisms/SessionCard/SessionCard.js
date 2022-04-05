import { useState } from "react";
import "./SessionCard.css";

function SessionCard({ title, date, time, onClick, selected }) {
  // TODO: which meta information to show here additionally?
  const [selectedCardClass, setSelectedCardClass] = useState(
    "sessionCardContainer"
  );

  return (
    <div
      className={
        !selected ? "sessionCardContainer" : "sessionCardContainer active"
      }
      onClick={onClick}
    >
      <div className="sessionCardHeader">
        <h3 className="sessionCardHeaderTitle">{title}</h3>
        <h3 className="sessionCardHeaderDate">
          {date}, {time}
        </h3>
      </div>
      <p className="sessionMetaInformation">{"Some meta information"}</p>
    </div>
  );
}

export default SessionCard;
