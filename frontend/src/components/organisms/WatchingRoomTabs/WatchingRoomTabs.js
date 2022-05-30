import "./WatchingRoomTabs.css";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import NotesTab from "../NotesTab/NotesTab";

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
          <h2>Participants are here</h2>
        </TabPanel>
      </Tabs>
    </div>
  );
}

export default WatchingRoomTabs;
