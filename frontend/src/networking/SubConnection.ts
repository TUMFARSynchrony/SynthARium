import Connection from "./Connection";
import ConnectionBase from "./ConnectionBase";
import { ConnectionOffer } from "./MessageTypes";

export default class SubConnection extends ConnectionBase<MediaStream | string> {
  readonly id: string;
  readonly remoteStream: MediaStream;

  private pc: RTCPeerConnection;
  private initialOffer: ConnectionOffer;
  private connection: Connection;
  private stopped: boolean;

  constructor(offer: ConnectionOffer, connection: Connection, logging: boolean) {
    super(true, `SubConnection - ${offer.id}`, logging);
    this.id = offer.id;
    this.remoteStream = new MediaStream();
    const config: any = {
      sdpSemantics: "unified-plan",
    };
    this.pc = new RTCPeerConnection(config);
    this.initialOffer = offer;
    this.connection = connection;
    this.stopped = false;

    this.log("Initiating SubConnection");

    // register event listeners for pc
    this.pc.addEventListener(
      "icegatheringstatechange",
      () => this.log(`IceGatheringStateChange: ${this.pc.iceGatheringState}`),
      false
    );
    this.pc.addEventListener(
      "iceconnectionstatechange",
      this.handleIceConnectionStateChange.bind(this),
      false
    );
    this.pc.addEventListener(
      "signalingstatechange",
      this.handleSignalingStateChange.bind(this),
      false
    );
    // Receive audio / video
    this.pc.addEventListener("track", (e) => {
      this.log(`Received a ${e.track.kind}, track from remote`);
      if (e.track.kind !== "video" && e.track.kind !== "audio") {
        this.logError(`Received track with unknown kind: ${e.track.kind}`);
        return;
      }
      this.remoteStream.addTrack(e.track);
      this.emit("remoteStreamChange", this.remoteStream);

      e.track.onended = () => {
        this.log(`${e.track.kind} track ended`);
      };
      e.track.onmute = () => {
        this.log(`${e.track.kind} track muted`);
      };
      e.track.onunmute = () => {
        this.log(`${e.track.kind} track un-muted`);
      };
    });
  }

  public async start() {
    this.log("Starting SubConnection");
    await this.pc.setRemoteDescription(this.initialOffer.offer as RTCSessionDescriptionInit);
    const answer = await this.pc.createAnswer();
    await this.pc.setLocalDescription(answer);
    const connectionAnswer = {
      id: this.id,
      answer: {
        type: answer.type,
        sdp: answer.sdp
      }
    };
    this.connection.sendMessage("CONNECTION_ANSWER", connectionAnswer);
  }

  public stop() {
    if (this.stopped) {
      return;
    }
    this.stopped = true;
    this.log("Stopping");

    // close transceivers
    this.pc.getTransceivers().forEach(function (transceiver) {
      if (transceiver.stop) {
        transceiver.stop();
      }
    });

    this.pc.close();
    this.emit("connectionClosed", this.id);
  }

  private handleSignalingStateChange() {
    this.log(`SignalingState: ${this.pc.signalingState}`);
    if (this.pc.signalingState === "closed") {
      this.stop();
    }
  }

  private handleIceConnectionStateChange() {
    this.log(`IceConnectionState: ${this.pc.iceConnectionState}`);
    if (["disconnected", "closed", "failed"].includes(this.pc.iceConnectionState)) {
      this.stop();
    }
  }
}
