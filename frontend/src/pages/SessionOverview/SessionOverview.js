import { useEffect, useRef, useState } from "react";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { initializeSession } from "../../features/openSession";

import SessionCard from "../../components/organisms/SessionCard/SessionCard";
import "./SessionOverview.css";
import SessionPreview from "../../components/organisms/SessionPreview/SessionPreview";
import { INITIAL_SESSION_DATA } from "../../utils/constants";
import { getPastAndFutureSessions } from "../../utils/utils";
import Label from "../../components/atoms/Label/Label";
import HeroText from "../../components/atoms/HeroText/HeroText";
import ExpandMore from "@mui/icons-material/ExpandMore";
import ExpandLess from "@mui/icons-material/ExpandLess";
import { ActionIconButton, LinkButton } from "../../components/atoms/Button";

function SessionOverview({
  onDeleteSession,
  onJoinExperiment,
  onCreateExperiment,
}) {
  const dispatch = useDispatch();
  const sessionsList = useSelector((state) => state.sessionsList.value);
  const [past, setPast] = useState([]);
  const [future, setFuture] = useState([]);

  // const { past, future } = getPastAndFutureSessions(sessionsList);
  useEffect(() => {
    const { pastSession, futureSession } =
      getPastAndFutureSessions(sessionsList);
    setPast(pastSession);
    setFuture(futureSession);
    setSelectedSession(futureSession.length !== 0 ? futureSession[0] : null);
  }, [sessionsList]);

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
      <HeroText text={"Welcome! Get started with conducting your user studies here!"} />
      <LinkButton text="CREATE NEW SESSION" path="/sessionForm" variant="contained" color="primary" onClick={() => onCreateNewSession()} />
      <div className="sessionOverviewDescription">
        Create a new session to create your own experimental design template.
        You can hold these sessions for each experiment you would like to
        connect a new participant/set of participants to (link to wiki
        forexperimental workflow).
      </div>
      <div className="sessionOverviewContainer">
        <div className="sessionOverviewCards">
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
          <ActionIconButton text={showPastSessions ? "Hide past sessions" : "Show past sessions"} 
            variant="outlined" 
            color="primary"
            onClick={() => onShowPastSessions()} 
            icon={showPastSessions ? <ExpandLess /> : <ExpandMore />} />
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
        </div>
        <>
          {selectedSession ? (
            <SessionPreview
              selectedSession={selectedSession}
              setSelectedSession={setSelectedSession}
              onDeleteSession={onDeleteSession}
              onCreateExperiment={onCreateExperiment}
              onJoinExperiment={onJoinExperiment}
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
