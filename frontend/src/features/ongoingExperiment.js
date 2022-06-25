import { createSlice } from "@reduxjs/toolkit";

export const ongoingExperimentSlice = createSlice({
  name: "ongoingExperiment",
  initialState: {
    value: "",
  },
  reducers: {
    createExperiment: (state, { payload }) => {
      state.value = payload;
    },
  },
});

export const { createExperiment } = ongoingExperimentSlice.actions;

export default ongoingExperimentSlice.reducer;
