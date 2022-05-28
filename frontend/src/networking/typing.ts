export type Message = {
	type: string,
	data: any;
};

export function isValidMessage(data: any): data is Message {
	return "type" in data && typeof data.type === 'string' && "data" in data;
}

export type ConnectionOffer = {
	id: string,
	offer: {
		sdp: string;
		type: string;
	};
	participant_summary: ParticipantSummary | null;
};

export function isValidConnectionOffer(data: any): data is ConnectionOffer {
	return (
		"id" in data
		&& "offer" in data
		&& "sdp" in data.offer
		&& "type" in data.offer
		&& "participant_summary" in data
	);
}

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

export type ConnectedPeer = {
	stream: MediaStream,
	summary: ParticipantSummary | null;
};
