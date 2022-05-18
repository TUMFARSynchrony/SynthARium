import { BACKEND } from "../utils/constants";
import SimpleEventHandler from "./ConnectionEvents";

export enum ConnectionState {
  NotStarted,
  Connecting,
  Connected,
  Disconnected
}

export default class Connection {
  // Event handlers
  public connectionStateChange: SimpleEventHandler<ConnectionState>;
  public remoteStreamChange: SimpleEventHandler<MediaStream>;

  readonly sessionId: string;
  readonly participantId?: string;
  readonly userType: "participant" | "experimenter";

  // Private variables
  private _state: ConnectionState

  private localStream: MediaStream;
  private _remoteStream: MediaStream;

  private mainPc: RTCPeerConnection; // RTCPeerConnection | undefined
  private dc: RTCDataChannel;


  constructor(userType: "participant" | "experimenter", sessionId: string, participantId?: string) {
    if (userType === "participant" && !participantId) {
      throw new Error("[Connection] userType participant requires the participantId to be defined.");
    }
    this.sessionId = sessionId;
    this.participantId = participantId;
    this.userType = userType;
    this._state = ConnectionState.NotStarted;
    this._remoteStream = new MediaStream();

    this.remoteStreamChange = new SimpleEventHandler();
    this.connectionStateChange = new SimpleEventHandler();

    this.initMainPeerConnection();
    this.initDataChannel();
  }

  public get remoteStream(): MediaStream {
    return this._remoteStream
  }

  public get state(): ConnectionState {
    return this._state
  }

  public async start(localStream?: MediaStream) {
    if (!localStream && this.userType === "participant") {
      throw new Error("Connection.start(): localStream is required for user type participant.");
    }
    if (this._state !== ConnectionState.NotStarted) {
      throw new Error(`Connection.start(): cannot start Connection, state is: ${ConnectionState[this._state]}`);
    }
    this.localStream = localStream;
    this.setState(ConnectionState.Connecting)

    // Add localStream to peer connection
    console.log("[Connection] Stating -- Adding localStream:", this.localStream);
    this.localStream?.getTracks().forEach((track) => {
      console.log("Adding track", track);
      this.mainPc.addTrack(track, this.localStream);
    });

    await this.negotiate();
  }

  public stop() {
    this.setState(ConnectionState.Disconnected);

    if (!this.mainPc || this.mainPc.connectionState === "closed") return;

    // close transceivers
    if (this.mainPc.getTransceivers) {
      this.mainPc.getTransceivers().forEach(function (transceiver) {
        if (transceiver.stop) {
          transceiver.stop();
        }
      });
    }

    // close local audio / video
    this.mainPc.getSenders().forEach(function (sender) {
      if (sender && sender.track) {
        sender.track.stop();
      };
    });

    // close peer connection
    setTimeout(() => {
      if (this.mainPc) {
        this.mainPc.close();
      }
    }, 500);
  }

  private setState(state: ConnectionState): void {
    this._state = state;
    this.connectionStateChange.trigger(state);
  }

  private initMainPeerConnection() {
    const config: any = {
      sdpSemantics: "unified-plan",
    };
    this.mainPc = new RTCPeerConnection(config);

    // register event listeners for pc
    this.mainPc.addEventListener(
      "icegatheringstatechange",
      () => console.log(`[Connection--MainPc] icegatheringstatechange: ${this.mainPc.iceGatheringState}`),
      false
    );
    this.mainPc.addEventListener(
      "iceconnectionstatechange",
      () => console.log(`[Connection--MainPc] iceConnectionState: ${this.mainPc.iceConnectionState}`),
      false
    );
    this.mainPc.addEventListener(
      "signalingstatechange",
      () => console.log(`[Connection--MainPc] signalingState: ${this.mainPc.signalingState}`),
      false
    );

    // Receive audio / video
    this.mainPc.addEventListener("track", (e) => {
      console.groupCollapsed(`[Connection] Received ${e.track.kind} track from remote`);
      console.log(e);
      console.groupEnd();

      if (e.track.kind !== "video" && e.track.kind !== "audio") {
        console.error("[Connection] Received track with unknown kind:", e.track.kind);
        return;
      }

      this._remoteStream.addTrack(e.track);
      this.remoteStreamChange.trigger(this._remoteStream);
    });
  }

  private initDataChannel() {
    this.dc = this.mainPc.createDataChannel("API");
    this.dc.onclose = (e) => {
      console.log("[Connection] datachannel onclose");
      this.stop();
    };
    this.dc.onopen = (e) => {
      console.log("[Connection] datachannel onopen");
      this.setState(ConnectionState.Connected);
    };
    this.dc.onmessage = (e) => {
      const msgObj = JSON.parse(e.data);
      console.log("[Connection] Received", msgObj);
      // TODO
    };
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
    console.log("[Connection] Sending initial offer");

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
      console.error("[Connection] Failed to connect to backend.", error.message);
      return;
    }

    if (!response.ok) {
      console.error("[Connection] Failed to connect to backend. Response not ok");
      return;
    }


    const answer = await response.json();
    if (answer.type !== "SESSION_DESCRIPTION") {
      console.log(
        "[Connection] Received unexpected answer from backend. type:",
        answer.type
      );
      return;
    }

    console.log("[Connection] Received answer:", answer);

    const remoteDescription = answer.data;
    await this.mainPc.setRemoteDescription(remoteDescription);
  }
}
