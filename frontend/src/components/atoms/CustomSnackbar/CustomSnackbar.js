import MuiAlert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";
import React from "react";

// Using MUI Snackbar and Alert to display notifications in :
// Session Overview Page - when participant invite link is copied to clipboard
// Session Form - upon entry of data and save in the ParticipantDataModal
function CustomSnackbar({ open, text, severity, handleClose }) {
  const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
  });

  return (
    <Snackbar
      open={open}
      autoHideDuration={2000}
      onClose={handleClose}
      anchorOrigin={{ vertical: "top", horizontal: "right" }}
    >
      <Alert onClose={handleClose} severity={severity} sx={{ width: "100%" }}>
        {text}
      </Alert>
    </Snackbar>
  );
}

export default CustomSnackbar;
