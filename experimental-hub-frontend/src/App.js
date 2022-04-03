import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainPage from "./pages/MainPage/MainPage";
import WatchingRoom from "./pages/WatchingRoom/WatchingRoom";
import ExperimentRoom from "./pages/ExperimentRoom/ExperimentRoom";
import SessionOverview from "./pages/SessionOverview/SessionOverview";
import PostProcessing from "./pages/PostProcessing/PostProcessing";

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
