import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { Provider } from "react-redux";
import "react-toastify/dist/ReactToastify.css";
import { BrowserRouter as Router } from "react-router-dom";
import ThemeProvider from "@mui/material/styles/ThemeProvider";
import { hubTheme } from "./styles/hubTheme";
import { store } from "./store";
import { NextUIProvider } from "@nextui-org/react";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <ThemeProvider theme={hubTheme}>
    <Provider store={store}>
      <Router>
        <NextUIProvider>
          <App />
        </NextUIProvider>
      </Router>
    </Provider>
  </ThemeProvider>
);
