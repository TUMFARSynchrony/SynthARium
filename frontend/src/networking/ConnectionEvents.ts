export type HandlerFunction<T> = (data?: T) => void;

export class SimpleEventHandler<T> {
	private handlers: HandlerFunction<T>[];

	constructor() {
		this.handlers = [];
	}

	public on(handler: HandlerFunction<T>): void {
		this.handlers.push(handler);
	}

	public off(handler: HandlerFunction<T>): void {
		this.handlers = this.handlers.filter(h => h !== handler);
	}

	public trigger(data?: T): void {
		this.handlers.forEach(handler => handler(data));
	}
}

export type ApiHandlerFunction = (data: any) => Promise<void>;

export class ApiHandler {
	private handlers: Map<string, ApiHandlerFunction[]>;

	constructor() {
		this.handlers = new Map();
	}

	public on(endpoint: string, handler: ApiHandlerFunction): void {
		if (this.handlers.has(endpoint)) {
			this.handlers.get(endpoint).push(handler);
		} else {
			this.handlers.set(endpoint, [handler]);
		}
	}

	public off(endpoint: string, handler: ApiHandlerFunction): void {
		this.handlers.get(endpoint)?.filter(h => h !== handler);
	}

	public async trigger(endpoint: string, data: any): Promise<void> {
		const handlers = this.handlers.get(endpoint);

		if (!handlers || handlers.length === 0) {
			console.warn(`[ApiHandler] Received message for endpoint: ${endpoint}, but no handler defined.`);
			return;
		}

		await Promise.all(handlers.map(handler => handler(data)));
	}
}
