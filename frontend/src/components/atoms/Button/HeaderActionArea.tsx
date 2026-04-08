import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { IconDefinition } from "@fortawesome/free-solid-svg-icons";
import openAiLogo from "../../molecules/ChatGptTab/ChatGPT_logo.png";
import { Tooltip } from "@nextui-org/react";

type HeaderActionAreaProps = {
  buttons: Array<ButtonConfig>;
};

type ButtonConfig = {
  onClick?: () => void;
  icon?: IconDefinition;
  externalIcon?: boolean;
  label?: string;
  tooltip?: string;
};

const HeaderActionArea = (props: HeaderActionAreaProps) => {
  const { buttons } = props;
  return (
    <div className="button-list flex gap-2">
      {buttons.map((button, index) => {
        const ButtonContent = (
          <button
            className="px-4 py-2 bg-neutral-200 rounded-2xl border border-neutral-200 flex justify-center items-center text-sm"
            onClick={button.onClick}
          >
            {button.externalIcon ? (
              <img className="w-4 h-4" src={openAiLogo} alt="OpenAI Logo" />
            ) : (
              <FontAwesomeIcon icon={button.icon} className="w-4 h-4" />
            )}
            {button.label}
          </button>
        );

        return button.tooltip ? (
          <Tooltip key={index} content={button.tooltip} placement="bottom">
            {ButtonContent}
          </Tooltip>
        ) : (
          <React.Fragment key={index}>{ButtonContent}</React.Fragment>
        );
      })}
    </div>
  );
};

export default HeaderActionArea;
