import Typography from "@mui/material/Typography";
import { styled } from "@mui/material/styles";

function HeroText({ text }) {
  // This is the main heading of the page - used in Session Overview and
  // the Post Processing Room.
  const Text = styled(Typography)(({ theme }) => ({
    fontWeight: "bold",
    margin: theme.spacing(4)
  }));

  return (
    <>
      <Text variant="h5">{text}</Text>
    </>
  );
}

export default HeroText;
