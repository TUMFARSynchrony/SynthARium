import Button from '@mui/material/Button';

function ActionIconButton({ text, variant, color, onClick, icon }) {

    return (
        <>
            <Button variant={variant} color={color} onClick={() => { onClick(); }} startIcon={icon}>
                {text}
            </Button>
        </>
    );
}

export default ActionIconButton;
