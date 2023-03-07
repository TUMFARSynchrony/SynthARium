import Typography from "@mui/material/Typography";
import { styled } from '@mui/material/styles';

function HeroText({ text }) {

    const Text = styled(Typography)(({ theme }) => ({
        fontWeight: 'bold',
        marginTop: theme.spacing(4),
        marginBottom: theme.spacing(1),
        marginRight: theme.spacing(4),
        marginLeft: theme.spacing(4),
    }));

    return (
        <>
            <Text variant="h5">
                {text}
            </Text>
        </>
    );
}


export default HeroText;
