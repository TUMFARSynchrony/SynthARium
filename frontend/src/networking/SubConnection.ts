import Connection from "./Connection";
import { SimpleEventHandler } from "./ConnectionEvents";
import { ConnectionOffer } from "./MessageTypes";

export default class SubConnection {
  readonly id: string;
  readonly connectionClosed: SimpleEventHandler<string>;
  readonly remoteStreamChange: SimpleEventHandler<MediaStream>;
  readonly remoteStream: MediaStream;

  private pc: RTCPeerConnection;
  private initialOffer: ConnectionOffer;
  private connection: Connection;

  constructor(offer: ConnectionOffer, connection: Connection) {
    this.id = offer.id;
    this.connectionClosed = new SimpleEventHandler();
    this.remoteStreamChange = new SimpleEventHandler();
    this.remoteStream = new MediaStream();
    const config: any = {
      sdpSemantics: "unified-plan",
    };
    this.pc = new RTCPeerConnection(config);
    this.initialOffer = offer;
    this.connection = connection;

    this.log("Initiating SubConnection");

    // register event listeners for pc
    this.pc.addEventListener(
      "icegatheringstatechange",
      () => this.log(`icegatheringstatechange: ${this.pc.iceGatheringState}`),
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
      this.remoteStreamChange.trigger(this.remoteStream);
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
    if (this.pc.connectionState === "closed") return;

    this.log("Stopping");

    // close transceivers
    this.pc.getTransceivers().forEach(function (transceiver) {
      if (transceiver.stop) {
        transceiver.stop();
      }
    });

    this.pc.close();
    this.connectionClosed.trigger(this.id);
  }

  private handleSignalingStateChange() {
    this.log(`signalingState: ${this.pc.signalingState}`);
    if (this.pc.signalingState === "closed") {
      this.stop();
    }
  }

  private handleIceConnectionStateChange() {
    this.log(`iceConnectionState: ${this.pc.iceConnectionState}`);
    if (["disconnected", "closed", "failed"].includes(this.pc.iceConnectionState)) {
      this.stop();
    }
  }

  private log(message: string) {
    console.log(`[SubConnection - ${this.id}] ${message}`);
  }

  private logError(message: string) {
    console.error(`[SubConnection - ${this.id}] ${message}`);
  }
}
