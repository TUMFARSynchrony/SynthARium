import { createTheme } from "@mui/material";

export const hubTheme = createTheme({
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    margin: '8px',
                },
            },
        },
        MuiChip: {
            styleOverrides: {
                root: {
                    margin: '8px',
                }
            }
        }
    },
});