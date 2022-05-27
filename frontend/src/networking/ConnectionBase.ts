import { EventHandler } from "./EventHandler";


/**
 * Base class for Connection and SubConnection. Shared functionality is implemented here.
 * 
 * @extends EventHandler
 */
export default class ConnectionBase<T> extends EventHandler<T> {

  protected logging: boolean;
  private name: string;

  /**
   * Initiate ConnectionBase class instance.
   * @param warnNoHandler If true, the EventHandler will log a warning if there are no handlers for an emitted event.
   * @param name name used for logging and the event handler. EventHandler's name is set to: "<name>#Event"
   * @param logging Whether logging should be enabled.
   */
  constructor(warnNoHandler: boolean, name: string, logging: boolean) {
    super(warnNoHandler, `${name}#Event`);
    this.logging = logging;
    this.name = name;
  }

  /**
   * Log message in a group with contents inside, if `this.logging` is true.
   * @param message Message used as group header.
   * @param contents Contents of the group. Logged inside of the group.
   * @param collapsed If true, `console.groupCollapsed` is used, otherwise `console.group`.
   */
  protected logGroup(message: any, contents: any, collapsed?: boolean): void {
    if (this.logging) {
      if (collapsed) {
        console.groupCollapsed(`[${this.name}] ${message}`);
      } else {
        console.group(`[${this.name}] ${message}`);
      }
      console.log(contents);
      console.groupEnd();
    }
  }

  /**
   * Log message, if `this.logging` is true. Arguments are passed to `console.log`.
   * @param message message that will be logged.
   * @param optionalParams optional parameters for `console.log`.
   */
  protected log(message: any, ...optionalParams: any[]): void {
    if (this.logging) {
      console.log(`[${this.name}] ${message}`, ...optionalParams);
    }
  }

  /**
   * Log error message. Arguments are passed to `console.error`. Ignores `this.logging`.
   * @param message error message that will be logged.
   * @param optionalParams optional parameters for `console.error`.
   */
  protected logError(message: any, ...optionalParams: any[]): void {
    console.error(`[${this.name}] ${message}`, ...optionalParams);
  }
}
