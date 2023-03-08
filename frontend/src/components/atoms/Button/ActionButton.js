import Button from '@mui/material/Button';

function ActionButton({ text, variant, color, onClick }) {

    return (
        <>
            <Button variant={variant} color={color} onClick={onClick}>
                {text}
            </Button>
        </>
    );
}

export default ActionButton;
