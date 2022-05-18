import { BACKEND } from "../utils/constants";

/*
export default class SubConnection {
  pc: RTCPeerConnection; // RTCPeerConnection | undefined
  dc: RTCDataChannel;

  constructor(localStream: MediaStream, sessionId?: string, participantId?: string) {
    this.localStream = localStream;
    this.sessionId = sessionId;
    this.participantId = participantId;
    this.userType = sessionId && participantId ? "participant" : "experimenter";

    this.mainPc = this.initPeerConnection("MAIN PC");
    this.dc = this.initDataChannel(this.mainPc);
  }

  async start() {
    // Add localStream to peer connection
    console.log(this.localStream);
    this.localStream?.getTracks().forEach((track) => {
      console.log("Adding track", track);
      this.mainPc.addTrack(track, this.localStream);
    });

    await this.negotiate();
  }

  stop() {
    // TODO implement
  }

  private initPeerConnection(name: string): RTCPeerConnection {
    const config: any = {
      sdpSemantics: "unified-plan",
    };
    const pc = new RTCPeerConnection(config);

    // register event listeners for pc
    pc.addEventListener(
      "icegatheringstatechange",
      () => console.log(`[${name}] icegatheringstatechange: ${pc.iceGatheringState}`),
      false
    );
    pc.addEventListener(
      "iceconnectionstatechange",
      () => console.log(`[${name}] iceConnectionState: ${pc.iceConnectionState}`),
      false
    );
    pc.addEventListener(
      "signalingstatechange",
      () => console.log(`[${name}] signalingState: ${pc.signalingState}`),
      false
    );

    // Receive audio / video
    pc.addEventListener("track", (e) => {
      console.log("Received a", e.track.kind, "track from remote");
      if (e.track.kind === "video") {
        // TODO:
      } else if (e.track.kind === "audio") {
        // TODO:
      } else {
        // TODO: error?
      }
    });
    return pc
  }

  private initDataChannel(pc: RTCPeerConnection): RTCDataChannel {
    const dc = pc.createDataChannel("API");
    dc.onclose = function () {
      console.log("datachannel onclose");
    };
    dc.onopen = function () {
      console.log("datachannel onopen");
    };
    dc.onmessage = dc.onmessage = (e) => {
      const msgObj = JSON.parse(e.data);
      console.log("Received", msgObj);
      // TODO
    };
    return dc
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

    const response = await fetch(BACKEND + "/offer", {
      body: JSON.stringify({ request }),
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      mode: "cors", // TODO for dev only
    });

    const answer = await response.json();
    if (answer.type !== "SESSION_DESCRIPTION") {
      console.log(
        "Received unexpected answer from backend. type:",
        answer.type
      );
      return;
    }
    const remoteDescription = answer.data;
    await this.mainPc.setRemoteDescription(remoteDescription);
  }
}
*/
