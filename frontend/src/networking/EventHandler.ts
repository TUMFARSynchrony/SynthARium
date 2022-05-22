export type EventHandlerFunction<T> = (data: T) => Promise<void>;

export class EventHandler<T> {
	private handlers: Map<string, EventHandlerFunction<T>[]>;
	private name: string;
	private warnNoHandler: boolean;

	constructor(warnNoHandler: boolean = true, name: string = "EventHandler") {
		this.handlers = new Map();
		this.name = name;
		this.warnNoHandler = warnNoHandler;
	}

	public on(event: string, handler: EventHandlerFunction<T>): void {
		if (this.handlers.has(event)) {
			this.handlers.get(event).push(handler);
		} else {
			this.handlers.set(event, [handler]);
		}
	}

	public off(event: string, handler: EventHandlerFunction<T>): void {
		this.handlers.get(event)?.filter(h => h !== handler);
	}

	public removeAllEventHandlers(event?: string): void {
		if (event) {
			// remove all handlers for the given event
			this.handlers.delete(event);
		} else {
			// Remove all handlers for all events
			this.handlers.clear();
		}
	}

	public async trigger(event: string, data: any): Promise<void> {
		const handlers = this.handlers.get(event);

		if (this.warnNoHandler && (!handlers || handlers.length === 0)) {
			console.warn(`[${this.name}] Received event: ${event}, but no handler defined.`);
			return;
		}

		await Promise.all(handlers.map(handler => handler(data)));
	}
}
