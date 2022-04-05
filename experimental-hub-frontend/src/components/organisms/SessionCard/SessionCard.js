import "./SessionCard.css";

function SessionCard({ title, date, time }) {
  // TODO: which meta information to show here additionally?
  return (
    <div className="sessionCardContainer">
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
