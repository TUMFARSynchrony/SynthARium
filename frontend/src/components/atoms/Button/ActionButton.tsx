import Button, { ButtonProps } from "@mui/material/Button";

interface ActionButtonProps extends ButtonProps {
  text: string;
  onClick: () => void;
}

function ActionButton({
  text,
  variant,
  color,
  size,
  onClick,
  disabled = false
}: ActionButtonProps) {
  return (
    <Button
      variant={variant}
      color={color}
      size={size}
      onClick={onClick}
      disabled={disabled}
    >
      {text}
    </Button>
  );
}

export default ActionButton;
