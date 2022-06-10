import Button from "../../atoms/Button/Button";
import Heading from "../../atoms/Heading/Heading";
import Label from "../../atoms/Label/Label";
import TextField from "../TextField/TextField";
import "./OverviewTab.css";

function OverviewTab() {
  return (
    <div className="overviewTabContainer">
      <Heading heading={"Session 1"} />
      <hr className="separatorLine"></hr>
      <div className="sessionInformation">
        <h3>Session Information</h3>
        <div className="sessionDuration">
          <div>
            <Label title={"Time Limit: "} /> 60mins
          </div>
          <div>
            <Label title={"Starting time: "} /> Not started yet
          </div>
          <div>
            <Label title={"Ending time: "} /> Not ended yet
          </div>
        </div>
        <hr className="separatorLine"></hr>
      </div>
      <div className="sessionInformation">
        <h3>Send Message to all participants</h3>
        <TextField placeholder={"Enter your message here"} />
        <Button name={"Send"} design={"secondary"} />
      </div>
    </div>
  );
}

export default OverviewTab;
