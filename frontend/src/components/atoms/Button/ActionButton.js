import Button from "@mui/material/Button";

function ActionButton({
  text,
  variant,
  color,
  size,
  onClick,
  disabled = false
}) {
  return (
    <>
      <Button
        variant={variant}
        color={color}
        size={size}
        onClick={onClick}
        disabled={disabled}
      >
        {text}
      </Button>
    </>
  );
}

export default ActionButton;
