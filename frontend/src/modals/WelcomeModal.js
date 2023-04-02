import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Typography from '@mui/material/Typography';
import { ActionButton } from '../components/atoms/Button';
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import RadioGroup from "@mui/material/RadioGroup";
import Radio from "@mui/material/Radio";
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import { useState } from 'react';

function WelcomeModal({ userType, setUserType, openUserTypeDialog, setOpenUserTypeDialog, 
                        sessionId, setSessionId, participantId, setParticipantId, createConnection }) {
    const [checkParticipation, setCheckParticipation] = useState(false);
    const [checkRecording, setCheckRecording] = useState(false);
    const consentTextParticipation = "I understand that I may terminate my participation in the study at any time.";
    const consentTextRecording = "I accept the recording of my audio and video and am also aware that the data \
                                    will be kept anonymous and maybe used for research purposes.";

    return (
        <Dialog open={openUserTypeDialog} PaperProps={{ sx: { width: "50%" } }}>
            <DialogTitle sx={{ textAlign: "center", fontWeight: "bold" }}>Welcome to the Synchrony Hub!</DialogTitle>
            <DialogContent>
                <FormControl>
                    <FormLabel id="user-type-label">You are joining as :</FormLabel>
                    <RadioGroup
                        row
                        aria-labelledby="user-type-label"
                        name="user-type"
                        onChange={(event) => setUserType(event.target.value)}
                    >
                        <FormControlLabel value="experimenter" control={<Radio />} label="Experimenter" />
                        <FormControlLabel value="participant" control={<Radio />} label="Participant" />
                    </RadioGroup>
                </FormControl>
                {
                    userType == "participant" && (
                        <>
                            <Typography variant="body1" align="justify" sx={{ marginBottom: 3 }}>
                                Study description... Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                                fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
                                deserunt mollit anim id est laborum.
                            </Typography>
                            <Box sx={{ display: "flex", justifyContent: "space-between", columnGap: 5, mb: 3 }}>
                                <TextField label="Session ID" size="small" fullWidth required onChange={(event) => { setSessionId(event.target.value) }} />
                                <TextField label="Participant ID" size="small" fullWidth required onChange={(event) => { setParticipantId(event.target.value) }} />
                            </Box>
                            <FormControlLabel control={<Checkbox />} label={consentTextParticipation} checked={checkParticipation}
                                sx={{ alignItems: "flex-start" }} onChange={() => { setCheckParticipation(!checkParticipation) }} />
                            <FormControlLabel control={<Checkbox />} label={consentTextRecording} checked={checkRecording}
                                sx={{ alignItems: "flex-start" }} onChange={() => { setCheckRecording(!checkRecording) }} />
                        </>
                    )
                }
            </DialogContent>
            <DialogActions sx={{ alignSelf: "center" }}>
                {
                    userType == "participant" ? (
                        <ActionButton text="I AGREE" variant="contained" color="success" size="medium" onClick={() => {
                            setOpenUserTypeDialog(!openUserTypeDialog);
                            createConnection()
                        }}
                            disabled={!checkParticipation || !checkRecording || !sessionId || !participantId} />
                    ) :
                        (
                            <ActionButton text="JOIN" variant="contained" color="success" size="medium" onClick={() => {
                                setOpenUserTypeDialog(!openUserTypeDialog);
                                createConnection()
                            }} />
                        )
                }
            </DialogActions>
        </Dialog>
    )
}

export default WelcomeModal;
