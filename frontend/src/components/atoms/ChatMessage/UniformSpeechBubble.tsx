import moment from "moment";

type Props = {
  author: string;
  target: string;
  message: string;
  date: number;
  currentUser: string;
  participant_name: string;
};
export const UniformSpeechBubble = (props: Props) => {
  const { author, target, message, date, currentUser, participant_name } =
    props;

  const setMessageTexts = (author: string) => {
    if (author === "experimenter" && target === "participants") {
      return `Me to Participants (Announcement)`;
    } else if (author === "experimenter" && target !== "participants") {
      return `Me to ${participant_name} (Privately)`;
    } else {
      return `${participant_name} to Me (Privately)`;
    }
  };
  return (
    <div className="flex flex-col">
      <div className="flex flex-row justify-between">
        <div className="self-start text-[0.75rem] pt-1.5">
          {setMessageTexts(author)}
        </div>
        <div className="self-end text-[0.65rem] max-w-full">
          {moment(date).format("lll")}
        </div>
      </div>
      <div className="self-start bg-blue-600 text-white px-2 py-1 rounded break-words max-w-full text-start">
        {message}
      </div>
    </div>
  );
};
