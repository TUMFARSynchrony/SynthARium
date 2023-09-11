import ActionButton from "../atoms/Button/ActionButton";
function PageTemplate({
  content,
  customComponent,
  actionButtonProps,
  contentTitle
}) {
  return (
    <div className="h-screen flex flex-col mx-[100px] py-4 text-left gap-y-4 xl:items-center">
      <div className="flex flex-col h-full overflow-y-auto justify-center gap-y-4 xl:w-1/2">
        <div className="font-bold text-lg">{contentTitle}</div>
        <p className="text-justify">{content}</p>
        <div className="flex flex-col h-full overflow-y-auto justify-center gap-y-4 xl:w-1/2">
          <div className="flex flex-col">{customComponent}</div>
        </div>
      </div>
      <div className="self-center h-fit">
        <ActionButton {...actionButtonProps} />
      </div>
    </div>
  );
}

export default PageTemplate;
