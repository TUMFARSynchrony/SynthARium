import "./WatchingRoomTabs.css";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import NotesTab from "../../molecules/NotesTab/NotesTab";
import ParticipantsTab from "../../molecules/ParticipantsTab/ParticipantsTab";
import OverviewTab from "../../molecules/OverviewTab/OverviewTab";

function WatchingRoomTabs() {
  return (
    <div className="watchingRoomTabsContainer">
      <Tabs>
        <TabList>
          <Tab>Overview</Tab>
          <Tab>Notes</Tab>
          <Tab>Paticipants</Tab>
        </TabList>

        <TabPanel>
          <OverviewTab />
        </TabPanel>
        <TabPanel>
          <NotesTab />
        </TabPanel>
        <TabPanel>
          <ParticipantsTab />
        </TabPanel>
      </Tabs>
    </div>
  );
}

export default WatchingRoomTabs;
