import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "../../store";

type OngoingExperimentState = {
  sessionId: string;
  experimentState: string;
};

const initialState: OngoingExperimentState = {
  sessionId: "",
  experimentState: ""
};

export const ongoingExperimentSlice = createSlice({
  name: "ongoingExperiment",
  initialState,
  reducers: {
    createExperiment: (state, { payload }) => {
      state.sessionId = payload;
      state.experimentState = "WAITING";
    },

    joinExperiment: (state, { payload }) => {
      state.sessionId = payload;
    },

    changeExperimentState: (state, { payload }) => {
      state.experimentState = payload;
    }
  }
});

export const { createExperiment, changeExperimentState, joinExperiment } =
  ongoingExperimentSlice.actions;

export default ongoingExperimentSlice.reducer;

export const selectOngoingExperiment = (state: RootState) =>
  state.ongoingExperiment;
