import Button, { ButtonProps } from "@mui/material/Button";
import { useNavigate } from "react-router-dom";

interface LinkActionIconButtonProps extends ButtonProps {
  text: string;
  path: string;
  onClick: () => void;
  icon: JSX.Element;
}

function LinkActionIconButton({
  text,
  variant,
  path,
  size,
  onClick,
  icon
}: LinkActionIconButtonProps) {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate(path);
  };

  return (
    <Button
      variant={variant}
      size={size}
      onClick={() => {
        handleButtonClick();
        onClick();
      }}
      startIcon={icon}
    >
      {text}
    </Button>
  );
}

export default LinkActionIconButton;
