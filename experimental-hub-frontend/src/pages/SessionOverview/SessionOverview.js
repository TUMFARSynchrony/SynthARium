import { useState } from "react";

import SessionCard from "../../components/organisms/SessionCard/SessionCard";
import { getSessionJson } from "../../mockServer/sessionJson";
import "./SessionOverview.css";
import NavigationBar from "../../components/organisms/NavigationBar/NavigationBar";
import SessionPreview from "../../components/organisms/SessionPreview/SessionPreview";
import Button from "../../components/atoms/Button/Button";

function SessionOverview() {
  var sessionCards = getSessionJson();

  const [selectedSession, setSelectedSession] = useState(
    sessionCards.length !== 0 ? sessionCards[0] : null
  );

  const handleClick = (session) => {
    setSelectedSession(session);
  };

  return (
    <div>
      <NavigationBar />
      <h2 className="sessionOverviewHeadline">Planned Sessions</h2>
      <div className="sessionOverviewContainer">
        <div className="sessionOverviewCards">
          <Button name={"CREATE NEW SESSION"} to="/" />
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
          <SessionPreview sessionInformation={selectedSession} />
        </div>
      </div>
    </div>
  );
}

export default SessionOverview;
