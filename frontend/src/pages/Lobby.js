import AppToolbar from '../components/atoms/AppToolbar';
import TabPanel from '../components/atoms/TabPanel';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import { CANVAS_SIZE } from '../utils/constants';
import { Typography } from '@mui/material';
import { useState } from 'react';
import ParticipantVideo from '../components/molecules/ParticipantVideo';


function Lobby({ localStream, connection }) {
    const [tabValue, setTabValue] = useState(0);

    const handleTabChange = (event, newValue) => {
        setTabValue(newValue);
    };

    return (
        <>
            <AppToolbar />
            <Grid container sx={{ p: 2 }}>
                <Grid item sm={9}>
                    <Typography sx={{ mb: 2 }}>
                        <em>STUDY TITLE</em>
                    </Typography>
                    <Paper elevation={2} sx={{ backgroundColor: "whitesmoke", width: CANVAS_SIZE.width, height: CANVAS_SIZE.height }}>
                        {
                            localStream && connection.participantSummary && (
                                <ParticipantVideo localStream={localStream}/>
                            )
                        }
                    </Paper>
                </Grid>
                <Grid item sm={3}>
                    <Box sx={{ pt: 5 }}>
                        <Tabs value={tabValue} onChange={handleTabChange}>
                            <Tab label="Instructions" />
                            <Tab label="Overview" />
                        </Tabs>
                        <TabPanel value={tabValue} index={0}>
                            <List sx={{ listStyleType: 'disc' }}>
                                <ListItem sx={{ display: 'list-item' }}>
                                    Please remove any glasses, caps or other such articles if you are wearing any.
                                </ListItem>
                                <ListItem sx={{ display: 'list-item' }}>
                                    Ensure that your surrounding lighting is good.
                                </ListItem>
                                <ListItem sx={{ display: 'list-item' }}>
                                    We would like to know about your experience, so please take 5  minutes at the end to do the
                                    Feedback Survey.
                                </ListItem>
                            </List>
                        </TabPanel>
                        <TabPanel value={tabValue} index={1}>
                            <Typography align="left">
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                                fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
                                deserunt mollit anim id est laborum.
                            </Typography>
                        </TabPanel>
                    </Box>
                </Grid>
            </Grid >
        </>
    )
}

export default Lobby;