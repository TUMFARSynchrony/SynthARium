function PageTemplate({
  title,
  customComponent,
  buttonListComponent,
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
        {customComponent}
      </div>
    </div>
  );
}

export default PageTemplate;
