import { BACKEND } from "../utils/constants";

export default class Connection {
  messageHandler;
  mainPc; // RTCPeerConnection | undefined
  dc;
  userType;
  sessionId;
  participantId;

  constructor(messageHandler, localStream, sessionId, participantId) {
    this.messageHandler = messageHandler;
    this.localStream = localStream; // optional, required for participant only
    this.sessionId = sessionId; // optional, required for participant only
    this.participantId = participantId; // optional, required for participant only
    this.userType = sessionId && participantId ? "participant" : "experimenter";

    this.#initPeerConnection();
  }

  async start() {
    // Add localStream to peer connection
    console.log(this.localStream);
    this.localStream?.getTracks().forEach((track) => {
      console.log("Adding track", track);
      this.mainPc.addTrack(track, this.localStream);
    });

    await this.#negotiate();
  }

  stop() { }

  sendRequest(type, data) {
    const message = JSON.stringify({ type: type, data: data });
    this.dc.send(message);
  }

  #initPeerConnection() {
    const config = {
      sdpSemantics: "unified-plan",
    };
    this.mainPc = new RTCPeerConnection(config);

    // register event listeners for pc
    this.mainPc.addEventListener(
      "icegatheringstatechange",
      () => {
        console.log("icegatheringstatechange", this.mainPc.iceGatheringState);
      },
      false
    );
    this.mainPc.addEventListener(
      "iceconnectionstatechange",
      () => {
        console.log("iceConnectionState", this.mainPc.iceConnectionState);
      },
      false
    );
    this.mainPc.addEventListener(
      "signalingstatechange",
      () => {
        console.log("signalingState", this.mainPc.signalingState);
      },
      false
    );

    // Setup datachannel
    this.dc = this.mainPc.createDataChannel("chat");
    this.dc.onclose = function () {
      console.log("datachannel onclose");
    };
    this.dc.onopen = function () {
      console.log("datachannel onopen");
    };
    this.dc.onmessage = this.dc.onmessage = (e) => {
      const msgObj = JSON.parse(e.data);
      console.log("Received", msgObj);
      this.messageHandler(msgObj);
    };

    // Receive audio / video
    this.mainPc.addEventListener("track", (e) => {
      console.log("Received a", e.track.kind, "track from remote");
      if (e.track.kind === "video") {
        // TODO:
      } else if (e.track.kind === "audio") {
        // TODO:
      } else {
        // TODO: error?
      }
    });
  }

  async #negotiate() {
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
          if (this.mainPc && this.mainPc.iceGatheringState === "complete") {
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
