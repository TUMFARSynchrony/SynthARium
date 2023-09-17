import Button, { ButtonProps } from "@mui/material/Button";
import { useNavigate } from "react-router-dom";

interface ActionButtonProps extends ButtonProps {
  text: string;
  path?: string;
  onClick: () => void;
}

function ActionButton({
  text,
  variant,
  color,
  size,
  path,
  onClick,
  disabled = false
}: ActionButtonProps) {
  const navigate = useNavigate();
  const handleNavigation = () => {
    if (path) navigate(path);
  };
  return (
    <Button
      variant={variant}
      color={color}
      size={size}
      onClick={() => {
        handleNavigation();
        onClick();
      }}
      disabled={disabled}
    >
      {text}
    </Button>
  );
}

export default ActionButton;
