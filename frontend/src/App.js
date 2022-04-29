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

function App() {
  const [localStream, setLocalStream] = useState(null);
  const [connection, setConnection] = useState(null);

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
    if (connection !== null) {
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
    setConnection(newConnection);
    newConnection.start();
  }, [connection, localStream, requireLocalStream]);

  return (
    <div className="App">
      <Router>
        <Routes>
          <Route exact path="/" element={<SessionOverview />} />
          <Route
            exact
            path="/postProcessingRoom"
            element={<PostProcessing />}
          />
          <Route exact path="/experimentRoom" element={<ExperimentRoom />} />
          <Route exact path="/watchingRoom" element={<WatchingRoom />} />
          <Route exact path="/sessionForm" element={<SessionForm />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;

function messageHandler(message) {
  console.log("messageHandler received:", message);
}
