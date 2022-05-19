import { useState } from "react";
import Heading from "../../components/atoms/Heading/Heading";
import "./WatchingRoom.css";

function WatchingRoom() {
  const [state, setState] = useState("WAITING");
  return (
    <div className="watchingRoomContainer">
      <div className="watchingRoomHeader">
        <Heading heading={"State: " + state} />
      </div>
    </div>
  );
}

export default WatchingRoom;
