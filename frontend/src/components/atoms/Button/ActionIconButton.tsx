import Button, { ButtonProps } from "@mui/material/Button";

interface ActionIconButtonProps extends ButtonProps {
  text: string;
  icon: JSX.Element;
}

function ActionIconButton({ text, variant, color, size, onClick, icon }: ActionIconButtonProps) {
  return (
    <Button variant={variant} color={color} size={size} onClick={onClick} startIcon={icon}>
      {text}
    </Button>
  );
}

export default ActionIconButton;
