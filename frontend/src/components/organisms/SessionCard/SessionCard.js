import Typography from "@mui/material/Typography";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Box from "@mui/material/Box";
import CardActionArea from "@mui/material/CardActionArea";
import Stack from "@mui/material/Stack";
import { integerToDateTime } from "../../../utils/utils";

function SessionCard({ title, date, description, onClick, selected }) {
  return (
    <Card sx={{ mt: 2, mb: 2, borderTop: '3px solid dodgerblue' }} >
      <CardActionArea onClick={onClick}>
        <CardContent>
          <Stack spacing={1}>
            <Typography component='div' variant="subtitle1" align="left" sx={{ color: 'grey', fontWeight: 'bold' }}>
              {title}
            </Typography>
            <Box sx={{ display: "flex", justifyContent: "space-between" }}>
              <Typography>
                {integerToDateTime(date).toLocaleDateString()}
              </Typography>
              <Typography>
                {integerToDateTime(date).toLocaleTimeString()}
              </Typography>
            </Box>
            <Typography align="left" noWrap={true}>
              {description}
            </Typography>
          </Stack>
        </CardContent>
      </CardActionArea>
    </Card>
  );
}

export default SessionCard;
