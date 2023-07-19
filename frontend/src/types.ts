export type Session = {
  id: string;
  title: string;
  date: number;
  record: boolean;
  time_limit: number;
  description: string;
  creation_time: number;
  end_time: number;
  start_time: number;
  notes: Note[];
  participants: Participant[];
  log: [];
};

export type Note = {
  time: number;
  speakers: string[];
  content: string;
};

export type Participant = {
  id: string;
  participant_name: string;
  banned: boolean;
  size: { width: number; height: number };
  muted_video: boolean;
  muted_audio: boolean;
  position: { x: number; y: number; z: number };
  chat: Chat[];
  audio_filters: [];
  video_filters: VideoFilter[];
};

export type Box = {
  x: number;
  y: number;
  width: number;
  height: number;
};

export type Shape = {
  x: number;
  y: number;
  fill: string;
  participant_name: string;
};

export type Group = {
  x: number;
  y: number;
  width: number;
  height: number;
};

type VideoFilter = {
  id: string;
  type: string;
};

export type Chat = {
  message: string;
  time: number;
  author: string;
  target: string;
};
