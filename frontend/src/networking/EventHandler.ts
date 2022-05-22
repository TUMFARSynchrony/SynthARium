export type EventHandlerFunction<T> = (data: T) => Promise<void>;

export class EventHandler<T> {
	private eventHandlers: Map<string, EventHandlerFunction<T>[]>;
	private handlerName: string;
	private warnNoHandler: boolean;

	constructor(warnNoHandler: boolean = true, name: string = "EventHandler") {
		this.eventHandlers = new Map();
		this.handlerName = name;
		this.warnNoHandler = warnNoHandler;
	}

	public on(event: string, handler: EventHandlerFunction<T>): void {
		if (this.eventHandlers.has(event)) {
			this.eventHandlers.get(event).push(handler);
		} else {
			this.eventHandlers.set(event, [handler]);
		}
	}

	public off(event: string, handler: EventHandlerFunction<T>): void {
		this.eventHandlers.get(event)?.filter(h => h !== handler);
	}

	public removeAllEventHandlers(event?: string): void {
		if (event) {
			// remove all handlers for the given event
			this.eventHandlers.delete(event);
		} else {
			// Remove all handlers for all events
			this.eventHandlers.clear();
		}
	}

	public async trigger(event: string, data: any): Promise<void> {
		const handlers = this.eventHandlers.get(event);

		if (this.warnNoHandler && (!handlers || handlers.length === 0)) {
			console.warn(`[${this.handlerName}] Received event: ${event}, but no handler defined.`);
			return;
		}

		await Promise.all(handlers.map(handler => handler(data)));
	}
}
