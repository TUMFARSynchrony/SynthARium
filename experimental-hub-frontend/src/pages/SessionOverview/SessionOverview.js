import SessionCard from "../../components/organisms/SessionCard/SessionCard";
import { getSessionJson } from "../../mockServer/sessionJson";
import "./SessionOverview.css";
import NavigationBar from "../../components/organisms/NavigationBar/NavigationBar";

function SessionOverview() {
  var sessionCards = getSessionJson();
  console.log(sessionCards);
  return (
    <div>
      <NavigationBar />
      <h2 className="sessionOverviewHeadline">Planned Sessions</h2>
      <div className="sessionOverviewContainer">
        <div className="sessionOverviewCards">
          {sessionCards.map((session) => {
            return (
              <SessionCard
                title={session.title}
                date={session.date}
                time={session.time}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default SessionOverview;
