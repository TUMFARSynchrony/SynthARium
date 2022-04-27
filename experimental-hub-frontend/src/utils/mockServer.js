export function getSessionJson() {
  return [
    {
      id: "",
      time_limit: 180,
      record: true,
      title: "Filter Testing",
      date: 1651075892358,
      start_time: 0,
      end_time: 0,
      notes: [],
      log: "",
      description: "This session is for testing some filters.",
      participants: [
        {
          id: "",
          first_name: "Anna",
          last_name: "Mueller",
          link: "",
          muted: true,
          filters: [],
          position: {
            x: 20,
            y: 50,
            z: 0,
          },
          size: {
            width: 200,
            height: 200,
          },
        },
        {
          id: "",
          first_name: "Max",
          last_name: "Mustermann",
          link: "",
          muted: true,
          filters: [],
          position: {
            x: 10,
            y: 10,
            z: 0,
          },
          size: {
            width: 100,
            height: 100,
          },
        },
      ],
    },
    {
      id: "",
      time_limit: 180,
      record: true,
      title: "Hello World",
      date: 1651075892358,
      start_time: 0,
      end_time: 0,
      notes: [],
      log: "",
      description: "Hello, World!",
      participants: [
        {
          id: "",
          first_name: "Anna",
          last_name: "Mueller",
          link: "",
          muted: true,
          filters: [],
          position: {
            x: 20,
            y: 50,
            z: 0,
          },
          size: {
            width: 200,
            height: 200,
          },
        },
        {
          id: "",
          first_name: "Max",
          last_name: "Mustermann",
          link: "",
          muted: true,
          filters: [],
          position: {
            x: 10,
            y: 10,
            z: 0,
          },
          size: {
            width: 100,
            height: 100,
          },
        },
      ],
    },
  ];
}

export function getEmptySessionJson() {
  return [];
}
