import { EventHandler } from "./EventHandler";


export default class ConnectionBase<T> extends EventHandler<T> {

  protected logging: boolean;
  private name: string;

  constructor(warnNoHandler: boolean, name: string, logging: boolean) {
    super(warnNoHandler, `${name}#Event`);
    this.logging = logging;
    this.name = name;
  }

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

  protected log(message: any, ...optionalParams: any[]): void {
    if (this.logging) {
      console.log(`[${this.name}] ${message}`, ...optionalParams);
    }
  }

  protected logError(message: any, ...optionalParams: any[]): void {
    console.error(`[${this.name}] ${message}`, ...optionalParams);
  }
}
