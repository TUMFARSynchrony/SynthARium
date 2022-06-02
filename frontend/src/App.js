import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ExperimentRoom from "./pages/ExperimentRoom/ExperimentRoom";
import SessionOverview from "./pages/SessionOverview/SessionOverview";
import PostProcessing from "./pages/PostProcessing/PostProcessing";
import WatchingRoom from "./pages/WatchingRoom/WatchingRoom";
import SessionForm from "./pages/SessionForm/SessionForm";
import { useEffect, useState } from "react";
import { getLocalStream } from "./utils/utils";
import Connection from "./networking/Connection";
import ConnectionTest from "./pages/ConnectionTest/ConnectionTest";
import ConnectionState from "./networking/ConnectionState";

function App() {
  const [sessionsList, setSessionsList] = useState(null);
  const [localStream, setLocalStream] = useState(null);
  const [connection, setConnection] = useState(null);
  const [connectionState, setConnectionState] = useState(null);

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
    if (state === "CONNECTED") {
    }
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
    const asyncStreamHelper = async () => {
      const stream = await getLocalStream();
      if (stream) {
        setLocalStream(stream);
      }
    };

    if (connection?.userType === "participant" && !localStream) {
      asyncStreamHelper();
    }
  }, [localStream, connection]);

  useEffect(() => {
    const userType = "experimenter";
    const newConnection = new Connection(userType, "", "", true);
    setConnection(newConnection);

    newConnection.start();
    return () => {
      newConnection.stop();
    };
  }, [localStream]);

  useEffect(() => {
    if (!connection) {
      return;
    }

    connection.api.on("SESSION_LIST", handleSessionList);
    connection.api.on("DELETED_SESSION", handleDeletedSession);

    return () => {
      connection.api.off("SESSION_LIST", handleSessionList);
      connection.api.off("DELETED_SESSION", handleDeletedSession);
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
    setSessionsList(data);
  };

  const handleDeletedSession = (data) => {
    console.log("data", data);
  };

  return (
    <div className="App">
      {sessionsList ? (
        <Router>
          <Routes>
            <Route
              exact
              path="/"
              element={
                <SessionOverview
                  sessionsList={sessionsList}
                  onDeleteSession={onDeleteSession}
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
                    connection={connection}
                    setConnection={setConnection}
                  />
                ) : (
                  "loading"
                )
              }
            />
          </Routes>
        </Router>
      ) : (
        <h1>Loading...</h1>
      )}
    </div>
  );
}

export default App;
