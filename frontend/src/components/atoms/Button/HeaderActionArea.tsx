import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { IconDefinition } from "@fortawesome/free-solid-svg-icons";

/*
const buttonConfigs = {
  // not only icons but general buttons with different looks etc.
  undoRedoButtonList: [faUndo, faRedo],
  experimenterButtonList: [faCommentAlt, faClipboardCheck, faUsers],
  participantButtonList: [faCommentAlt, faClipboardCheck]
};
*/

type HeaderActionAreaProps = {
  buttons: Array<ButtonConfig>;
};

type ButtonConfig = {
  label?: string;
  onClick?: () => void;
  icon?: IconDefinition;
};

const HeaderActionArea = (props: HeaderActionAreaProps) => {
  const { buttons } = props;
  return (
    <div className="button-list flex gap-2">
      {buttons.map((button, index) => (
        <button
          key={index}
          className="px-4 py-2 bg-neutral-200 rounded-2xl border border-neutral-200 flex justify-center items-center text-sm"
          onClick={button.onClick}
        >
          <FontAwesomeIcon icon={button.icon} className="w-4 h-4 pr-2" />
          {button.label}
        </button>
      ))}
    </div>
  );
};

export default HeaderActionArea;
