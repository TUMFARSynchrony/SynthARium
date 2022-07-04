/**
 * Message send by / to the backend.
 * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#message Message data type documentation.
 */
export type Message = {
	type: string,
	data: any;
};

/**
 * Checks if `data` is a valid {@link Message}. Does not check the type or contents of the `data` field in message.
 * @param data data that should be checked for {@link Message} type
 * @returns true if `data` is a valid {@link Message}
 */
export function isValidMessage(data: any): data is Message {
	return "type" in data && typeof data.type === 'string' && "data" in data;
}

/** TODO document */
function isValidConnectionRTCSessionDescriptionInit(data: any): data is RTCSessionDescriptionInit {
	return "sdp" in data && "type" in data;
}

/** TODO document */
export type ConnectionProposal = {
	id: string,
	participant_summary: ParticipantSummary | string | null;
};

/** TODO document */
export function isValidConnectionProposal(data: any): data is ConnectionProposal {
	return "id" in data && "participant_summary" in data;
}

/** TODO document */
export type ConnectionOffer = {
	id: string,
	offer: RTCSessionDescriptionInit;
};

/** TODO document */
export type ConnectionAnswer = {
	id: string;
	answer: RTCSessionDescriptionInit;
};

/** TODO document */
export function isValidConnectionAnswer(data: any): data is ConnectionAnswer {
	return (
		"id" in data
		&& "answer" in data
		&& isValidConnectionRTCSessionDescriptionInit(data.answer)
	);
}

/**
 * Summary of a participant.
 * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#participantsummary ParticipantSummary data type documentation.
 */
export type ParticipantSummary = {
	first_name: string,
	last_name: string,
	position: {
		x: number,
		y: number,
		z: number,
	};
	size: {
		width: number,
		height: number,
	};
	chat: {
		message: string,
		time: number,
		author: string,
		target: string,
	}[];
};

/**
 * Information about a connected peer the {@link Connection} has.
 */
export type ConnectedPeer = {
	stream: MediaStream,
	summary: ParticipantSummary | string | null;
};
