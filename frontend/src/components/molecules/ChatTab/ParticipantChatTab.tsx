import { useAppDispatch, useAppSelector } from "../../../redux/hooks";
import { selectCurrentSession } from "../../../redux/slices/sessionsListSlice";
import { useEffect, useRef, useState } from "react";
import { INITIAL_CHAT_DATA } from "../../../utils/constants";
import { SpeechBubble } from "../../atoms/ChatMessage/SpeechBubble";
import { useBackListener } from "../../../hooks/useBackListener";
import useAutosizeTextArea from "../../../hooks/useAutosizeTextArea";
import { useSearchParams } from "react-router-dom";
import { Button } from "@nextui-org/react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { ChatMessage, Session } from "../../../types";

type Props = {
  onChat: (newMessage: ChatMessage) => void;
  onGetSession: (sessionId: string) => void;
  currentUser: string;
  participantId?: string;
  onLeaveExperiment?: () => void;
};

export const ParticipantChatTab = (props: Props) => {
  const { onChat, onGetSession, currentUser, participantId, onLeaveExperiment } = props;
  const [message, setMessage] = useState("");
  const [searchParams, setSearchParams] = useSearchParams();
  const currentSession = useAppSelector(selectCurrentSession);
  const sessionId = currentSession?.id ?? searchParams.get("sessionId");
  const [messageTarget, setMessageTarget] = useState("participants");
  const [shouldShowNotification, setShouldShowNotification] = useState(false);
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  useAutosizeTextArea(textAreaRef.current, message);
  useBackListener(() => onLeaveExperiment());

  useEffect(() => {
    if (sessionId) {
      onGetSession(sessionId);
    }
  }, [onGetSession, sessionId]);

  const onSendMessage = (messageTarget: string) => {
    if (message.length === 0) {
      return;
    }
    const newMessage = { ...INITIAL_CHAT_DATA };
    newMessage["message"] = message;
    newMessage["time"] = Date.now();
    newMessage["author"] = participantId;
    newMessage["target"] = "experimenter";

    onChat(newMessage);
    onGetSession(sessionId);

    setMessage("");
  };
  const onEnterPressed = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      onSendMessage(messageTarget);
    }
  };

  return (
    <div className="flex flex-col border-l-gray-200 border-l-2 h-full w-full items-center">
      <div className="flex flex-row justify-center items-center gap-x-2 border-b-2 border-b-gray-200 w-full py-2">
        <div className="text-3xl text-center">Chat</div>
      </div>

      <div className="w-full flex flex-col justify-between overflow-y-auto h-full">
        <div className="p-4 overflow-y-auto">
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
        </div>
        <div className="flex flex-col p-4 py-8">
          <div className="flex flex-row justify-between gap-x-2 items-center">
            <textarea
              className="resize-none border-2 border-stone-300 p-2 py-2 h-full w-full rounded outline-none text-sm"
              placeholder="Enter your message here"
              value={message}
              ref={textAreaRef}
              rows={1}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={(event: React.KeyboardEvent<HTMLTextAreaElement>) => {
                onEnterPressed(event);
              }}
            />
            <Button
              className="h-8 rounded-sm"
              color="primary"
              size="md"
              isIconOnly={true}
              onClick={() => onSendMessage(messageTarget)}
            >
              <FontAwesomeIcon icon={faPaperPlane} style={{ color: "#ffffff" }} />{" "}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
