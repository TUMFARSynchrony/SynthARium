import Button from '@mui/material/Button';

function ActionButton({ text, variant, color, size, onClick }) {

    return (
        <>
            <Button variant={variant} color={color} size={size} onClick={onClick}>
                {text}
            </Button>
        </>
    );
}

export default ActionButton;
