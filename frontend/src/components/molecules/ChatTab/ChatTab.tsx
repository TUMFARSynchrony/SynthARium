import { ChatMessage } from "../../../types";
import { useAppSelector } from "../../../redux/hooks";
import { selectCurrentSession } from "../../../redux/slices/sessionsListSlice";
import { ActionIconButton } from "../../atoms/Button";
import PlayArrowOutlined from "@mui/icons-material/PlayArrowOutlined";
import { useEffect, useRef, useState } from "react";
import { INITIAL_CHAT_DATA } from "../../../utils/constants";
import { SpeechBubble } from "../../atoms/ChatMessage/SpeechBubble";
import { useBackListener } from "../../../hooks/useBackListener";
import useAutosizeTextArea from "../../../hooks/useAutosizeTextArea";
import { useSearchParams } from "react-router-dom";

type Props = {
  onChat: (newMessage: ChatMessage) => void;
  onGetSession: (sessionId: string) => void;
  currentUser: string;
  participantId?: string;
  onLeaveExperiment?: () => void;
};

export const ChatTab = (props: Props) => {
  const {
    onChat,
    onGetSession,
    currentUser,
    participantId,
    onLeaveExperiment
  } = props;
  const [message, setMessage] = useState("");
  const [searchParams, setSearchParams] = useSearchParams();
  const currentSession = useAppSelector(selectCurrentSession);
  const sessionId = currentSession?.id ?? searchParams.get("sessionId");
  const [messageTarget, setMessageTarget] = useState("participants");
  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  useAutosizeTextArea(textAreaRef.current, message);
  console.log(currentSession);
  useBackListener(() => onLeaveExperiment());

  useEffect(() => {
    if (sessionId) {
      onGetSession(sessionId);
    }
  }, [onGetSession, sessionId]);

  const handleChange = (message: string) => {
    setMessageTarget(message);
  };

  const onSendMessage = (messageTarget: string) => {
    const newMessage = { ...INITIAL_CHAT_DATA };
    newMessage["message"] = message;
    newMessage["time"] = Date.now();
    newMessage["author"] = participantId ? participantId : "experimenter";
    newMessage["target"] = participantId ? "experimenter" : messageTarget;

    onChat(newMessage);
    onGetSession(sessionId);
    if (message.length === 0) {
      return;
    }
    setMessage("");
  };
  console.log(
    currentUser === "experimenter" &&
      currentSession &&
      messageTarget !== "participants"
  );
  return (
    <div className="flex flex-col border-l-gray-100 border-l-2 h-[calc(100vh-4rem)] w-full items-center gap-y-5">
      <div className="text-3xl">Chat</div>
      <div className="w-full flex flex-col justify-between overflow-y-auto h-full">
        <div className="p-4 overflow-y-auto">
          {currentUser === "experimenter" &&
            currentSession &&
            messageTarget !== "participants" &&
            currentSession.participants
              .find((participant) => participant.id === messageTarget)
              .chat.map((message, index) => (
                <SpeechBubble
                  key={index}
                  currentUser={currentUser}
                  message={message.message}
                  author={message.author}
                  target={message.target}
                  date={message.time}
                />
              ))}
          {currentUser === "participant" &&
            currentSession &&
            messageTarget !== "experimenter" &&
            currentSession.participants
              .find((participant) => participant.id === participantId)
              .chat.map((message, index) => (
                <SpeechBubble
                  key={index}
                  currentUser={currentUser}
                  message={message.message}
                  author={message.author}
                  target={message.target}
                  date={message.time}
                />
              ))}
          {currentSession &&
            messageTarget === "participants" &&
            currentUser === "experimenter" &&
            currentSession.participants[0].chat
              .filter((message) => message.target === "participants")
              .map((message, index) => (
                <SpeechBubble
                  key={index}
                  currentUser={currentUser}
                  message={message.message}
                  author={message.author}
                  target={message.target}
                  date={message.time}
                  color={"bg-green-600"}
                />
              ))}
        </div>
        <div className="flex flex-col p-4">
          {currentUser === "experimenter" && (
            <div>
              <label htmlFor="participant-names">Send to </label>
              <select
                className="bg-gray-200 px-2 py-2 my-2 rounded"
                name="participant-names"
                id="participant-names"
                onChange={(event) => handleChange(event.target.value)}
              >
                <option value={"participants"}>All participants</option>
                {currentSession.participants.map((participant, index) => (
                  <option key={index} value={participant.id}>
                    {participant.participant_name}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div>
            <textarea
              className="resize-none border-2 border-stone-300 p-3 rounded outline-none w-full"
              placeholder="Enter your message here"
              value={message}
              ref={textAreaRef}
              rows={1}
              onChange={(event) => setMessage(event.target.value)}
            />
          </div>
          <ActionIconButton
            text="Send"
            variant="outlined"
            color="primary"
            size="medium"
            onClick={() => onSendMessage(messageTarget)}
            icon={<PlayArrowOutlined />}
          />
        </div>
      </div>
    </div>
  );
};
