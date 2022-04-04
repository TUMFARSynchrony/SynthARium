import { Link } from "react-router-dom";
import "./WatchingRoom.css";

function WatchingRoom() {
  return (
    <div>
      <h1>Watching Room</h1>
      <Link to="/">
        <span>Session Overview</span>
      </Link>
    </div>
  );
}

export default WatchingRoom;
