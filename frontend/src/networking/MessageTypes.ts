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
};

export function isValidConnectionOffer(data: any): data is ConnectionOffer {
	return (
		"id" in data
		&& "offer" in data
		&& "sdp" in data.offer
		&& "type" in data.offer
	);
}
