import { Link } from "react-router-dom";
import "./WatchingRoom.css";

function WatchingRoom() {
  return (
    <div>
      <h1>Watching Room</h1>
      <Link to="/">
        <span>Main Page</span>
      </Link>
    </div>
  );
}

export default WatchingRoom;
