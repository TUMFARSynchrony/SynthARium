import PlayArrowOutlined from "@mui/icons-material/PlayArrowOutlined";
import { useState } from "react";
import { useBackListener } from "../../../hooks/useBackListener";
import EndVerificationModal from "../../../modals/EndVerificationModal/EndVerificationModal";
import StartVerificationModal from "../../../modals/StartVerificationModal/StartVerificationModal";
import { useAppSelector } from "../../../redux/hooks";
import { selectOngoingExperiment } from "../../../redux/slices/ongoingExperimentSlice";
import { selectSessions } from "../../../redux/slices/sessionsListSlice";
import { INITIAL_CHAT_DATA, instructionsList } from "../../../utils/constants";
import { getSessionById, integerToDateTime } from "../../../utils/utils";
import { ActionButton, ActionIconButton } from "../../atoms/Button";
import Heading from "../../atoms/Heading/Heading";
import Label from "../../atoms/Label/Label";
import TextAreaField from "../TextAreaField/TextAreaField";
import "./OverviewTab.css";
import { FormControl, InputLabel, MenuItem, Select } from "@mui/material";

function OverviewTab({
  onLeaveExperiment,
  onStartExperiment,
  onEndExperiment,
  onChat,
  onGetSession
}) {
  const [message, setMessage] = useState("");
  const [startVerificationModal, setStartVerificationModal] = useState(false);
  const [endVerificationModal, setEndVerificationModal] = useState(false);
  const [messageOption, setMessageOption] = useState("participants");
  const sessionId = useAppSelector(selectOngoingExperiment).sessionId;
  const sessionsList = useAppSelector(selectSessions);
  const sessionData = getSessionById(sessionId, sessionsList);
  console.log(messageOption);

  useBackListener(() => onLeaveExperiment());

  const onSendMessage = (messageTarget) => {
    let newMessage = { ...INITIAL_CHAT_DATA };
    newMessage["message"] = message;
    newMessage["time"] = Date.now();
    newMessage["author"] = "experimenter";
    newMessage["target"] = messageTarget;

    onChat(newMessage);
    onGetSession(sessionId);
    if (message.length === 0) {
      return;
    }
    setMessage("");
  };

  const handleChange = (value) => {
    setMessageOption(value);
  };

  return (
    <div className="overviewTabContainer">
      <Heading heading={sessionData.title} />
      <hr className="separatorLine"></hr>
      <div className="sessionInformation">
        <div className="sessionDuration">
          <div>
            <Label title={"Instructions"} />
            <ul>
              {
                // getting a common set of instructions for the participant from constants.js
                instructionsList.map((instruction, index) => {
                  return <li key={index}>{instruction}</li>;
                })
              }
            </ul>
          </div>
          <div>
            <Label title={"Starting time: "} />
            {sessionData.start_time > 0
              ? integerToDateTime(sessionData.start_time)
              : "Not started yet"}
          </div>
          <div>
            <Label title={"Ending time: "} />{" "}
            {sessionData.end_time > 0
              ? integerToDateTime(sessionData.start_time)
              : "Not ended yet"}
          </div>
        </div>
        <hr className="separatorLine"></hr>
      </div>
      <div className="sessionInformation">
        {messageOption && (
          <FormControl fullWidth>
            <InputLabel id="demo-simple-select-label">
              Message target
            </InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={messageOption}
              label="Message target"
              onChange={(e) => handleChange(e.target.value)}
            >
              <MenuItem value={"participants"}>All participants</MenuItem>
              {sessionData.participants.map((participant, index) => (
                <MenuItem key={index} value={participant.id}>
                  {participant.participant_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        )}
        <TextAreaField
          placeholder={"Enter your message here"}
          value={message}
          onChange={(newMessage) => setMessage(newMessage)}
        />
        <ActionIconButton
          text="Send"
          variant="outlined"
          color="primary"
          size="medium"
          onClick={() => onSendMessage(messageOption)}
          icon={<PlayArrowOutlined />}
        />
      </div>
      <hr className="separatorLine"></hr>

      <ActionButton
        text="LEAVE EXPERIMENT"
        variant="outlined"
        path="/"
        size="large"
        color="primary"
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
