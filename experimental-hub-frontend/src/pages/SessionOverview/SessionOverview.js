import { useState } from "react";

import SessionCard from "../../components/organisms/SessionCard/SessionCard";
import "./SessionOverview.css";
import NavigationBar from "../../components/organisms/NavigationBar/NavigationBar";
import SessionPreview from "../../components/organisms/SessionPreview/SessionPreview";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";
import { getSessionJson } from "../../utils/mockServer";

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
          <LinkButton name="CREATE NEW SESSION" to="/sessionForm" />
          {sessionCards.length !== 0 ? (
            sessionCards.map((session, index) => {
              return (
                <SessionCard
                  title={session.title}
                  key={index}
                  date={session.date}
                  description={session.description}
                  onClick={() => handleClick(session)}
                  selected={session.title === selectedSession.title}
                />
              );
            })
          ) : (
            <>No active sessions found.</>
          )}
        </div>
        <>
          {sessionCards.length > 0 && (
            <SessionPreview sessionInformation={selectedSession} />
          )}
        </>
      </div>
    </div>
  );
}

export default SessionOverview;
