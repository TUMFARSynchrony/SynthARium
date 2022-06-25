import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import NotesTab from "../../molecules/NotesTab/NotesTab";
import ParticipantsTab from "../../molecules/ParticipantsTab/ParticipantsTab";
import OverviewTab from "../../molecules/OverviewTab/OverviewTab";

function WatchingRoomTabs({
  connectedParticipants,
  onKickBanParticipant,
  onAddNote,
  onLeaveExperiment,
  onStartExperiment,
}) {
  return (
    <>
      <Tabs>
        <TabList>
          <Tab>Overview</Tab>
          <Tab>Notes</Tab>
          <Tab>Paticipants</Tab>
        </TabList>

        <TabPanel>
          <OverviewTab
            onLeaveExperiment={onLeaveExperiment}
            onStartExperiment={onStartExperiment}
          />
        </TabPanel>
        <TabPanel>
          <NotesTab onAddNote={onAddNote} />
        </TabPanel>
        <TabPanel>
          <ParticipantsTab
            connectedParticipants={connectedParticipants}
            onKickBanParticipant={onKickBanParticipant}
          />
        </TabPanel>
      </Tabs>
    </>
  );
}

export default WatchingRoomTabs;
