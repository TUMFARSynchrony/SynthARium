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

function App() {
  const userType = "experimenter" // window.location.pathname === "/experimentRoom" ? "experimenter" : "participant";
  const sessionId = "bbbef1d7d0";
  const participantId = "ef798c85d5";

  const [localStream, setLocalStream] = useState(null);
  const [connection, setConnection] = useState(new Connection(userType, sessionId, participantId));

  useEffect(() => {
    const asyncStreamHelper = async () => {
      const stream = await getLocalStream();
      if (stream) {
        setLocalStream(stream);
      }
    };

    // request local stream if requireLocalStream and localStream was not yet requested. 
    if (userType === "participant" && !localStream) {
      asyncStreamHelper();
    }
  }, [localStream]);

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
          <Route exact path="/connectionTest" element={
            <ConnectionTest localStream={localStream} connection={connection} />
          } />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
