import { useState } from "react";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { initializeSession } from "../../features/openSession";
import { FaAngleDown, FaAngleUp } from "react-icons/fa";

import SessionCard from "../../components/organisms/SessionCard/SessionCard";
import "./SessionOverview.css";
import NavigationBar from "../../components/organisms/NavigationBar/NavigationBar";
import SessionPreview from "../../components/organisms/SessionPreview/SessionPreview";
import LinkButton from "../../components/atoms/LinkButton/LinkButton";
import { INITIAL_SESSION_DATA } from "../../utils/constants";
import { getPastAndFutureSessions } from "../../utils/utils";
import Button from "../../components/atoms/Button/Button";
import Label from "../../components/atoms/Label/Label";

function SessionOverview({ onDeleteSession, onCreateExperiment }) {
  const dispatch = useDispatch();
  const sessionsList = useSelector((state) => state.sessionsList.value);
  const { past, future } = getPastAndFutureSessions(sessionsList);

  const [selectedSession, setSelectedSession] = useState(
    future.length !== 0 ? future[0] : null
  );

  const [showPastSessions, setShowPastSessions] = useState(false);

  const handleClick = (session) => {
    setSelectedSession(session);
  };

  const onCreateNewSession = () => {
    dispatch(initializeSession(INITIAL_SESSION_DATA));
  };

  const onShowPastSessions = () => {
    setShowPastSessions(!showPastSessions);
  };

  return (
    <>
      <NavigationBar />
      <h2 className="sessionOverviewHeadline">Welcome! Get started with conducting your user studies here!</h2>
      <div className="sessionOverviewDescription">
        Create a new session to create your own experimental design template.
        You can hold these sessions for each experiment you would like to
        connect a new participant/set of participants to (link to wiki
        forexperimental workflow).
      </div>
      <div className="sessionOverviewContainer">
        <div className="sessionOverviewCards">
          <LinkButton
            name="CREATE NEW SESSION"
            to="/sessionForm"
            onClick={() => onCreateNewSession()}
          />

          <Label title={"Upcoming sessions:"} />
          {future.length !== 0 ? (
            future.map((session, index) => {
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
          <hr className="separatorLine"></hr>
          <Button
            name={
              showPastSessions ? "Hide past sessions" : "Show past sessions"
            }
            icon={showPastSessions ? <FaAngleUp /> : <FaAngleDown />}
            design={"secondary"}
            onClick={() => onShowPastSessions()}
          />
          {showPastSessions &&
            past.length > 0 &&
            past.map((session, index) => {
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
            })}
          <hr className="separatorLine"></hr>
        </div>
        <>
          {selectedSession ? (
            <SessionPreview
              selectedSession={selectedSession}
              setSelectedSession={setSelectedSession}
              onDeleteSession={onDeleteSession}
              onCreateExperiment={onCreateExperiment}
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
