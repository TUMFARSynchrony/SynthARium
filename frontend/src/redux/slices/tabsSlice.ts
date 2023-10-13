import { createSlice } from "@reduxjs/toolkit";
import { Tabs } from "../../utils/enums";
import { RootState } from "../../store";

const initialState = {
  chatTabActive: true,
  instructionsTabActive: false,
  participantsTabActive: false
};

export const tabsSlice = createSlice({
  name: "tabs",
  initialState,
  reducers: {
    closeAllTabs: (state) => {
      state.chatTabActive = false;
      state.instructionsTabActive = false;
      state.participantsTabActive = false;
    },
    toggleSingleTab: (state, { payload }) => {
      const tab: Tabs = payload;
      switch (tab) {
        case Tabs.CHAT:
          state.chatTabActive = !state.chatTabActive;
          state.instructionsTabActive = false;
          state.participantsTabActive = false;
          break;
        case Tabs.INSTRUCTIONS:
          state.chatTabActive = false;
          state.instructionsTabActive = !state.instructionsTabActive;
          state.participantsTabActive = false;
          break;
        case Tabs.PARTICIPANTS:
          state.chatTabActive = false;
          state.instructionsTabActive = false;
          state.participantsTabActive = !state.participantsTabActive;
          break;
        default:
        // do nothing all cases covered
      }
    }
  }
});

export const { closeAllTabs, toggleSingleTab } = tabsSlice.actions;

export default tabsSlice.reducer;

export const selectChatTab = (state: RootState) => state.tabs.chatTabActive;
export const selectInstructionsTab = (state: RootState) => state.tabs.instructionsTabActive;

export const selectParticipantsTab = (state: RootState) => state.tabs.participantsTabActive;
