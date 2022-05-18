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
import Heading from "./components/atoms/Heading/Heading";

function App() {
  const [localStream, setLocalStream] = useState(null);
  const [connection, setConnection] = useState(null);
  const [sessionsList, setSessionsList] = useState([]);
  const [sessionsLoaded, setSessionsLoaded] = useState(false);

  const requireLocalStream = window.location.pathname === "/experimentRoom";
  const sessionId = "example_session_id_1";
  const participantId = "example_user_id";

  useEffect(() => {
    const asyncStreamHelper = async () => {
      const stream = await getLocalStream();
      if (stream) {
        setLocalStream(stream);
      }
      return stream;
    };

    asyncStreamHelper();
  }, []);

  useEffect(() => {
    if (connection) {
      connection.messageHandler = messageHandler;
      // Return if connection was already established
      return;
    }

    let newConnection;
    if (requireLocalStream && localStream) {
      // We are a participant
      newConnection = new Connection(
        messageHandler,
        localStream,
        sessionId,
        participantId
      );
    } else if (!requireLocalStream) {
      // We are a experimenter
      newConnection = new Connection(messageHandler);
    } else {
      return;
    }

    const startConnection = async (newConnection) => {
      await newConnection.start();
      setConnection(newConnection);
    };

    startConnection(newConnection);
  }, [connection, localStream, requireLocalStream]);

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
      {sessionsLoaded ? (
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
          </Routes>
        </Router>
      ) : (
        <Heading heading={"Loading..."} />
      )}
    </div>
  );
}

export default App;
