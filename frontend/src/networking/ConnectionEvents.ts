export type HandlerFunction<T> = (data?: T) => void

export default class SimpleEventHandler<T> {
	private handlers: HandlerFunction<T>[];

	constructor() {
		this.handlers = [];
	}

	public on(handler: HandlerFunction<T>): void {
		this.handlers.push(handler);
	}

	public off(handler: HandlerFunction<T>): void {
		this.handlers = this.handlers.filter(h => h !== handler)
	}

	public trigger(data?: T): void {
		this.handlers.forEach(handler => handler(data));
	}
}
