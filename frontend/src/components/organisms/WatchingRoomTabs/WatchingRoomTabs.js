import "./WatchingRoomTabs.css";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import NotesTab from "../../molecules/NotesTab/NotesTab";
import ParticipantsTab from "../../molecules/ParticipantsTab/ParticipantsTab";

function WatchingRoomTabs() {
  return (
    <div className="watchingRoomTabsContainer">
      <Tabs>
        <TabList>
          <Tab>Notes</Tab>
          <Tab>Paticipants</Tab>
        </TabList>

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
