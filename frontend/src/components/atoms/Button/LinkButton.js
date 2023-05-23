import { useNavigate } from "react-router-dom";
import Button from '@mui/material/Button';

function LinkButton({ text, variant, size, path }) {
    let navigate = useNavigate();

    const handleButtonClick = (() => {
        navigate(path);
    });

    return (
        <>
            <Button variant={variant} size={size} onClick={handleButtonClick}>
                {text}
            </Button>
        </>
    );
}

export default LinkButton;
