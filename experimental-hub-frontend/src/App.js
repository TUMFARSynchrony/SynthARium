import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ExperimentRoom from "./pages/participant-pov/ExperimentRoom/ExperimentRoom";
import MainPage from "./pages/researcher-pov/MainPage/MainPage";
import PostProcessing from "./pages/researcher-pov/PostProcessing/PostProcessing";
import WatchingRoom from "./pages/researcher-pov/WatchingRoom/WatchingRoom";
import SessionOverview from "./pages/researcher-pov/SessionOverview/SessionOverview";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route exact path="/" element={<MainPage />} />
          <Route
            exact
            path="/postProcessingRoom"
            element={<PostProcessing />}
          />
          <Route exact path="/watchingRoom" element={<WatchingRoom />} />
          <Route exact path="/experimentRoom" element={<ExperimentRoom />} />
          <Route exact path="/sessionOverview" element={<SessionOverview />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
