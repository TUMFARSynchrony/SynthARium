import { useEffect } from "react";
import { FiltersData, Participant } from "../../../types";
import { selectFiltersData } from "../../../redux/slices/sessionsListSlice";
import { useAppSelector } from "../../../redux/hooks";

type Props = {
  onGetFiltersData: (data: any) => void;
  participants: Participant[];
};

export const FilterInformationTab = (props: Props) => {
  const { onGetFiltersData, participants } = props;
  const filtersData = useAppSelector(selectFiltersData);

  useEffect(() => {
    function getFiltersData() {
      const filter_id = "all";
      const filter_name = "PING";
      const filter_channel = "video";

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

  const getNameById = (id: string) => {
    const participant = participants.find((participant) => {
      if (participant.id === id) {
        return participant;
      }
    });
    if (participant !== undefined) {
      return participant.participant_name;
    } else {
      return "Unknown";
    }
  };

  return (
    <div className="flex flex-col p-4 border-l-gray-100 border-l-2 h-[calc(100vh-4rem)] w-full items-center gap-y-5">
      <div className="text-3xl">Filter Information</div>
      <div className="w-full flex flex-col h-full items-start space-y-6">
        <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
          <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3">
                Participant
              </th>
              <th scope="col" className="px-6 py-3">
                Ping (ms)
              </th>
            </tr>
          </thead>
          {filtersData !== null &&
            Object.keys(filtersData).map((id) => {
              const name = getNameById(id);
              return filtersData[id].video.map((filter_data) => {
                return Object.keys(filter_data.data).map((key) => {
                  return (
                    <tbody className="text-base text-gray-700 text-center" key={key}>
                      <tr>
                        <td>{name}</td>
                        <td>{Math.round(filter_data.data[key])}</td>
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