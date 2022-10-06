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
  createSession,
  getSessionsList,
  updateSession,
} from "./features/sessionsList";
import { deleteSession } from "./features/sessionsList";

import {
  BrowserRouter as Router,
  Routes,
  Route,
  useSearchParams,
} from "react-router-dom";
import { useEffect, useState } from "react";
import { getLocalStream } from "./utils/utils";
import { useSelector, useDispatch } from "react-redux";
import { ToastContainer, toast } from "react-toastify";
import { saveSession } from "./features/openSession";

function App() {
  const [localStream, setLocalStream] = useState(null);
  const [connection, setConnection] = useState(null);
  const [connectionState, setConnectionState] = useState(null);
  let [searchParams, setSearchParams] = useSearchParams();

  const sessionsList = useSelector((state) => state.sessionsList.value);
  const dispatch = useDispatch();

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
    return () => {
      connection.off("remoteStreamChange", streamChangeHandler);
      connection.off("connectionStateChange", stateChangeHandler);
    };
  }, [connection]);

  useEffect(() => {
    const closeConnection = () => {
      connection?.stop();
    };

    const sessionIdParam = searchParams.get("sessionId");
    const participantIdParam = searchParams.get("participantId");
    console.log("sessionIdParam", sessionIdParam);
    console.log("participantIdParam", participantIdParam);

    const sessionId = sessionIdParam ? sessionIdParam : "";
    const participantId = participantIdParam ? participantIdParam : "";
    const userType =
      sessionId && participantId ? "participant" : "experimenter";

    const pathname = window.location.pathname.toLowerCase();
    const isConnectionTestPage = (
      pathname === "/connectiontest" || pathname === "/connectionlatencytest"
    );

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
    if (!connection) {
      return;
    }

    connection.api.on("SESSION_LIST", handleSessionList);
    connection.api.on("DELETED_SESSION", handleDeletedSession);
    connection.api.on("CREATED_SESSION", handleCreatedSession);
    connection.api.on("UPDATED_SESSION", handleUpdatedSession);
    connection.api.on("SUCCESS", handleSuccess);
    connection.api.on("ERROR", handleError);

    return () => {
      connection.api.off("SESSION_LIST", handleSessionList);
      connection.api.off("DELETED_SESSION", handleDeletedSession);
      connection.api.off("UPDATED_SESSION", handleUpdatedSession);
      connection.api.off("CREATED_SESSION", handleCreatedSession);
      connection.api.off("SUCCESS", handleSuccess);
      connection.api.off("ERROR", handleError);
    };
  }, [connection]);

  useEffect(() => {
    if (!connection || connectionState !== ConnectionState.CONNECTED) {
      return;
    }

    connection.sendMessage("GET_SESSION_LIST", {});
  }, [connection, connectionState]);

  const onDeleteSession = (sessionId) => {
    connection.sendMessage("DELETE_SESSION", {
      session_id: sessionId,
    });
  };

  const onSendSessionToBackend = (session) => {
    connection.sendMessage("SAVE_SESSION", session);
  };

  const handleSessionList = (data) => {
    dispatch(getSessionsList(data));
  };

  const handleDeletedSession = (data) => {
    toast.success("Successfully deleted session with ID " + data);
    dispatch(deleteSession(data));
  };

  const handleUpdatedSession = (data) => {
    toast.success("Successfully updated session " + data.title);
    dispatch(updateSession(data));
    dispatch(saveSession(data));
  };

  const handleCreatedSession = (data) => {
    toast.success("Successfully created session " + data.title);
    dispatch(createSession(data));
    dispatch(saveSession(data));
  };

  const handleSuccess = (data) => {
    toast.success("SUCCESS: " + data.description);
  };

  const handleError = (data) => {
    toast.error(data.description);
  };

  const onCreateExperiment = (sessionId) => {
    connection.sendMessage("CREATE_EXPERIMENT", { session_id: sessionId });
  };

  return (
    <div className="App">
      <ToastContainer />
      {sessionsList ? (
        <Routes>
          <Route
            exact
            path="/"
            element={
              <SessionOverview
                onDeleteSession={onDeleteSession}
                onCreateExperiment={onCreateExperiment}
              />
            }
          />
          <Route
            exact
            path="/postProcessingRoom"
            element={<PostProcessing />}
          />
          <Route exact path="/experimentRoom" element={<ExperimentRoom />} />
          <Route exact path="/watchingRoom" element={<WatchingRoom />} />
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
    </div>
  );
}

export default App;
