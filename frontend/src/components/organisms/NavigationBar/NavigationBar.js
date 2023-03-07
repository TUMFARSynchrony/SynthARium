import { useState } from "react";
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import { useNavigate } from "react-router-dom";
import Stack from "@mui/material/Stack";
import { styled } from '@mui/material/styles';

const GreyToolbar = styled(Toolbar)(({ theme }) => ({
  backgroundColor: "#899499",
}));

function NavigationBar() {
  let navigate = useNavigate();
  const [sessionOverview, setSessionOverview] = useState(true);
  const [postProcessing, setPostProcessing] = useState(true);

  const handleSessionOverviewClick = (() => {
    setSessionOverview(true);
    navigate("/");
  });

  const handlePostProcessingClick = (() => {
    setPostProcessing(true);
    navigate("/postProcessingRoom")
  })

  return (
    <>
      <AppBar position="static">
        <GreyToolbar>
          <Stack direction="row" spacing={2}>
            <Button variant="string" onClick={handleSessionOverviewClick}>
              Session Overview
            </Button>
            <Button variant="string" onClick={handlePostProcessingClick}>
              Post-Processing Room
            </Button>
          </Stack>
        </GreyToolbar>
      </AppBar>
    </>
  );
}


export default NavigationBar;
