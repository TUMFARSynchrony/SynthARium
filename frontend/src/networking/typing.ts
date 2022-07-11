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

/**
 * ConnectionOffer received from the backend connection, offering a subconnection for a new user.
 */
export type ConnectionOffer = {
	id: string,
	offer: {
		sdp: string;
		type: string;
	};
	participant_summary: ParticipantSummary | string | null;
};

/**
 * Checks if all fields of an {@link ConnectionOffer} exist in `data`.
 * Does currently not check the data types or contents of any fields.
 */
export function isValidConnectionOffer(data: any): data is ConnectionOffer {
	return (
		"id" in data
		&& "offer" in data
		&& "sdp" in data.offer
		&& "type" in data.offer
		&& "participant_summary" in data
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
