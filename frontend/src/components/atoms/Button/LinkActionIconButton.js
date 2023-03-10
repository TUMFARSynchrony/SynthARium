import { useNavigate } from "react-router-dom";
import Button from '@mui/material/Button';

function LinkActionIconButton({ text, variant, path, size, onClick, icon }) {
    let navigate = useNavigate();

    const handleButtonClick = (() => {
        navigate(path);
    });

    return (
        <>
            <Button variant={variant} size={size} onClick={() => { handleButtonClick(); onClick(); }} startIcon={icon}>
                {text}
            </Button>
        </>
    );
}

export default LinkActionIconButton;
