import { createSlice } from "@reduxjs/toolkit";

export const ongoingExperimentSlice = createSlice({
  name: "ongoingExperiment",
  initialState: {
    value: {
      id: "",
      title: "",
      description: "",
      date: 0,
      time_limit: 0,
      record: false,
      participants: [],
      start_time: 0,
      end_time: 0,
      notes: [],
      log: "",
    },
  },
  reducers: {
    createExperiment: (state, { payload }) => {
      state.value = payload;
    },
  },
});

export const { createExperiment } = ongoingExperimentSlice.actions;

export default ongoingExperimentSlice.reducer;
