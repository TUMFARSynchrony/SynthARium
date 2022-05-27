import { BACKEND } from "../utils/constants";
import ConnectionBase from "./ConnectionBase";
import ConnectionState from "./ConnectionState";
import { EventHandler } from "./EventHandler";
import { isValidConnectionOffer, isValidMessage, Message } from "./MessageTypes";
import SubConnection from "./SubConnection";


export default class Connection extends ConnectionBase<ConnectionState | MediaStream | MediaStream[]> {
  readonly api: EventHandler<any>;
  readonly sessionId?: string;
  readonly participantId?: string;
  readonly userType: "participant" | "experimenter";

  // Private variables
  private _state: ConnectionState;

  private localStream: MediaStream;
  private _remoteStream: MediaStream;

  private mainPc: RTCPeerConnection; // RTCPeerConnection | undefined
  private dc: RTCDataChannel;

  private subConnections: Map<string, SubConnection>;

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

  public get remoteStream(): MediaStream {
    return this._remoteStream;
  }

  public get peerStreams(): MediaStream[] {
    const streams: MediaStream[] = [];
    this.subConnections.forEach(sc => {
      streams.push(sc.remoteStream);
    });
    return streams;
  }

  public get state(): ConnectionState {
    return this._state;
  }

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

  public stop(closeSenders: boolean = true) {
    this.internalStop(undefined, closeSenders);
  }

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

  private setState(state: ConnectionState): void {
    this._state = state;
    this.emit("connectionStateChange", state);
  }

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

  private handleSignalingStateChange() {
    this.log(`SignalingState: ${this.mainPc.signalingState}`);
    if (this.mainPc.signalingState === "closed") {
      this.stop();
    }
  }

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
        mode: "cors", // TODO for dev only
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

    const remoteDescription = answer.data;
    await this.mainPc.setRemoteDescription(remoteDescription);
  }

  private async handleConnectionOffer(data: any): Promise<void> {
    if (!isValidConnectionOffer(data)) {
      this.logError("Received invalid CONNECTION_OFFER.");
      return;
    }
    const subConnection = new SubConnection(data, this, this.logging);
    this.subConnections.set(subConnection.id, subConnection);
    subConnection.on("remoteStreamChange", async (_) => {
      this.emit("remotePeerStreamsChange", this.peerStreams);
    });
    subConnection.on("connectionClosed", async (id) => {
      this.log("SubConnection \"connectionClosed\" event received. Removing SubConnection:", id);
      this.subConnections.delete(id as string);
      this.emit("remotePeerStreamsChange", this.peerStreams);
    });
    await subConnection.start();
  }
}
