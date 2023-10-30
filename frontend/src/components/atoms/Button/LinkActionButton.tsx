import Button, { ButtonProps } from "@mui/material/Button";
import { useNavigate } from "react-router-dom";

interface LinkActionButtonProps extends ButtonProps {
  text: string;
  path: string;
  onClick: () => void;
}

function LinkActionButton({ text, variant, path, size, color, onClick }: LinkActionButtonProps) {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate(path);
  };

  return (
    <Button
      variant={variant}
      size={size}
      color={color}
      onClick={() => {
        handleButtonClick();
        onClick();
      }}
    >
      {text}
    </Button>
  );
}

export default LinkActionButton;
