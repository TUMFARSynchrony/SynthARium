import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import { ActionButton } from '../components/atoms/Button';
import { useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';
import Toolbar from '@mui/material/Toolbar';
import AppToolbar from '../components/atoms/AppToolbar';


function Lobby() {
    const [openConsent, setOpenConsent] = useState(true);
    const [checkParticipation, setCheckParticipation] = useState(false);
    const [checkRecording, setCheckRecording] = useState(false);
    const consentTextParticipation = "I understand that I may terminate my participation in the study at any time.";
    const consentTextRecording = "I accept the recording of my user data and am also aware that excerpts from interviews \
                                    will be kept anonymous and maybe included in a publication.";

    return (
        <>
            <Dialog open={openConsent}>
                <DialogTitle sx={{ textAlign: "center", fontWeight: "bold" }}>Welcome to the study!</DialogTitle>
                <DialogContent>
                    <Typography variant="body1" align="justify" sx={{ marginBottom: 3 }}>
                        Study description... Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                        dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                        ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                        fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
                        deserunt mollit anim id est laborum.
                    </Typography>
                    <FormControlLabel control={<Checkbox />} label={consentTextParticipation} checked={checkParticipation}
                        sx={{ alignItems: "flex-start" }} onChange={() => { setCheckParticipation(!checkParticipation) }} />
                    <FormControlLabel control={<Checkbox />} label={consentTextRecording} checked={checkRecording}
                        sx={{ alignItems: "flex-start" }} onChange={() => { setCheckRecording(!checkRecording) }} />
                </DialogContent>
                <DialogActions sx={{ alignSelf: "center" }}>
                    <ActionButton text="I AGREE" variant="contained" color="success" size="medium" onClick={() => { setOpenConsent(!openConsent) }}
                        disabled={!checkParticipation || !checkRecording} />
                </DialogActions>
            </Dialog>

            <AppToolbar />
        </>
    )
}

export default Lobby;