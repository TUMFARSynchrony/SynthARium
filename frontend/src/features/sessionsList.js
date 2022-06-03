import { createSlice } from "@reduxjs/toolkit";
import { filterListById } from "../utils/utils";

export const sessionsListSlice = createSlice({
  name: "sessionsList",
  initialState: { value: [] },
  reducers: {
    deleteSession: (state, { payload }) => {
      const newSessionsList = filterListById(state.value, payload);
      state.value = newSessionsList;
    },
    getSessionsList: (state, { payload }) => {
      state.value = payload;
    },
    updateSession: (state, { payload }) => {
      const newSessionsList = filterListById(state.value, payload.id);
      state.value = [...newSessionsList, payload];
    },
    createSession: (state, { payload }) => {
      const newSessionsList = [...state.value, payload];
      state.value = newSessionsList;
    },
  },
});

export const { getSessionsList, deleteSession, createSession, updateSession } =
  sessionsListSlice.actions;

export default sessionsListSlice.reducer;
