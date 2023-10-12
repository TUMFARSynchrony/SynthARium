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
          participant_name: "Anna Mueller",
          link: "",
          muted: true,
          filters: [],
          position: {
            x: 20,
            y: 50,
            z: 0
          },
          size: {
            width: 200,
            height: 200
          }
        },
        {
          id: "",
          participant_name: "Max Mustermann",
          link: "",
          muted: true,
          filters: [],
          position: {
            x: 10,
            y: 10,
            z: 0
          },
          size: {
            width: 100,
            height: 100
          }
        }
      ]
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
          participant_name: "Anna Mueller",
          link: "",
          muted: true,
          filters: [],
          position: {
            x: 20,
            y: 50,
            z: 0
          },
          size: {
            width: 200,
            height: 200
          }
        },
        {
          id: "",
          participant_name: "Max Mustermann",
          link: "",
          muted: true,
          filters: [],
          position: {
            x: 10,
            y: 10,
            z: 0
          },
          size: {
            width: 100,
            height: 100
          }
        }
      ]
    }
  ];
}

export function getEmptySessionJson() {
  return [];
}

export function getJoinedParticipants() {
  return [
    {
      id: "9c93d486fe",
      participant_name: "Max Mustermann",
      muted_video: false,
      muted_audio: false,
      filters: [],
      position: {
        x: 0,
        y: 10,
        z: 10
      },
      size: {
        width: 100,
        height: 100
      },
      chat: [
        {
          message: "Welcome to todays experiment!",
          time: 1650380763075,
          author: "experimenter",
          target: "participants"
        }
      ],
      banned: false
    },
    {
      id: "2d1882e48b",
      participant_name: "Erika Mustermann",
      muted_video: false,
      muted_audio: true,
      filters: [],
      position: {
        x: 0,
        y: 150,
        z: 200
      },
      size: {
        width: 100,
        height: 100
      },
      chat: [
        {
          message: "Welcome to todays experiment!",
          time: 1650380763075,
          author: "experimenter",
          target: "participants"
        },
        {
          message: "Hello Erika. Please enable your video camera to start the experiment.",
          time: 1650380764175,
          author: "experimenter",
          target: "25a882669d"
        },
        {
          message: "Hello, of course. It should work now.",
          time: 1650380765075,
          author: "25a882669d",
          target: "experimenter"
        }
      ],
      banned: false
    }
  ];
}
