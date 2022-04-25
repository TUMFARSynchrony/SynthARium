export function getSessionJson() {
  return [
    {
      sessionID: "filter_testing_10012021_1200",
      timeLimit: 180,
      recordSession: true,
      title: "Filter Testing",
      date: "10.01.2021",
      time: "12:00 CET",
      participant: [
        {
          userID: "maria_pospelova_24042000",
          xPosition: 1336,
          yPosition: 1020,
          muted: true,
          filters: [],
        },
        {
          userID: "max_mustermann_24042000",
          xPosition: 4200,
          yPosition: 6969,
          muted: true,
          filters: [],
        },
      ],
    },
    {
      sessionID: "hello_world_08122022_1300",
      timeLimit: 180,
      recordSession: true,
      title: "Hello World",
      date: "08.12.2022",
      time: "13:00 CET",
      users: [
        {
          userID: "maria_pospelova_24042000",
          xPosition: 1336,
          yPosition: 1020,
          muted: true,
          filters: [],
        },
        {
          userID: "max_mustermann_24042000",
          xPosition: 4200,
          yPosition: 6969,
          muted: true,
          filters: [],
        },
      ],
    },
  ];
}

export function getEmptySessionJson() {
  return [];
}
