import AppToolbar from '../components/atoms/AppToolbar';
import Paper from '@mui/material/Paper';
import { CANVAS_SIZE } from '../utils/constants';


function Lobby() {

    return (
        <>
            <AppToolbar />

            <Paper elevation={2} sx={{ backgroundColor: "whitesmoke", width: CANVAS_SIZE.width, height: CANVAS_SIZE.height }}>

            </Paper>
        </>
    )
}

export default Lobby;