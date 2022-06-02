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
  },
});

export const { getSessionsList, deleteSession } = sessionsListSlice.actions;

export default sessionsListSlice.reducer;
