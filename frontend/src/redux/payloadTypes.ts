import { Session } from "../types";
import { BanMuteUnmuteActions, ExperimentTimes } from "../utils/enums";

export type BanMuteUnmuteParticipantPayload = {
  participantId: string;
  action: BanMuteUnmuteActions;
  value: boolean;
  sessionId: string;
};
export type ExperimentTypesPayload = {
  action: ExperimentTimes;
  value: number;
  sessionId: string;
};

export type ChangeValuePayload = {
  objKey: keyof Pick<Session, "title" | "description" | "record" | "date">;
  objValue: Session[keyof Pick<Session, "title" | "description" | "record" | "date">];
};
