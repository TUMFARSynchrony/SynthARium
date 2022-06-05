import { useState } from "react";
import { useSelector } from "react-redux";

import SessionCard from "../../components/organisms/SessionCard/SessionCard";
import "./SessionOverview.css";
import NavigationBar from "../../components/organisms/NavigationBar/NavigationBar";
import SessionPreview from "../../components/organisms/SessionPreview/SessionPreview";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";
import { INITIAL_SESSION_DATA } from "../../utils/constants";

function SessionOverview({ onDeleteSession }) {
  const sessionsList = useSelector((state) => state.sessionsList.value);

  const [selectedSession, setSelectedSession] = useState(
    sessionsList.length !== 0 ? sessionsList[0] : null
  );

  const handleClick = (session) => {
    setSelectedSession(session);
  };

  return (
    <>
      <NavigationBar />
      <h2 className="sessionOverviewHeadline">Planned Sessions</h2>
      <div className="sessionOverviewContainer">
        <div className="sessionOverviewCards">
          <LinkButton
            name="CREATE NEW SESSION"
            to="/sessionForm"
            state={{
              initialData: INITIAL_SESSION_DATA,
            }}
          />
          {sessionsList?.length !== 0 ? (
            sessionsList?.map((session, index) => {
              return (
                <SessionCard
                  title={session.title}
                  key={index}
                  date={session.date}
                  description={session.description}
                  onClick={() => handleClick(session)}
                  selected={session.id === selectedSession?.id}
                />
              );
            })
          ) : (
            <>No active sessions found.</>
          )}
        </div>
        <>
          {selectedSession ? (
            <SessionPreview
              selectedSession={selectedSession}
              setSelectedSession={setSelectedSession}
              onDeleteSession={onDeleteSession}
            />
          ) : (
            <h2>No session selected.</h2>
          )}
        </>
      </div>
    </>
  );
}

export default SessionOverview;
