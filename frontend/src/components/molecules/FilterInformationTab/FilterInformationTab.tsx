import { useEffect } from "react";
import { FiltersData } from "../../../types";

type Props = {
  onGetFiltersData: (data: any) => void;
  filtersData: FiltersData;
};

export const FilterInformationTab = (props: Props) => {
  const { onGetFiltersData, filtersData } = props;

  useEffect(() => {
    console.log("Loaded FilterInformationTab");
    function getFiltersData() {
      const filter_id = "all";
      const filter_name = "AUDIO_SPEAKING_TIME";
      const filter_channel = "audio";

      const data = {
        filter_id: filter_id,
        filter_channel: filter_channel,
        filter_name: filter_name
      };
      onGetFiltersData(data);
    }
    getFiltersData();
    const interval = setInterval(() => {
      getFiltersData();
    }, 3000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="flex flex-col p-4 border-l-gray-100 border-l-2 h-[calc(100vh-4rem)] w-full items-center gap-y-5">
      <div className="text-3xl">Filter Information</div>
      <div className="w-full flex flex-col h-full items-start space-y-6">
        <table>
          <thead>
            <tr>
              <th>Participant</th>
              <th>Speaking Time</th>
            </tr>
          </thead>
          {console.log(filtersData)}
          {Object.keys(filtersData).map((id) => {
            return filtersData[id].audio.map((filter_data) => {
              return Object.keys(filter_data.data).map((key) => {
                return (
                  <tbody key={key}>
                    <tr>
                      <td>{id}</td>
                      <td>{filter_data.data[key]}</td>
                    </tr>
                  </tbody>
                );
              });
            });
          })}
        </table>
      </div>
    </div>
  );
};
