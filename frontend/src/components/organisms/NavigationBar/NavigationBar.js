import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Stack from "@mui/material/Stack";
import { styled } from '@mui/material/styles';
import { LinkButton } from '../../atoms/Button';

const GreyToolbar = styled(Toolbar)(({ theme }) => ({
  backgroundColor: "#899499",
}));

function NavigationBar() {

  return (
    <>
      <AppBar position="static">
        <GreyToolbar>
          <Stack direction="row">
            <LinkButton text={"Session Overview"} path={"/"} variant="string"/>
            <LinkButton text={"Post-Processing Room"} path={"/postProcessingRoom"} variant="string"/>
          </Stack>
        </GreyToolbar>
      </AppBar>
    </>
  );
}


export default NavigationBar;
