import { useState } from "react";

import SessionCard from "../../components/organisms/SessionCard/SessionCard";
import {
  getEmptySessionJson,
  getSessionJson,
} from "../../mockServer/sessionJson";
import "./SessionOverview.css";
import NavigationBar from "../../components/organisms/NavigationBar/NavigationBar";
import SessionPreview from "../../components/organisms/SessionPreview/SessionPreview";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";

function SessionOverview() {
  //TODO: Dropdown for past Sessions
  var sessionCards = getSessionJson();

  const [showFormPopup, setShowFormPopup] = useState(false);
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
          <LinkButton name="CREATE NEW SESSION" to="/sessionForm" />
          {sessionCards.length !== 0 ? (
            sessionCards.map((session) => {
              return (
                <SessionCard
                  title={session.title}
                  date={session.date}
                  time={session.time}
                  onClick={() => handleClick(session)}
                  selected={session.title === selectedSession.title}
                />
              );
            })
          ) : (
            <div>No active sessions found.</div>
          )}
        </div>
        <div className="sessionOverviewCardPreview">
          {sessionCards.length > 0 && (
            <SessionPreview sessionInformation={selectedSession} />
          )}
        </div>
      </div>
    </div>
  );
}

export default SessionOverview;
