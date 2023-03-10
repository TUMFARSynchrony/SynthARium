import { useState } from "react";
import { useSelector } from "react-redux";
import EndVerificationModal from "../../../modals/EndVerificationModal/EndVerificationModal";
import StartVerificationModal from "../../../modals/StartVerificationModal/StartVerificationModal";
import {
  getSessionById,
  integerToDateTime,
  useBackListener,
} from "../../../utils/utils";
import { ActionButton, ActionIconButton, LinkActionButton } from "../../atoms/Button";
import Heading from "../../atoms/Heading/Heading";
import Label from "../../atoms/Label/Label";
import TextAreaField from "../TextAreaField/TextAreaField";
import PlayArrowOutlined from "@mui/icons-material/PlayArrowOutlined";
import "./OverviewTab.css";

function OverviewTab({
  onLeaveExperiment,
  onStartExperiment,
  onEndExperiment,
}) {
  const [message, setMessage] = useState("");
  const [startVerificationModal, setStartVerificationModal] = useState(false);
  const [endVerificationModal, setEndVerificationModal] = useState(false);

  const ongoingExperiment = useSelector(
    (state) => state.ongoingExperiment.value
  );
  const sessionId = ongoingExperiment.sessionId;
  const sessionsList = useSelector((state) => state.sessionsList.value);
  const sessionData = getSessionById(sessionId, sessionsList)[0];

  useBackListener(() => onLeaveExperiment());

  return (
    <div className="overviewTabContainer">
      <Heading heading={sessionData.title} />
      <hr className="separatorLine"></hr>
      <div className="sessionInformation">
        <h3>Session Information</h3>
        <div className="sessionDuration">
          <div>
            <Label title={"Time Limit: "} /> {sessionData.time_limit / 60000}
          </div>
          <div>
            <Label title={"Starting time: "} />
            {sessionData.start_time > 0
              ? integerToDateTime(sessionData.start_time).toLocaleString()
              : "Not started yet"}
          </div>
          <div>
            <Label title={"Ending time: "} />{" "}
            {sessionData.end_time > 0
              ? integerToDateTime(sessionData.start_time).toLocaleString()
              : "Not ended yet"}
          </div>
        </div>
        <hr className="separatorLine"></hr>
      </div>
      <div className="sessionInformation">
        <h3>Send Message to all participants</h3>
        <TextAreaField
          placeholder={"Enter your message here"}
          value={message}
          onChange={(newMessage) => setMessage(newMessage)}
        />
        <ActionIconButton text="Send" variant="outlined" color="primary" size="medium" onClick={() => {}} icon={<PlayArrowOutlined />} />
      </div>
      <hr className="separatorLine"></hr>

      <LinkActionButton
        text="LEAVE EXPERIMENT"
        variant="outlined"
        path="/"
        onClick={() => onLeaveExperiment()}
      />
      {sessionData.start_time === 0 ? (
        <ActionButton
          text="START EXPERIMENT"
          variant="contained"
          color="success"
          size="large"
          onClick={() => {
            setStartVerificationModal(true);
          }}
        />
      ) : (
        <ActionButton
          text="END EXPERIMENT"
          variant="contained"
          color="error"
          size="large"
          onClick={() => {
            setEndVerificationModal(true);
          }}
        />
      )}

      {startVerificationModal && (
        <StartVerificationModal
          setShowModal={setStartVerificationModal}
          onStartExperiment={onStartExperiment}
        />
      )}

      {endVerificationModal && (
        <EndVerificationModal
          setShowModal={setEndVerificationModal}
          onEndExperiment={onEndExperiment}
        />
      )}
    </div>
  );
}

export default OverviewTab;
