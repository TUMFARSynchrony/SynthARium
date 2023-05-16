import { styled } from '@mui/material/styles';
import Toolbar from '@mui/material/Toolbar';

export default function AppToolbar() {

    // This is the toolbar view for partcipants only and used in the lobby, 
    // with the title - SYNCHRONY HUB. Can add a logo in the future
    const AppToolbar = styled(Toolbar)(() => ({
        backgroundColor: "#899499",
        color: "white",
        fontWeight: "bold",
        height: "8vh"
    }));

    return (
        <AppToolbar>
            SYNCHRONY HUB
        </AppToolbar>
    )
}
