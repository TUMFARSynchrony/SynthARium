import { Link } from "react-router-dom";
import "./MainPage.css";

function MainPage() {
  return (
    <div>
      <h1>Main Page</h1>
      <Link to="/sessionOverview">Session Overview</Link>
      <Link to="/watchingRoom">Watching Room</Link>
      <Link to="/postProcessingRoom">Post-Processing Room</Link>
    </div>
  );
}

export default MainPage;
