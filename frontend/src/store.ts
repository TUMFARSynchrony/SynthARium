import { configureStore } from "@reduxjs/toolkit";
import sessionsListReducer from "./redux/slices/sessionsListSlice";
import openSessionReducer from "./redux/slices/openSessionSlice";
import ongoingExperimentReducer from "./redux/slices/ongoingExperimentSlice";
import tabsReducer from "./redux/slices/tabsSlice";

export const store = configureStore({
  reducer: {
    sessionsList: sessionsListReducer,
    openSession: openSessionReducer,
    ongoingExperiment: ongoingExperimentReducer,
    tabs: tabsReducer
  }
});

export type RootState = ReturnType<typeof store.getState>;

export type AppDispatch = typeof store.dispatch;
