import { useEffect, useState } from "react";
import { Layer, Stage } from "react-konva";
import Video from "../../components/atoms/Video/Video";
import AppToolbar from "../../components/atoms/AppToolbar";
import { CANVAS_SIZE } from "../../utils/constants";
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import ConsentModal from "../../modals/ConsentModal";

function ExperimentRoom({ localStream, connection }) {
  const [participantStream, setParticipantStream] = useState(localStream);
  const [participantVideoData, setParticipantVideoData] = useState({
    size: {
      width: CANVAS_SIZE.width,
      height: CANVAS_SIZE.height
    },
    position: {
      x: 0,
      y: 0
    }
  });

  useEffect(() => {
    setParticipantStream(localStream);
  }, [localStream]);


  return (
    <>
      <AppToolbar />
      <ConsentModal />
      <Grid container sx={{ p: 2 }}>
        <Grid item sm={9}>
          <Paper elevation={2} sx={{ backgroundColor: "whitesmoke", width: CANVAS_SIZE.width, height: CANVAS_SIZE.height }}>
            {
              <Stage width={CANVAS_SIZE.width} height={CANVAS_SIZE.height}>
                <Layer>
                  <Video
                    src={participantStream}
                    participantData={participantVideoData}
                  />
                </Layer>
              </Stage>
            }
          </Paper>
        </Grid>
        <Grid item sm={3}>
          <Box>
            <Typography variant="button" sx={{ color: "primary.main" }}>Instructions</Typography>
            <List sx={{ listStyleType: 'disc', px: 2, lineHeight: 1.3 }}>
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
            <Divider />
          </Box>
        </Grid>
      </Grid >
    </>
  );
}

export default ExperimentRoom;
