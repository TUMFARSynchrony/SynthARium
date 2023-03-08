import { useNavigate } from "react-router-dom";
import Button from '@mui/material/Button';

function LinkButton({ text, variant, path }) {
    let navigate = useNavigate();

    const handleButtonClick = (() => {
        navigate(path);
    });

    return (
        <>
            <Button variant={variant} onClick={handleButtonClick}>
                {text}
            </Button>
        </>
    );
}

export default LinkButton;
