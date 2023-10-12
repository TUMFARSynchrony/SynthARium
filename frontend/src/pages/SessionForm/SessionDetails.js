import React from "react";
import Box from "@mui/material/Box";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";

function SessionDetails({ sessionData, handleSessionDataChange, numberOfParticipants }) {
  return (
    <div>
      <Typography variant="h6" sx={{ fontWeight: "bold" }}>
        Session Details
      </Typography>
      <Box component="form" sx={{ "& .MuiTextField-root": { m: 1 } }} noValidate autoComplete="off">
        <Box sx={{ "& .MuiTextField-root": { width: "38vw" } }}>
          <TextField
            label="Title"
            value={sessionData.title}
            size="small"
            required
            onChange={(event) => handleSessionDataChange("title", event.target.value)}
          />
          <TextField
            label="Description"
            value={sessionData.description}
            size="small"
            required
            onChange={(event) => handleSessionDataChange("description", event.target.value)}
          />
        </Box>
        <Box sx={{ "& .MuiTextField-root": { width: "18.5vw" } }}>
          <TextField label="Number of Participants" value={numberOfParticipants} type="number" size="small" disabled />
        </Box>
        <Box sx={{ mt: 1, mb: 3 }}>
          <FormControlLabel
            control={
              <Checkbox
                checked={sessionData.record}
                onChange={() => handleSessionDataChange("record", !sessionData.record)}
              />
            }
            label="Record Session"
          />
        </Box>
      </Box>
    </div>
  );
}

export default SessionDetails;
