import Button from "@mui/material/Button";

function ActionIconButton({ text, variant, color, size, onClick, icon }) {
  return (
    <>
      <Button
        variant={variant}
        color={color}
        size={size}
        onClick={() => {
          onClick();
        }}
        startIcon={icon}
      >
        {text}
      </Button>
    </>
  );
}

export default ActionIconButton;
