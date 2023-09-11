import ActionButton from "../atoms/Button/ActionButton";
import ParticipantContentTemplate from "./ParticipantContentTemplate";
function PageTemplate({
  title,
  content,
  customComponent,
  buttonListComponent,
  actionButtonProps,
  contentTitle,
  minusMarginRight
}) {
  const buttonClasses = `py-4 font-bold text-3xl ${
    minusMarginRight ? "-mr-16" : ""
  }`;

  return (
    <div className="h-screen flex flex-col mx-[100px] py-4 text-left gap-y-4 xl:items-center">
      <div className="flex flex-row justify-between items-center w-full">
        <div className="py-4 font-bold text-3xl">{title}</div>
        <div className={buttonClasses}>{buttonListComponent}</div>
      </div>
      <hr className="w-screen -mx-8 border-2 border-gray-200" />
      <div className="flex flex-col h-full overflow-y-auto justify-center gap-y-4 xl:w-1/2">
        <ParticipantContentTemplate
          customComponent={customComponent}
          content={content}
          contentTitle={contentTitle}
          actionButtonProps={actionButtonProps}
        />
      </div>
    </div>
  );
}

export default PageTemplate;
