import { createSlice } from "@reduxjs/toolkit";
import { filterListById, sortArray } from "../utils/utils";

export const sessionsListSlice = createSlice({
  name: "sessionsList",
  initialState: { value: [] },
  reducers: {
    deleteSession: (state, { payload }) => {
      const newSessionsList = filterListById(state.value, payload);
      state.value = newSessionsList;

      state.value = sortArray(state.value);
    },
    getSessionsList: (state, { payload }) => {
      state.value = payload;
      state.value = sortArray(state.value);
    },
    updateSession: (state, { payload }) => {
      const newSessionsList = filterListById(state.value, payload.id);
      state.value = [...newSessionsList, payload];
      state.value = sortArray(state.value);
    },
    createSession: (state, { payload }) => {
      const newSessionsList = [...state.value, payload];
      state.value = newSessionsList;
      state.value = sortArray(state.value);
    },
  },
});

export const { getSessionsList, deleteSession, createSession, updateSession } =
  sessionsListSlice.actions;

export default sessionsListSlice.reducer;
