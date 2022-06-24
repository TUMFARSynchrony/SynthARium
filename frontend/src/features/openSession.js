import { createSlice } from "@reduxjs/toolkit";
import { filterListByIndex } from "../utils/utils";

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

    changeValue: (state, { payload }) => {
      let newSessionData = { ...state.value };
      newSessionData[payload.objKey] = payload.objValue;
      state.value = newSessionData;
    },

    addParticipant: (state, { payload }) => {
      let newSessionData = { ...state.value };
      let newParticipantArray = [...newSessionData.participants, payload];
      newSessionData.participants = newParticipantArray;
      state.value = newSessionData;
    },

    changeParticipant: (state, { payload }) => {
      let newSessionData = { ...state.value };

      let newParticipantArray = [...newSessionData.participants];
      newParticipantArray[payload.index] = {
        ...newParticipantArray[payload.index],
        ...payload.participant,
      };

      newSessionData.participants = newParticipantArray;
      state.value = newSessionData;
    },

    deleteParticipant: (state, { payload }) => {
      let newSessionData = { ...state.value };
      let newParticipantArray = filterListByIndex(
        newSessionData.participants,
        payload.index
      );
      newSessionData.participants = newParticipantArray;
      state.value = newSessionData;
    },

    changeParticipantDimensions: (state, { payload }) => {
      let newSessionData = { ...state.value };

      let newParticipantArray = [...newSessionData.participants];
      newParticipantArray[payload.index].position = payload.position;
      newParticipantArray[payload.index].size = payload.size;

      newSessionData.participants = newParticipantArray;
      state.value = newSessionData;
    },

    copySession: (state, { payload }) => {
      let participants = [...payload.participants];
      participants = participants.map((p) => {
        let newParticipant = { ...p };
        newParticipant.id = "";
        return newParticipant;
      });

      let newSessionData = { ...payload };
      newSessionData.id = "";
      newSessionData.participants = participants;

      state.value = newSessionData;
    },
  },
});

export const {
  initializeSession,
  saveSession,
  changeValue,
  addParticipant,
  changeParticipant,
  deleteParticipant,
  changeParticipantDimensions,
  copySession,
} = openSessionSlice.actions;

export default openSessionSlice.reducer;
