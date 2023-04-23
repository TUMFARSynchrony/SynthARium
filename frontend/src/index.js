import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { configureStore } from "@reduxjs/toolkit";
import { Provider } from "react-redux";
import sessionsListReducer from "./features/sessionsList";
import openSessionReducer from "./features/openSession";
import ongoingExperimentReducer from "./features/ongoingExperiment";
import "react-toastify/dist/ReactToastify.css";
import { BrowserRouter as Router } from "react-router-dom";
import ThemeProvider from "@mui/material/styles/ThemeProvider";
import { hubTheme } from "./styles/hubTheme";

const store = configureStore({
  reducer: {
    sessionsList: sessionsListReducer,
    openSession: openSessionReducer,
    ongoingExperiment: ongoingExperimentReducer,
  },
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <ThemeProvider theme={hubTheme}>
    <Provider store={store}>
      <Router>
        <App />
      </Router>
    </Provider>
  </ThemeProvider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
