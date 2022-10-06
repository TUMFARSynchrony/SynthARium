/**
 * Handler function for an event emitted by an {@link EventHandler}
 */
export type EventHandlerFunction<T> = (data: T) => Promise<void>;

/**
 * EventHandler used to store handlers and emit events. 
 * The type of event data is defined by `T`.
 * 
 * @example ```js
 * // Create new event handler:
 * const eventHandler = new EventHandler<string>();
 * // Define an handler:
 * function handleUpdate(data) {
 *     console.log("Event handler called. data:", data);
 * }
 * // Register event handler:
 * eventHandler.on("update", handleUpdate);
 * // Emit an event:
 * eventHandler.emit("test-data");
 * // log: Event handler called. data: test-data
 * ```
 */
export class EventHandler<T> {
	private eventHandlers: Map<string, EventHandlerFunction<T>[]>;
	private handlerName: string;
	private warnNoHandler: boolean;

	/**
	 * Initiate new EventHandler.
	 * @param warnNoHandler if true, a warning will be logged when an event had no listener.
	 * @param name name of this EventHandler for logging.
	 */
	constructor(warnNoHandler: boolean = true, name: string = "EventHandler") {
		this.eventHandlers = new Map();
		this.handlerName = name;
		this.warnNoHandler = warnNoHandler;
	}

	/**
	 * Register an event handler.
	 * @param event event the handler should listen to.
	 * @param handler handler function for the event.
	 * @see off use off to remove the handler from the EventHandler.
	 */
	public on(event: string, handler: EventHandlerFunction<T>): void {
		if (this.eventHandlers.has(event)) {
			this.eventHandlers.get(event).push(handler);
		} else {
			this.eventHandlers.set(event, [handler]);
		}
	}

	/**
	 * Remove a event handler from the EventHandler.
	 * @param event event the event handler function should be removed from.
	 * @param handler event handler function that should be removed from the EventHandler. 
	 */
	public off(event: string, handler: EventHandlerFunction<T>): void {
		if (!this.eventHandlers.has(event)) {
			return;
		}
		const filtered = this.eventHandlers.get(event).filter(h => h !== handler);
		this.eventHandlers.set(event, filtered);
	}

	/**
	 * Remove all listeners from an specific event or all events.
	 * @param event if given, all handlers of event are removed. Otherwise all handlers for all events are removed.
	 * @see off to remove only a specific handler.
	 */
	public removeAllEventHandlers(event?: string): void {
		if (event) {
			// remove all handlers for the given event
			this.eventHandlers.delete(event);
		} else {
			// Remove all handlers for all events
			this.eventHandlers.clear();
		}
	}

	/**
	 * Emit an event.
	 * @param event event that should be emitted.
	 * @param data data the event contains. Passed to the event handlers.
	 * @returns Promise for completing all event handler calls, or void if none where found.
	 */
	public emit(event: string, data: any): Promise<void[]> {
		const handlers = this.eventHandlers.get(event);

		if (this.warnNoHandler && (!handlers || handlers.length === 0)) {
			console.warn(`[${this.handlerName}] Received event: ${event}, but no handler defined.`);
			return;
		}

		return Promise.all(handlers.map(handler => handler(data)));
	}
}
