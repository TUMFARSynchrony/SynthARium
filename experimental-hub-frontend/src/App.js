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
  const sessionId = "123";
  const participantId = "123";

  useEffect(() => {
    const asyncStreamHelper = async () => {
      const stream = await getLocalStream();
      if (stream) {
        setLocalStream(stream);
      }
      return stream;
    };

    if (connection !== null) {
      // Return if connection was already established
      return;
    }

    if (requireLocalStream) {
      // We are a participant
      const stream = asyncStreamHelper();
      setConnection(new Connection(stream, sessionId, participantId));
    } else {
      // We are a experimenter
      setConnection(new Connection());
    }
  }, [requireLocalStream, connection]);

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
