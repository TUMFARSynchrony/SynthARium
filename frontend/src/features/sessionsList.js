import { createSlice } from "@reduxjs/toolkit";
import { filterListById, getSessionById, sortArray } from "../utils/utils";

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

    startSession: (state, { payload }) => {
      const session = getSessionById(payload.id, state.value)[0];
      session["ongoing"] = true;

      const newSessionsList = filterListById(state.value, payload.id);
      state.value = [...newSessionsList, session];
      state.value = sortArray(state.value);
    },

    addNote: (state, { payload }) => {
      const session = getSessionById(payload.id, state.value)[0];
      session.notes.push(payload.note);

      const newSessionsList = filterListById(state.value, payload.id);
      state.value = [...newSessionsList, session];
      state.value = sortArray(state.value);
    },
  },
});

export const {
  getSessionsList,
  deleteSession,
  createSession,
  updateSession,
  startSession,
  addNote,
} = sessionsListSlice.actions;

export default sessionsListSlice.reducer;
