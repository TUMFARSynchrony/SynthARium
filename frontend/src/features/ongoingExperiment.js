import { createSlice } from "@reduxjs/toolkit";

export const ongoingExperimentSlice = createSlice({
  name: "ongoingExperiment",
  initialState: {
    value: { sessionId: "", experimentState: "" },
  },
  reducers: {
    createExperiment: (state, { payload }) => {
      const session = { sessionId: "", experimentState: "WAITING" };
      session.sessionId = payload;
      state.value = session;
    },

    startExperiment: (state, { payload }) => {
      state.value.experimentState = payload;
    },
  },
});

export const { createExperiment, startExperiment } =
  ongoingExperimentSlice.actions;

export default ongoingExperimentSlice.reducer;
