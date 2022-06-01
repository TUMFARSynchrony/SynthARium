import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ExperimentRoom from "./pages/ExperimentRoom/ExperimentRoom";
import SessionOverview from "./pages/SessionOverview/SessionOverview";
import PostProcessing from "./pages/PostProcessing/PostProcessing";
import WatchingRoom from "./pages/WatchingRoom/WatchingRoom";
import SessionForm from "./pages/SessionForm/SessionForm";
import { useEffect, useState } from "react";
import { filterListById, getLocalStream } from "./utils/utils";
import Connection from "./networking/Connection";
import ConnectionTest from "./pages/ConnectionTest/ConnectionTest";

function App() {
  const [localStream, setLocalStream] = useState(null);
  const [connection, setConnection] = useState(null);
  const [sessionsList, setSessionsList] = useState([]);
  const [sessionsLoaded, setSessionsLoaded] = useState(false);

  useEffect(() => {
    const asyncStreamHelper = async () => {
      const stream = await getLocalStream();
      if (stream) {
        setLocalStream(stream);
      }
    };

    // request local stream if requireLocalStream and localStream was not yet requested.
    if (connection?.userType === "participant" && !localStream) {
      asyncStreamHelper();
    }
  }, [localStream, connection]);

  useEffect(() => {
    const userType = "participant"; // window.location.pathname === "/experimentRoom" ? "experimenter" : "participant";
    const sessionId = "bbbef1d7d0";
    const participantId = "aa798c85d5";
    // Could be in useState initiator, but then the connection is executed twice / six times if in StrictMode.
    const newConnection = new Connection(
      userType,
      sessionId,
      participantId,
      true
    );
    setConnection(newConnection);
    return () => {
      newConnection.stop();
    };
  }, []);

  useEffect(() => {
    if (!connection) {
      return;
    }

    connection.dc.addEventListener("open", () => {
      connection.sendRequest("GET_SESSION_LIST", {});
    });
  }, [connection, connection?.dc]);

  const messageHandler = (message) => {
    if (message.type === "SESSION_LIST") {
      setSessionsList(message.data);
      setSessionsLoaded(true);
    } else if (message.type === "DELETED_SESSION") {
      let newSessionsList = filterListById(sessionsList, message.data);
      setSessionsList(newSessionsList);
    }
  };

  const onDeleteSession = (sessionId) => {
    if (!connection) {
      return;
    }

    connection.sendRequest("DELETE_SESSION", {
      session_id: sessionId,
    });
  };

  const onSendSessionToBackend = (session) => {
    connection.sendRequest("SAVE_SESSION", session);
  };

  return (
    <div className="App">
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
    </div>
  );
}

export default App;
