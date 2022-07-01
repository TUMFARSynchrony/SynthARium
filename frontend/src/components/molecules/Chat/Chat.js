import { useState } from "react";
import Button from "../../atoms/Button/Button";
import TextAreaField from "../TextAreaField/TextAreaField";
import { FaAngleRight } from "react-icons/fa";

import "./Chat.css";
import Message from "../../atoms/Message/Message";

function Chat({ participantId, chat, onSendChat }) {
  const [messageContent, setMessageContent] = useState("");

  const onMessageChange = (newMessage) => {
    setMessageContent(newMessage);
  };

  const onSendMessage = () => {
    const newMessage = {
      author: "experimenter",
      message: messageContent,
      target: participantId,
      time: new Date().getTime(),
    };

    onSendChat(newMessage);
  };

  return (
    <div className="chatContainer">
      {chat.length > 0 ? (
        chat.map((message, index) => {
          return <Message />;
        })
      ) : (
        <p>No messages with this user yet.</p>
      )}
      <div className="chatInput">
        <TextAreaField
          value={messageContent}
          placeholder={"Enter your message here"}
          onChange={onMessageChange}
        />
        <Button icon={<FaAngleRight />} onClick={() => onSendMessage()} />
      </div>
    </div>
  );
}

export default Chat;
