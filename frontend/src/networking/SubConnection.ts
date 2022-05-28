import Connection from "./Connection";
import ConnectionBase from "./ConnectionBase";
import { ConnectionOffer } from "./typing";

/**
 * SubConnection class used by {@link Connection} to get streams of other users from the backend.
 * 
 * Not intended for use outside of {@link Connection}.
 * 
 * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Technical-Documentation for details about the connection protocol.
 * @extends ConnectionBase
 */
export default class SubConnection extends ConnectionBase<MediaStream | string> {
  readonly id: string;
  readonly remoteStream: MediaStream;

  private pc: RTCPeerConnection;
  private initialOffer: ConnectionOffer;
  private connection: Connection;
  private stopped: boolean;

  /**
   * Initialize new SubConnection.
   * @param offer ConnectionOffer received from the backend, with information on how to open the SubConnection.
   * @param connection parent Connection, used to send data to the backend.
   * @param logging Whether logging should be enabled.
   * 
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Technical-Documentation for details about the connection protocol.
   */
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
    this._participantSummary = offer.participant_summary;

    this.log("Initiating SubConnection");

    // Register event listeners for peer connection (pc)
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

    // handle incoming audio / video tracks
    this.pc.addEventListener("track", (e) => {
      this.log(`Received a ${e.track.kind}, track from remote`);
      if (e.track.kind !== "video" && e.track.kind !== "audio") {
        this.logError(`Received track with unknown kind: ${e.track.kind}`);
        return;
      }
      this.remoteStream.addTrack(e.track);
      this.emit("remoteStreamChange", this.remoteStream);

      // Debug logging - when track state changes
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

  /**
   * Start the subconnection.
   * 
   * Create and send an Answer to the initial offer set in the constructor and send 
   * it to the backend using the connection set in the constructor.
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Technical-Documentation for details about the connection protocol.
   */
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

  /**
   * Stop the SubConnection.
   * 
   * Stop all transceivers associated with this SubConnection and its peer connection. 
   * 
   * Multiple calls to this functions are ignored.
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Technical-Documentation for details about the connection protocol.
   */
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
