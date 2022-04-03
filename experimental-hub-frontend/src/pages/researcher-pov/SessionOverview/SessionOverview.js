import { Link } from "react-router-dom";
import "./SessionOverview.css";

function SessionOverview() {
  return (
    <div>
      <h1>Session Overview</h1>
      <Link to="/">
        <span>Main Page</span>
      </Link>
    </div>
  );
}

export default SessionOverview;
