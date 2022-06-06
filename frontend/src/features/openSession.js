import { createSlice } from "@reduxjs/toolkit";

export const openSessionSlice = createSlice({
  name: "openSession",
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
    initializeSession: (state, { payload }) => {
      state.value = payload;
    },

    saveSession: (state, { payload }) => {
      state.value = payload;
    },
  },
});

export const { initializeSession, saveSession } = openSessionSlice.actions;

export default openSessionSlice.reducer;
