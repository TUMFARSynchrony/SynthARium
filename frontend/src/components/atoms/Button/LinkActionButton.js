import { useNavigate } from "react-router-dom";
import Button from '@mui/material/Button';

function LinkActionButton({ text, variant, path, size, color, onClick }) {
    let navigate = useNavigate();

    const handleButtonClick = (() => {
        navigate(path);
    });

    return (
        <>
            <Button variant={variant} size={size} color={color} onClick={() => { handleButtonClick(); onClick(); }}>
                {text}
            </Button>
        </>
    );
}

export default LinkActionButton;
