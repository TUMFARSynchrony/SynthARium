import Connection from "./Connection";
import ConnectionBase from "./ConnectionBase";
import { ConnectionAnswer, ConnectionOffer, ConnectionProposal } from "./typing";

/**
 * SubConnection class used by {@link Connection} to get streams of other users from the backend.
 * 
 * Not intended for use outside of {@link Connection}.
 * 
 * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol for details about the connection protocol.
 * @extends ConnectionBase
 */
export default class SubConnection extends ConnectionBase<MediaStream | string> {
  readonly id: string;
  readonly remoteStream: MediaStream;

  private pc: RTCPeerConnection;
  private connection: Connection;
  private stopped: boolean;

  /**
   * TODO update docs 
   * 
   * Initialize new SubConnection.
   * @param offer ConnectionOffer received from the backend, with information on how to open the SubConnection.
   * @param connection parent Connection, used to send data to the backend.
   * @param logging Whether logging should be enabled.
   * 
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol for details about the connection protocol.
   */
  constructor(proposal: ConnectionProposal, connection: Connection, logging: boolean) {
    super(true, `SubConnection - ${proposal.id}`, logging);
    this.id = proposal.id;
    this.remoteStream = new MediaStream();
    const config: any = {
      sdpSemantics: "unified-plan",
    };
    this.pc = new RTCPeerConnection(config);
    this.connection = connection;
    this.stopped = false;
    this._participantSummary = proposal.participant_summary;

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
   * TODO update docs
   * 
   * Create and send an Answer to the initial offer set in the constructor and send 
   * it to the backend using the connection set in the constructor.
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol for details about the connection protocol.
   */
  public async sendOffer() {
    this.log("Generating & sending offer");
    const offer = await this.pc.createOffer({
      offerToReceiveVideo: true,
      offerToReceiveAudio: true,
    });
    await this.pc.setLocalDescription(offer);

    // Wait for iceGatheringState to be "complete".
    await new Promise((resolve) => {
      if (this.pc?.iceGatheringState === "complete") {
        resolve(undefined);
      } else {
        const checkState = () => {
          if (this.pc?.iceGatheringState === "complete") {
            this.pc.removeEventListener(
              "icegatheringstatechange",
              checkState
            );
            resolve(undefined);
          }
        };
        this.pc?.addEventListener("icegatheringstatechange", checkState);
      }
    });

    const connectionOffer: ConnectionOffer = {
      id: this.id,
      offer: {
        sdp: this.pc.localDescription.sdp,
        type: this.pc.localDescription.type,
      }
    };
    this.connection.sendMessage("CONNECTION_OFFER", connectionOffer);
  }

  /** TODO document */
  public async handleAnswer(answer: ConnectionAnswer) {
    // TODO Check if answer already handled
    await this.pc.setRemoteDescription(answer.answer);
  }

  /**
   * Stop the SubConnection.
   * 
   * Stop all transceivers associated with this SubConnection and its peer connection. 
   * 
   * Multiple calls to this functions are ignored.
   * @see https://github.com/TUMFARSynchorny/experimental-hub/wiki/Connection-Protocol for details about the connection protocol.
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
