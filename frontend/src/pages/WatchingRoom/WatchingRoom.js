import { useState } from "react";
import Heading from "../../components/atoms/Heading/Heading";
import WatchingRoomTabs from "../../components/organisms/WatchingRoomTabs/WatchingRoomTabs";
import "./WatchingRoom.css";

function WatchingRoom() {
  const [state, setState] = useState("WAITING");
  return (
    <div className="watchingRoomContainer">
      <div className="watchingRoomHeader">
        <Heading heading={"State: " + state} />
      </div>
      <div className="sessionSpectating">
        <WatchingRoomTabs />
      </div>
    </div>
  );
}

export default WatchingRoom;
