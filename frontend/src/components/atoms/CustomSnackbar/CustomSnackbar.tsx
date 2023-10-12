import MuiAlert, { AlertColor, AlertProps } from "@mui/material/Alert";
import Snackbar, { SnackbarOrigin } from "@mui/material/Snackbar";
import { forwardRef } from "react";

type CustomSnackbarProps = {
  open: boolean;
  text: string;
  severity: AlertColor;
  handleClose: () => void;
  autoHideDuration?: number;
  anchorOrigin?: SnackbarOrigin;
};

// Using MUI Snackbar and Alert to display notifications in :
// Session Overview Page - when participant invite link is copied to clipboard
// Session Form - upon entry of data and save in the ParticipantDataModal
function CustomSnackbar({
  open,
  text,
  severity,
  autoHideDuration,
  handleClose,
  anchorOrigin
}: CustomSnackbarProps) {
  const Alert = forwardRef<HTMLDivElement, AlertProps>(function Alert(props, ref): JSX.Element {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
  });
  return (
    <Snackbar
      open={open}
      autoHideDuration={autoHideDuration ?? 2000}
      onClose={handleClose}
      anchorOrigin={anchorOrigin ?? { vertical: "top", horizontal: "right" }}
    >
      <Alert onClose={handleClose} severity={severity} sx={{ width: "100%" }}>
        {text}
      </Alert>
    </Snackbar>
  );
}

export default CustomSnackbar;
