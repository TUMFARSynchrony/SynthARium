import { useState } from "react";

import SessionCard from "../../components/organisms/SessionCard/SessionCard";
import { getSessionJson } from "../../mockServer/sessionJson";
import "./SessionOverview.css";
import NavigationBar from "../../components/organisms/NavigationBar/NavigationBar";
import SessionPreview from "../../components/organisms/SessionPreview/SessionPreview";
import Button from "../../components/atoms/Button/Button";
import SessionForm from "../../components/organisms/SessionForm/SessionForm";

function SessionOverview() {
  var sessionCards = getSessionJson();

  const [showFormPopup, setShowFormPopup] = useState(false);
  const [selectedSession, setSelectedSession] = useState(
    sessionCards.length !== 0 ? sessionCards[0] : null
  );

  const toggleFormPopup = () => {
    setShowFormPopup(!showFormPopup);
  };

  const handleClick = (session) => {
    setSelectedSession(session);
  };

  return (
    <div>
      <NavigationBar />
      <h2 className="sessionOverviewHeadline">Planned Sessions</h2>
      <div className="sessionOverviewContainer">
        <div className="sessionOverviewCards">
          <Button
            name={"CREATE NEW SESSION"}
            onClick={() => toggleFormPopup()}
          />
          {sessionCards.map((session) => {
            return (
              <SessionCard
                title={session.title}
                date={session.date}
                time={session.time}
                onClick={() => handleClick(session)}
                selected={session.title === selectedSession.title}
              />
            );
          })}
        </div>
        <div className="sessionOverviewCardPreview">
          <SessionPreview
            sessionInformation={selectedSession}
            onClick={toggleFormPopup}
          />
        </div>
      </div>
      {showFormPopup ? <SessionForm closePopup={toggleFormPopup} /> : null}
    </div>
  );
}

export default SessionOverview;
