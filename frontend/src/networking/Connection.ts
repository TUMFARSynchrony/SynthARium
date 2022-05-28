import { BACKEND, ENVIRONMENT } from "../utils/constants";
import ConnectionBase from "./ConnectionBase";
import ConnectionState from "./ConnectionState";
import { EventHandler } from "./EventHandler";
import { isValidConnectionOffer, isValidMessage, Message, ConnectedPeer } from "./typing";
import SubConnection from "./SubConnection";


/**
 * Class handling the connection with the backend.
 * 
 * Provides {@link EventHandler} events that can be used to detect changes.
 * Provided Events:
 * - `connectionStateChange`: emitted when the connection {@link state} changes. The event contains the current {@link ConnectionState}.
 * - `remoteStreamChange`: emitted when {@link remoteStream} changes. The event contains {@link remoteStream}. 
 *    Changes should be inplace, so replacing the previous data is not required.
 * - `connectedPeersChange`: emitted when {@link connectedPeers} changes. The event contains {@link connectedPeers}. 
 *    Changes should be inplace, so replacing the previous data is not required.
 * 
 * To listen to incoming datachannel messages, use the {@link api} EventHandler.
 *
 * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Technical-Documentation for details about the connection protocol.
 * @see EventHandler
 * @extends ConnectionBase
 */
export default class Connection extends ConnectionBase<ConnectionState | MediaStream | ConnectedPeer[]> {

  /**
   * EventHandler for incoming messages over the datachannel.
   * 
   * @example ```js
   * function handleSuccess(data) {...}
   * function handleError(data) {...}
   * // Register event handlers
   * connection.api.on("SUCCESS", handleSuccess);
   * connection.api.on("ERROR", handleError)
   * ```
   * @see EventHandler
   */
  readonly api: EventHandler<any>;
  readonly sessionId?: string;
  readonly participantId?: string;
  readonly userType: "participant" | "experimenter";

  private _state: ConnectionState;
  private localStream: MediaStream;
  private _remoteStream: MediaStream;
  private mainPc: RTCPeerConnection;
  private dc: RTCDataChannel;
  private subConnections: Map<string, SubConnection>;

  /**
   * Initiate new Connection.
   * 
   * @param userType type of user this connection identify as.
   * @param sessionId session Id. Only required / used if userType === "participant".
   * @param participantId participant Id. Only required / used if userType === "participant".
   * @param logging Whether logging should be enabled. passed to {@link ConnectionBase}
   * 
   * @throws Error if userType === "participant" and one of: participantId or sessionId are missing.  
   * @see Connection class description for details about the class.
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Technical-Documentation for details about the connection protocol.
   */
  constructor(
    userType: "participant" | "experimenter",
    sessionId?: string,
    participantId?: string,
    logging: boolean = false
  ) {
    super(true, "Connection", logging);
    if (userType === "participant" && (!participantId || !sessionId)) {
      throw new Error("userType participant requires the participantId and sessionId to be defined.");
    }
    this.sessionId = sessionId;
    this.participantId = participantId;
    this.userType = userType;
    this.subConnections = new Map();
    this._state = ConnectionState.NEW;
    this._remoteStream = new MediaStream();

    this.api = new EventHandler();
    this.api.on("CONNECTION_OFFER", this.handleConnectionOffer.bind(this));

    this.initMainPeerConnection();
    this.initDataChannel();
  }

  /**
   * Get remote stream of this client. 
   * 
   * The remote stream is the stream received from the backend, based on the stream send from this client.
   */
  public get remoteStream(): MediaStream {
    return this._remoteStream;
  }

  /**
   * Get the streams from other clients connected to the same experiment (peers).
   * @returns MediaStream array containing only the peer streams.
   * @see connectedPeers to get the peer streams and participant summaries. 
   */
  public get peerStreams(): MediaStream[] {
    const streams: MediaStream[] = [];
    this.subConnections.forEach(sc => {
      streams.push(sc.remoteStream);
    });
    return streams;
  }

  /**
   * Get information and streams from other clients connected to the same experiment (peers).
   * @returns list of {@link ConnectedPeer}s
   * @see peerStreams to get only the peer streams without the participant summary.
   */
  public get connectedPeers(): ConnectedPeer[] {
    const connectedPeers: ConnectedPeer[] = [];
    this.subConnections.forEach(sc => {
      connectedPeers.push({
        stream: sc.remoteStream,
        summary: sc.participantSummary
      });
    });
    return connectedPeers;
  }

  /**
   * Get the state the experiment is currently in.
   * @see ConnectionState
   */
  public get state(): ConnectionState {
    return this._state;
  }

  /**
   * Start the connection.
   * @param localStream optional. {@link MediaStream} that is used as the participants stream.  
   * @throws error if `this.userType` === participant and localStream is not given,
   *   or if the connection {@link state} is not NEW.
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Technical-Documentation for details about the connection protocol.
   */
  public async start(localStream?: MediaStream) {
    if (!localStream && this.userType === "participant") {
      throw new Error("Connection.start(): localStream is required for user type participant.");
    }
    if (this._state !== ConnectionState.NEW) {
      throw new Error(`Connection.start(): cannot start Connection, state is: ${ConnectionState[this._state]}`);
    }
    this.localStream = localStream;
    this.setState(ConnectionState.CONNECTING);

    // Add localStream to peer connection
    this.log("Stating -- Adding localStream:", this.localStream);
    this.localStream?.getTracks().forEach((track) => {
      this.log("Adding track", track);
      this.mainPc.addTrack(track, this.localStream);
    });

    await this.negotiate();
  }

  /**
   * Stop the connection.
   * 
   * Changes the state to CLOSED, closes datachannel and all streams and internal connections.
   * 
   * @fires `connectionStateChange` event
   * @param closeSenders default true - If true, streams send by this connection (localstream) will be closed.
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Technical-Documentation for details about the connection protocol.
   */
  public stop(closeSenders: boolean = true) {
    this.internalStop(undefined, closeSenders);
  }

  /**
   * Internal stop function with extended functionality. Intended for internal use only!
   * @fires `connectionStateChange` event
   * @param state default CLOSED - state the connection should set to
   * @param closeSenders default true - If true, streams send by this connection (localstream) will be closed.
   */
  private internalStop(state?: ConnectionState, closeSenders: boolean = true) {
    if ([ConnectionState.CLOSED, ConnectionState.FAILED].includes(this._state)) {
      return;
    }
    this.setState(state ?? ConnectionState.CLOSED);

    this.log("Stopping");

    this.subConnections.forEach(sc => sc.stop());

    this.dc.close();

    // close transceivers
    this.mainPc.getTransceivers().forEach(function (transceiver) {
      if (transceiver.currentDirection && transceiver.currentDirection !== "stopped") {
        transceiver.stop();
      }
    });

    // close local audio / video
    if (closeSenders) {
      this.mainPc.getSenders().forEach(function (sender) {
        if (sender && sender.track) {
          sender.track.stop();
        };
      });
    }

    // close peer connection
    this.mainPc.close();
  }

  /**
   * Construct and send a Message object to the backend using the datachannel.
   * @param endpoint Backend API endpoint / message type. See link bellow for details. 
   * @param data message data. See link bellow for details. 
   * 
   * @throws Error if the connection {@link state} is not CONNECTED.
   * 
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#message Message data type documentation.
   */
  public sendMessage(endpoint: string, data: any) {
    if (this._state !== ConnectionState.CONNECTED) {
      throw Error(`Cannot send message if connection state is not Connected. State: ${ConnectionState[this._state]}`);
    }
    this.logGroup(`Sending ${endpoint} message`, data, true);

    const message: Message = {
      type: endpoint,
      data: data
    };
    const stringified = JSON.stringify(message);
    this.dc.send(stringified);
  }

  /** 
   * Update the connection state.
   * @fires `connectionStateChange` event
   */
  private setState(state: ConnectionState): void {
    this._state = state;
    this.emit("connectionStateChange", state);
  }

  /** Initialize `this.mainPc` and add event listeners. */
  private initMainPeerConnection() {
    const config: any = {
      sdpSemantics: "unified-plan",
    };
    this.mainPc = new RTCPeerConnection(config);

    // register event listeners for pc
    this.mainPc.addEventListener(
      "icegatheringstatechange",
      () => this.log(`IceGatheringStateChange: ${this.mainPc.iceGatheringState}`),
      false
    );
    this.mainPc.addEventListener(
      "iceconnectionstatechange",
      this.handleIceConnectionStateChange.bind(this),
      false
    );
    this.mainPc.addEventListener(
      "signalingstatechange",
      this.handleSignalingStateChange.bind(this),
      false
    );

    // Receive audio / video
    this.mainPc.addEventListener("track", (e) => {
      this.logGroup(`Received ${e.track.kind} track from remote`, e, true);

      if (e.track.kind !== "video" && e.track.kind !== "audio") {
        this.logError("Received track with unknown kind:", e.track.kind);
        return;
      }

      this._remoteStream.addTrack(e.track);
      this.emit("remoteStreamChange", this._remoteStream);
    });
  }

  /** Handle the `iceconnectionstatechange` event on `this.mainPc`. */
  private handleIceConnectionStateChange() {
    this.log(`IceConnectionState: ${this.mainPc.iceConnectionState}`);
    if (["disconnected", "closed"].includes(this.mainPc.iceConnectionState)) {
      this.stop();
      return;
    }
    if (this.mainPc.iceConnectionState === "failed") {
      this.internalStop(ConnectionState.FAILED);
    }
  }

  /** Handle the `signalingstatechange` event on `this.mainPc`. */
  private handleSignalingStateChange() {
    this.log(`SignalingState: ${this.mainPc.signalingState}`);
    if (this.mainPc.signalingState === "closed") {
      this.stop();
    }
  }

  /** Initialize `this.dc` and add event listeners. */
  private initDataChannel() {
    this.dc = this.mainPc.createDataChannel("API");
    this.dc.onclose = (_) => {
      this.log("datachannel closed");
      this.stop();
    };
    this.dc.onopen = (_) => {
      this.log("datachannel opened");
      this.setState(ConnectionState.CONNECTED);
    };
    this.dc.onmessage = this.handleDcMessage.bind(this);
  }

  /**
   * Handle an incoming message on the datachannel. 
   * @param e incoming {@link MessageEvent}
   * 
   * @fires event in `this.api`, if `e` contains valid Message (see link bellow).
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#message Message data type documentation.
   */
  private handleDcMessage(e: MessageEvent<any>) {
    let message;
    try {
      message = JSON.parse(e.data);
    } catch (error) {
      this.logError("Failed to parse datachannel message received from the server.");
      return;
    }
    if (!isValidMessage(message)) {
      this.logError("Received invalid message.", message);
      return;
    }
    this.logGroup("DataChannel: received message", message, false);
    this.api.emit(message.type, message.data);
  }

  /**
   * Negotiate the connection with the backend. 
   * 
   * Used to start the initial / main connection with the backend.
   */
  private async negotiate() {
    const offer = await this.mainPc.createOffer({
      offerToReceiveVideo: true,
      offerToReceiveAudio: true,
    });
    await this.mainPc.setLocalDescription(offer);

    // Wait for iceGatheringState to be "complete".
    await new Promise((resolve) => {
      if (this.mainPc?.iceGatheringState === "complete") {
        resolve(undefined);
      } else {
        const checkState = () => {
          if (this.mainPc?.iceGatheringState === "complete") {
            this.mainPc.removeEventListener(
              "icegatheringstatechange",
              checkState
            );
            resolve(undefined);
          }
        };
        this.mainPc?.addEventListener("icegatheringstatechange", checkState);
      }
    });

    const localDesc = this.mainPc.localDescription;
    let request;
    if (this.userType === "participant") {
      request = {
        sdp: localDesc.sdp,
        type: localDesc.type,
        user_type: "participant",
        session_id: this.sessionId,
        participant_id: this.participantId,
      };
    } else {
      request = {
        sdp: localDesc.sdp,
        type: localDesc.type,
        user_type: "experimenter",
      };
    }
    this.log("Sending initial offer");

    let response;
    try {
      response = await fetch(BACKEND + "/offer", {
        body: JSON.stringify({ request }),
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        mode: ENVIRONMENT === "development" ? "cors" : undefined,
      });
    } catch (error) {
      this.logError("Failed to connect to backend.", error.message);
      this.setState(ConnectionState.FAILED);
      return;
    }

    if (!response.ok) {
      this.logError("Failed to connect to backend. Response not ok");
      this.setState(ConnectionState.FAILED);
      return;
    }


    const answer = await response.json();
    if (answer.type !== "SESSION_DESCRIPTION") {
      this.log("Received unexpected answer from backend. type:", answer.type);
      return;
    }

    this.log("Received answer:", answer);

    this._participantSummary = answer.data.participant_summary;
    const remoteDescription = answer.data;
    await this.mainPc.setRemoteDescription(remoteDescription);
  }

  /**
   * Handle incoming CONNECTION_OFFER messages from the backend connection.
   * 
   * If the offer is valid, start a new SubConnection, add event listeners and store it in `this.subConnections`.
   * @param data message data from the incoming message of type "CONNECTION_OFFER".
   * 
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#message Message data type documentation.
   */
  private async handleConnectionOffer(data: any): Promise<void> {
    if (!isValidConnectionOffer(data)) {
      this.logError("Received invalid CONNECTION_OFFER.");
      return;
    }
    const subConnection = new SubConnection(data, this, this.logging);
    this.subConnections.set(subConnection.id, subConnection);
    subConnection.on("remoteStreamChange", async (_) => {
      this.emit("connectedPeersChange", this.connectedPeers);
    });
    subConnection.on("connectionClosed", async (id) => {
      this.log("SubConnection \"connectionClosed\" event received. Removing SubConnection:", id);
      this.subConnections.delete(id as string);
      this.emit("connectedPeersChange", this.connectedPeers);
    });
    await subConnection.start();
  }
}
