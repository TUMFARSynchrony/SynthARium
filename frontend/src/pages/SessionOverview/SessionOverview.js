import { useEffect, useRef, useState } from "react";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { initializeSession } from "../../features/openSession";

import SessionCard from "../../components/organisms/SessionCard/SessionCard";
import SessionPreview from "../../components/organisms/SessionPreview/SessionPreview";
import { INITIAL_SESSION_DATA } from "../../utils/constants";
import { getPastAndFutureSessions } from "../../utils/utils";
import HeroText from "../../components/atoms/HeroText/HeroText";
import ExpandMore from "@mui/icons-material/ExpandMore";
import ExpandLess from "@mui/icons-material/ExpandLess";
import { ActionIconButton, LinkButton } from "../../components/atoms/Button";
import Typography from "@mui/material/Typography";
import styled from '@mui/material/styles/styled';
import Grid from "@mui/material/Grid";
import Divider from "@mui/material/Divider";
import NavigationBar from "../../components/organisms/NavigationBar/NavigationBar";


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

  const WelcomeText = styled(Typography)(({ theme }) => ({
    margin: theme.spacing(2, 4, 2, 4), // top, right, bottom, left
    fontStyle: "italic",
  }));

  const Separator = styled(Divider)(({ theme }) => ({
    borderRightWidth: 5,
  }));

  return (
    <>
      <NavigationBar />
      <HeroText text={"Synchrony Experiemental Hub"} />
      <LinkButton text="CREATE NEW EXPERIMENT" path="/sessionForm" variant="contained" color="primary" size="large" onClick={() => onCreateNewSession()} />
      <WelcomeText>
        A video conferencing tool for researchers. Create a new experimental template to start designing and hosting your next experiment. See
        <a href="https://github.com/TUMFARSynchrony/experimental-hub/wiki">Wiki</a> for more info.
      </WelcomeText>
      <Grid container>
        <Grid item sm={7} sx={{ m: 3 }}>
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
        </Grid>
        <Grid item>
          <Separator orientation="vertical" />
        </Grid>
        <Grid item sm={4} sx={{ m: 3 }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
            Upcoming sessions:
          </Typography>
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
            size="medium"
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
        </Grid>
      </Grid>
    </>
  );
}

export default SessionOverview;
