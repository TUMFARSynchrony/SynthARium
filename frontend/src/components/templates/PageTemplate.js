function PageTemplate({
  title,
  customComponent,
  buttonListComponent,
  minusMarginRight,
  centerContentOnYAxis
}) {
  const buttonClasses = `py-4 font-bold text-3xl ${
    minusMarginRight ? "-mr-16" : ""
  }`;

  return (
    <div className="h-full w-full flex flex-col">
      <div className="h-20 flex flex-row justify-between items-center w-full px-8">
        <div className="font-bold text-3xl">{title}</div>
        {buttonListComponent && (
          <div className={buttonClasses}>{buttonListComponent}</div>
        )}{" "}
      </div>
      <hr className="w-full border-2 border-gray-200" />
      {/*
      minus 84 because of the height(h-20 = 80px + border-2 = 4px)
      */}
      <div
        className={`flex flex-col overflow-y-auto h-[calc(100vh-84px)] w-full ${
          centerContentOnYAxis && "justify-center"
        } `}
      >
        {customComponent}
      </div>
    </div>
  );
}

export default PageTemplate;
