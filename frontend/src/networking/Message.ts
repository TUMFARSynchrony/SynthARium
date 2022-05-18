export type Message = {
	type: string,
	data: any;
};

export function isValidMessage(data: any) {
	return "type" in data && typeof data.type === 'string' && "data" in data;
}
