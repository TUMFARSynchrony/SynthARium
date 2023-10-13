import { createTheme } from "@mui/material";

// These style changes apply to the components across the entire application (uses a common theme).
const hubTheme = createTheme({
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          margin: "8px"
        }
      }
    },
    MuiChip: {
      styleOverrides: {
        root: {
          margin: "8px"
        }
      }
    }
  }
});
export default { hubTheme };
