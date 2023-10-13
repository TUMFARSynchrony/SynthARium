import Button, { ButtonProps } from "@mui/material/Button";
import { useNavigate } from "react-router-dom";

interface LinkButtonProps extends ButtonProps {
  text: string;
  path: string;
}

function LinkButton({ text, variant, size, path }: LinkButtonProps) {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate(path);
  };

  return (
    <Button variant={variant} size={size} onClick={handleButtonClick}>
      {text}
    </Button>
  );
}

export default LinkButton;
