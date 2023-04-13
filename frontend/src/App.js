import "./App.css";
import ExperimentRoom from "./pages/ExperimentRoom/ExperimentRoom";
import SessionOverview from "./pages/SessionOverview/SessionOverview";
import PostProcessing from "./pages/PostProcessing/PostProcessing";
import WatchingRoom from "./pages/WatchingRoom/WatchingRoom";
import SessionForm from "./pages/SessionForm/SessionForm";
import Connection from "./networking/Connection";
import ConnectionTest from "./pages/ConnectionTest/ConnectionTest";
import ConnectionLatencyTest from "./pages/ConnectionLatencyTest/ConnectionLatencyTest";
import ConnectionState from "./networking/ConnectionState";
import {
  addNote,
  createSession,
  getSessionsList,
  updateSession,
  setExperimentTimes,
} from "./features/sessionsList";
import { deleteSession } from "./features/sessionsList";

import { Routes, Route, useSearchParams } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { getLocalStream, getSessionById } from "./utils/utils";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { saveSession } from "./features/openSession";
import CustomSnackbar from "./components/atoms/CustomSnackbar/CustomSnackbar";
import {
  changeExperimentState,
  createExperiment,
  joinExperiment,
} from "./features/ongoingExperiment";
import { initialSnackbar } from "./utils/constants";


function App() {
  const [localStream, setLocalStream] = useState(null);
  const [connection, setConnection] = useState(null);
  const [connectionState, setConnectionState] = useState(null);
  const [connectedParticipants, setConnectedParticipants] = useState([]);
  let [searchParams, setSearchParams] = useSearchParams();
  const sessionsList = useSelector((state) => state.sessionsList.value);
  const ongoingExperiment = useSelector(
    (state) => state.ongoingExperiment.value
  );

  const sessionsListRef = useRef();
  sessionsListRef.current = sessionsList;
  const ongoingExperimentRef = useRef();
  ongoingExperimentRef.current = ongoingExperiment;
  const [snackbar, setSnackbar] = useState(initialSnackbar);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const connectedPeersChangeHandler = async (peers) => {
    console.groupCollapsed(
      "%cConnection peer streams change Handler",
      "color:blue"
    );
    console.log(peers);
    console.groupEnd();
    setConnectedParticipants(peers);
  };

  const streamChangeHandler = async (_) => {
    console.log("%cRemote Stream Change Handler", "color:blue");
  };

  /** Handle `connectionStateChange` event of {@link Connection}. */
  const stateChangeHandler = async (state) => {
    console.log(
      `%cConnection state change Handler: ${ConnectionState[state]}`,
      "color:blue"
    );

    setConnectionState(state);
  };

  // Register Connection event handlers
  useEffect(() => {
    if (!connection) {
      return;
    }

    connection.on("remoteStreamChange", streamChangeHandler);
    connection.on("connectionStateChange", stateChangeHandler);
    connection.on("connectedPeersChange", connectedPeersChangeHandler);

    connection.api.on("SESSION_LIST", handleSessionList);
    connection.api.on("DELETED_SESSION", handleDeletedSession);
    connection.api.on("SAVED_SESSION", handleSavedSession);
    connection.api.on("SESSION_CHANGE", handleSessionChange);
    connection.api.on("SUCCESS", handleSuccess);
    connection.api.on("ERROR", handleError);
    connection.api.on("EXPERIMENT_CREATED", handleExperimentCreated);
    connection.api.on("EXPERIMENT_STARTED", handleExperimentStarted);
    connection.api.on("EXPERIMENT_ENDED", handleExperimentEnded);

    return () => {
      connection.off("remoteStreamChange", streamChangeHandler);
      connection.off("connectionStateChange", stateChangeHandler);
      connection.off("connectedPeersChange", connectedPeersChangeHandler);

      connection.api.off("SESSION_LIST", handleSessionList);
      connection.api.off("DELETED_SESSION", handleDeletedSession);
      connection.api.off("SAVED_SESSION", handleSavedSession);
      connection.api.off("SESSION_CHANGE", handleSessionChange);
      connection.api.off("SUCCESS", handleSuccess);
      connection.api.off("ERROR", handleError);
      connection.api.off("EXPERIMENT_CREATED", handleExperimentCreated);
      connection.api.off("EXPERIMENT_STARTED", handleExperimentStarted);
      connection.api.off("EXPERIMENT_ENDED", handleExperimentEnded);
    };
  }, [connection]);

  useEffect(() => {
    const closeConnection = () => {
      connection?.stop();
    };

    const sessionIdParam = searchParams.get("sessionId");
    const participantIdParam = searchParams.get("participantId");
    const experimenterPasswordParam = searchParams.get("experimenterPassword");

    const sessionId = sessionIdParam ? sessionIdParam : "";
    const participantId = participantIdParam ? participantIdParam : "";
    let experimenterPassword = experimenterPasswordParam ?? "";
    const userType =
      sessionId && participantId ? "participant" : "experimenter";

    const pathname = window.location.pathname.toLowerCase();
    const isConnectionTestPage = pathname === "/connectiontest" || pathname === "/connectionlatencytest";

    //   // TODO: get experimenter password before creating Connection, e.g. from "login" page
    //   // The following solution using `prompt` is only a placeholder.
    if (
      !isConnectionTestPage &&
      userType === "experimenter" &&
      !experimenterPassword
    ) {
      //experimenterPassword = prompt("Please insert experimenter password");
      experimenterPassword = "no-password-given";
    }

    const asyncStreamHelper = async (connection) => {
      const stream = await getLocalStream();
      if (stream) {
        setLocalStream(stream);
        // Start connection if current page is not connection test page
        if (!isConnectionTestPage) {
          connection.start(stream);
        }
      }
    };

    const newConnection = new Connection(
      userType,
      sessionId,
      participantId,
      experimenterPassword || "no-password-given", // "no-password-given" is a placeholder if experimenterPassword is an empty string
      true
    );

    setConnection(newConnection);
    if (userType === "participant" && pathname !== "/connectionlatencytest") {
      asyncStreamHelper(newConnection);
      return;
    }

    // Start connection if current page is not connection test page
    if (!isConnectionTestPage) {
      newConnection.start();
    }

    window.addEventListener("beforeunload", closeConnection);

    return () => {
      window.removeEventListener("beforeunload", closeConnection);
      closeConnection();
    };
  }, []);

  useEffect(() => {
    if (!connection || connectionState !== ConnectionState.CONNECTED) {
      return;
    }

    connection.sendMessage("GET_SESSION_LIST", {});
  }, [connection, connectionState]);

  const handleSessionList = (data) => {
    dispatch(getSessionsList(data));
  };

  const handleDeletedSession = (data) => {
    setSnackbar({ open: true, text: `Successfully deleted session with ID ${data}`, severity: "success" });
    dispatch(deleteSession(data));
  };

  const handleSavedSession = (data) => {
    navigate("/");
    if (getSessionById(data.id, sessionsListRef.current).length === 0) {
      setSnackbar({ open: true, text: `Successfully created session ${data.title}`, severity: "success" });
      dispatch(createSession(data));
    } else {
      setSnackbar({ open: true, text: `Successfully updated session ${data.title}`, severity: "success" });
      dispatch(updateSession(data));
    }

    dispatch(saveSession(data));
  };

  const handleSuccess = (data) => {
    setSnackbar({ open: true, text: `SUCCESS: ${data.description}`, severity: "success" });
  };

  const handleError = (data) => {
    setSnackbar({ open: true, text: `${data.description}`, severity: "error" });
  };

  const handleSessionChange = (data) => {
    if (getSessionById(data.id, sessionsListRef.current).length === 0) {
      dispatch(createSession(data));
    } else {
      dispatch(updateSession(data));
    }
  };

  const handleExperimentCreated = (data) => {
    dispatch(
      setExperimentTimes({
        action: "creation_time",
        value: data.creation_time,
        sessionId: data.session_id,
      })
    );
  };

  const handleExperimentStarted = (data) => {
    dispatch(
      setExperimentTimes({
        action: "start_time",
        value: data.start_time,
        sessionId: ongoingExperimentRef.current.sessionId,
      })
    );
  };

  const handleExperimentEnded = (data) => {
    dispatch(
      setExperimentTimes({
        action: "end_time",
        value: data.end_time,
        sessionId: ongoingExperimentRef.current.sessionId,
      })
    );

    dispatch(
      setExperimentTimes({
        action: "start_time",
        value: data.start_time,
        sessionId: ongoingExperimentRef.current.sessionId,
      })
    );
  };

  const onCreateExperiment = (sessionId) => {
    connection.sendMessage("CREATE_EXPERIMENT", { session_id: sessionId });
    dispatch(createExperiment(sessionId)); // Initialize ongoingExperiment redux slice
  };

  const onDeleteSession = (sessionId) => {
    connection.sendMessage("DELETE_SESSION", {
      session_id: sessionId,
    });
  };

  const onSendSessionToBackend = (session) => {
    connection.sendMessage("SAVE_SESSION", session);
  };

  const onKickBanParticipant = (participant, action) => {
    if (action === "Kick") {
      connection.sendMessage("KICK_PARTICIPANT", participant);
    } else {
      connection.sendMessage("BAN_PARTICIPANT", participant);
    }
  };

  const onJoinExperiment = (sessionId) => {
    connection.sendMessage("JOIN_EXPERIMENT", { session_id: sessionId });
    dispatch(joinExperiment(sessionId));
  };

  const onAddNote = (note, sessionId) => {
    connection.sendMessage("ADD_NOTE", note);
    dispatch(addNote({ note: note, id: sessionId }));
  };

  const onLeaveExperiment = () => {
    connection.sendMessage("LEAVE_EXPERIMENT", {});
  };

  const onMuteParticipant = (muteRequest) => {
    connection.sendMessage("MUTE", muteRequest);
  };

  const onStartExperiment = () => {
    connection.sendMessage("START_EXPERIMENT", {});
    dispatch(changeExperimentState("ONGOING"));
  };

  const onEndExperiment = () => {
    connection.sendMessage("STOP_EXPERIMENT", {});
  };

  return (
    <div className="App">
      {sessionsList ? (
        <Routes>
          <Route
            exact
            path="/"
            element={
              <SessionOverview
                onDeleteSession={onDeleteSession}
                onCreateExperiment={onCreateExperiment}
                onJoinExperiment={onJoinExperiment}
              />
            }
          />
          <Route
            exact
            path="/postProcessingRoom"
            element={<PostProcessing />}
          />
          <Route
            exact
            path="/experimentRoom"
            element={
              connection ? (
                <ExperimentRoom
                  localStream={localStream}
                  connection={connection}
                />
              ) : (
                "Loading..."
              )
            }
          />
          <Route
            exact
            path="/watchingRoom"
            element={
              <WatchingRoom
                connectedParticipants={connectedParticipants}
                onKickBanParticipant={onKickBanParticipant}
                onAddNote={onAddNote}
                onLeaveExperiment={onLeaveExperiment}
                onMuteParticipant={onMuteParticipant}
                onStartExperiment={onStartExperiment}
                onEndExperiment={onEndExperiment}
              />
            }
          />
          <Route
            exact
            path="/sessionForm"
            element={
              <SessionForm onSendSessionToBackend={onSendSessionToBackend} />
            }
          />
          <Route
            exact
            path="/connectionTest"
            element={
              connection ? (
                <ConnectionTest
                  localStream={localStream}
                  setLocalStream={setLocalStream}
                  connection={connection}
                  setConnection={setConnection}
                />
              ) : (
                "loading"
              )
            }
          />
          <Route
            exact
            path="/connectionLatencyTest"
            element={
              connection ? (
                <ConnectionLatencyTest
                  localStream={localStream}
                  setLocalStream={setLocalStream}
                  connection={connection}
                />
              ) : (
                "loading"
              )
            }
          />
        </Routes>
      ) : (
        <h1>Loading...</h1>
      )}
      <CustomSnackbar open={snackbar.open} text={snackbar.text} severity={snackbar.severity}
        handleClose={() => setSnackbar(initialSnackbar)} />
    </div>
  );
}

export default App;
