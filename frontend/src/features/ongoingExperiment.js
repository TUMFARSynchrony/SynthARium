import { createSlice } from "@reduxjs/toolkit";

export const ongoingExperimentSlice = createSlice({
  name: "ongoingExperiment",
  initialState: {
    value: { sessionId: "", experimentState: "" },
  },
  reducers: {
    createExperiment: (state, { payload }) => {
      const session = { sessionId: payload, experimentState: "WAITING" };
      state.value = session;
    },

    joinExperiment: (state, { payload }) => {
      const session = { ...state.value };
      session.sessionId = payload;

      state.value = session;
    },

    changeExperimentState: (state, { payload }) => {
      state.value.experimentState = payload;
    },
  },
});

export const { createExperiment, changeExperimentState, joinExperiment } =
  ongoingExperimentSlice.actions;

export default ongoingExperimentSlice.reducer;
