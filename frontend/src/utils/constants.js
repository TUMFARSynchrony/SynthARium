export const INITIAL_SESSION_DATA = {
  id: "",
  title: "",
  description: "",
  date: 0,
  time_limit: 0,
  record: false,
  participants: [],
  start_time: 0,
  end_time: 0,
  notes: [],
  log: "",
};

export const CANVAS_SIZE = {
  width: 1138.333, // 1366
  height: 640, //768
  scale: 1.2,
};

export const INITIAL_PARTICIPANT_DATA = {
  id: "",
  first_name: "",
  last_name: "",
  link: "",
  muted_audio: true,
  muted_video: true,
  filters: [],
  position: {
    x: 0,
    y: 0,
    z: 0,
  },
  size: {
    width: 0,
    height: 0,
  },
};

export const BACKEND = "http://127.0.0.1:8080";
