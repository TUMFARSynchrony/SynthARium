import ActionButton from "../atoms/Button/ActionButton";
function ParticipantContentTemplate({
  content,
  customComponent,
  actionButtonProps,
  contentTitle,
  sideComponent
}) {
  const chatClasses = ` ${sideComponent ? "-mr-[60px]" : ""}`;
  return (
    <div className="h-[calc(100vh-72px)] flex flex-col text-left xl:items-center bg-pink-400">
      <div className="flex flex-row h-full w-full justify-center bg-purple-400">
        <div className="flex flex-col justify-between items-center w-full bg-orange-400">
          <div className="font-bold text-lg">{contentTitle}</div>
          <p className="text-justify">{content}</p>
          <div className="flex flex-row h-full w-full justify-center bg-yellow-400">
            {customComponent}
          </div>
        </div>
        <div className={`flex flex-col ${chatClasses} bg-black`}>
          {sideComponent}
        </div>
      </div>
      <div className="self-center h-fit">
        <ActionButton {...actionButtonProps} />
      </div>
    </div>
  );
}

export default ParticipantContentTemplate;
