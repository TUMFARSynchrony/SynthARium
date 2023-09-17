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
    <div className="h-screen flex flex-col py-4 text-left gap-y-4  xl:items-center ">
      <div className="flex flex-row justify-between items-center w-full">
        <div className="py-4 font-bold text-3xl ">{title}</div>
        <div className={buttonClasses}>{buttonListComponent}</div>
      </div>
      <hr className=" border-2 w-full border-gray-200" />
      <div className="flex flex-col w-full h-[calc(100vh-72px)] gap-y-4 justify-center ">
        {customComponent}
      </div>
    </div>
  );
}

export default PageTemplate;
