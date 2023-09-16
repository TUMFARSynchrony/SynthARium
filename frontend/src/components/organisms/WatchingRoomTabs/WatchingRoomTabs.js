import { Tab, TabList, TabPanel, Tabs } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import NotesTab from "../../molecules/NotesTab/NotesTab";
import OverviewTab from "../../molecules/OverviewTab/OverviewTab";
import ParticipantsTab from "../../molecules/ParticipantsTab/ParticipantsTab";

function WatchingRoomTabs({
  connectedParticipants,
  onKickBanParticipant,
  onChat,
  onAddNote,
  onLeaveExperiment,
  onStartExperiment,
  onMuteParticipant,
  onEndExperiment,
  onGetSession
}) {
  return (
    <>
      <Tabs>
        <TabList>
          <Tab>Overview</Tab>
          <Tab>Notes</Tab>
          <Tab>Participants</Tab>
        </TabList>

        <TabPanel>
          <OverviewTab
            onLeaveExperiment={onLeaveExperiment}
            onStartExperiment={onStartExperiment}
            onEndExperiment={onEndExperiment}
            onChat={onChat}
            onGetSession={onGetSession}
          />
        </TabPanel>
        <TabPanel>
          <NotesTab onAddNote={onAddNote} />
        </TabPanel>
        <TabPanel>
          <ParticipantsTab
            connectedParticipants={connectedParticipants}
            onKickBanParticipant={onKickBanParticipant}
            onMuteParticipant={onMuteParticipant}
          />
        </TabPanel>
      </Tabs>
    </>
  );
}

export default WatchingRoomTabs;
