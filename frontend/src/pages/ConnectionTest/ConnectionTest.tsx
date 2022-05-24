import * as React from "react";
import { useRef, useEffect, useState } from "react";

import "./ConnectionTest.css";
import Connection, { ConnectionState } from "../../networking/Connection";


const ConnectionTest = (props: {
  localStream?: MediaStream,
  connection: Connection,
  setConnection: (connection: Connection) => void,
}) => {
  const connection = props.connection;
  const [audioIsMuted, setAudioIsMuted] = useState(!props.localStream?.getAudioTracks()[0].enabled ?? false);
  const [videoIsMuted, setVideoIsMuted] = useState(!props.localStream?.getVideoTracks()[0].enabled ?? false);
  const [connectionState, setConnectionState] = useState(connection.state);
  const [peerStreams, setPeerStreams] = useState<MediaStream[]>([]);

  const streamChangeHandler = async (_: MediaStream) => {
    console.log("%cRemote Stream Change Handler", "color:blue");
  };
  const stateChangeHandler = async (state: ConnectionState) => {
    console.log(`%cConnection state change Handler: ${ConnectionState[state]}`, "color:blue");
    setConnectionState(state);
  };
  const peerStreamChangeHandler = async (streams: MediaStream[]) => {
    console.log(`%cConnection peer streams change Handler: ${streams}`, "color:blue");
    setPeerStreams(streams);
  };

  // Register Connection event handlers 
  useEffect(() => {
    connection.on("remoteStreamChange", streamChangeHandler);
    connection.on("connectionStateChange", stateChangeHandler);
    connection.on("remotePeerStreamsChange", peerStreamChangeHandler);
    return () => {
      // Remove event handlers when component is deconstructed
      connection.off("remoteStreamChange", streamChangeHandler);
      connection.off("connectionStateChange", stateChangeHandler);
      connection.off("remotePeerStreamsChange", peerStreamChangeHandler);
    };
  }, [connection]);

  // Update audioIsMuted and videoIsMuted when localStream changes
  useEffect(() => {
    if (props.localStream) {
      setAudioIsMuted(!props.localStream.getAudioTracks()[0].enabled);
      setVideoIsMuted(!props.localStream.getVideoTracks()[0].enabled);
    }
  }, [props.localStream]);

  /**
   * Mute audio in localstream.
   * @See {@link https://developer.mozilla.org/en-US/docs/Web/API/MediaStreamTrack/enabled}
   */
  const muteAudio = () => {
    if (props.localStream) {
      console.log(`${audioIsMuted ? "Unmute" : "Mute"} Audio`, audioIsMuted);
      props.localStream.getAudioTracks()[0].enabled = audioIsMuted;
      setAudioIsMuted(!audioIsMuted);
    }
  };

  /**
   * Mute video in localstream.
   * @See {@link https://developer.mozilla.org/en-US/docs/Web/API/MediaStreamTrack/enabled}
   */
  const muteVideo = () => {
    if (props.localStream) {
      console.log(`${videoIsMuted ? "Unmute" : "Mute"} Video`, videoIsMuted);
      props.localStream.getVideoTracks()[0].enabled = videoIsMuted;
      setVideoIsMuted(!videoIsMuted);
    }
  };

  return (
    <div className="ConnectionTestPageWrapper">
      <h1>ConnectionTest</h1>
      <p>Connection State:
        <span className={`connectionState ${ConnectionState[connectionState]}`}>{ConnectionState[connectionState]}</span>
      </p>
      <button onClick={() => connection.start(props.localStream)} disabled={connection.state !== ConnectionState.NEW}>Start Connection</button>
      <button onClick={() => connection.stop()} disabled={connection.state !== ConnectionState.CONNECTED}>Stop Connection</button>
      {connection.state === ConnectionState.NEW ? <ReplaceConnection connection={connection} setConnection={props.setConnection} /> : ""}
      <div className="ownStreams">
        <Video title="local stream" srcObject={props.localStream ?? new MediaStream()} />
        <Video title="remote stream" srcObject={connection.remoteStream} />
      </div>{props.localStream ?
        <>
          <button onClick={muteAudio}>{audioIsMuted ? "Unmute" : "Mute"} localStream Audio</button>
          <button onClick={muteVideo}>{videoIsMuted ? "Unmute" : "Mute"} localStream Video</button>
        </> : ""
      }
      <button onClick={() => console.log(connection)}>Print Debug</button>
      <p><b>Peer Streams</b> ({peerStreams.length}):</p>
      <div className="peerStreams">
        {peerStreams.map((stream, i) => <Video title={`Peer stream ${i}`} srcObject={stream} key={i} />)}
      </div>
      <ApiTests connection={connection} />
    </div>
  );
};

export default ConnectionTest;


function ApiTests(props: { connection: Connection; }): JSX.Element {
  const [responses, setResponses] = useState<{ endpoint: string, data: string; }[]>([]);
  const [highlightedResponse, setHighlightedResponse] = useState(0);
  const [sessionId, setSessionId] = useState(props.connection.sessionId ?? "");
  const [participantId, setParticipantId] = useState(props.connection.participantId ?? "");

  useEffect(() => {
    const saveGenericApiResponse = async (endpoint: string, response_Data: any) => {
      // Add message received by api to responses and reset highlightedResponse  
      setResponses([{ endpoint: endpoint, data: response_Data }, ...responses]);
      setHighlightedResponse(0);
    };

    const handleSessionList = (data: any) => saveGenericApiResponse("SESSION_LIST", data);
    const handleSuccess = (data: any) => saveGenericApiResponse("SUCCESS", data);
    const handleError = (data: any) => saveGenericApiResponse("ERROR", data);
    const handleExperimentEnded = (data: any) => saveGenericApiResponse("EXPERIMENT_ENDED", data);
    const handleExperimentStarted = (data: any) => saveGenericApiResponse("EXPERIMENT_STARTED", data);
    const handleKickNotification = (data: any) => saveGenericApiResponse("KICK_NOTIFICATION", data);

    props.connection.api.on("SESSION_LIST", handleSessionList);
    props.connection.api.on("SUCCESS", handleSuccess);
    props.connection.api.on("ERROR", handleError);
    props.connection.api.on("EXPERIMENT_ENDED", handleExperimentEnded);
    props.connection.api.on("EXPERIMENT_STARTED", handleExperimentStarted);
    props.connection.api.on("KICK_NOTIFICATION", handleKickNotification);

    return () => {
      props.connection.api.off("SESSION_LIST", handleSessionList);
      props.connection.api.off("SUCCESS", handleSuccess);
      props.connection.api.off("ERROR", handleError);
      props.connection.api.off("EXPERIMENT_ENDED", handleExperimentEnded);
      props.connection.api.off("EXPERIMENT_STARTED", handleExperimentStarted);
      props.connection.api.off("KICK_NOTIFICATION", handleKickNotification);
    };
  }, [props.connection.api, responses]);

  return (
    <>
      {props.connection.userType === "participant"
        ? <p className="apiWarning"><b>Note:</b> API should only work for experimenters</p>
        : <></>
      }
      <div className="requestButtons">
        <button
          onClick={() => props.connection.sendMessage("GET_SESSION_LIST", {})}
          disabled={props.connection.state !== ConnectionState.CONNECTED}
        >
          GET_SESSION_LIST
        </button>
        <button
          onClick={() => props.connection.sendMessage("STOP_EXPERIMENT", {})}
          disabled={props.connection.state !== ConnectionState.CONNECTED}
        >
          STOP_EXPERIMENT
        </button>
        <div className="inputBtnBox">
          <input
            type="text"
            placeholder="Session ID"
            onChange={(e) => setSessionId(e.target.value)}
            value={sessionId}
          />
          <button
            onClick={() => props.connection.sendMessage("CREATE_EXPERIMENT", { session_id: sessionId })}
            disabled={props.connection.state !== ConnectionState.CONNECTED}
          >
            CREATE_EXPERIMENT
          </button>
          <button
            onClick={() => props.connection.sendMessage("JOIN_EXPERIMENT", { session_id: sessionId })}
            disabled={props.connection.state !== ConnectionState.CONNECTED}
          >
            JOIN_EXPERIMENT
          </button>
        </div>
        <div className="inputBtnBox">
          <input
            type="text"
            placeholder="Participant ID"
            onChange={(e) => setParticipantId(e.target.value)}
            value={participantId}
          />
          <button
            onClick={() => props.connection.sendMessage("KICK_PARTICIPANT", { participant_id: participantId, reason: "Testing." })}
            disabled={props.connection.state !== ConnectionState.CONNECTED}
          >
            KICK_PARTICIPANT
          </button>
          <button
            onClick={() => props.connection.sendMessage("BAN_PARTICIPANT", { participant_id: participantId, reason: "Testing." })}
            disabled={props.connection.state !== ConnectionState.CONNECTED}
          >
            BAN_PARTICIPANT
          </button>
        </div>
      </div>
      <div className="basicTabs">
        <span className="tabsTitle">Responses:</span>
        {responses.map((response, index) => {
          return <button key={index}
            onClick={() => setHighlightedResponse(index)}
            className={index === highlightedResponse ? "" : "secondary"}
          >{response.endpoint}
          </button>;
        })}
      </div>
      {responses.length > 0 ? <PrettyJson json={responses[highlightedResponse].data} /> : ""}
    </>
  );
}

function PrettyJson(props: { json: any; }) {
  return (
    <div className="prettyJson">
      <pre>{JSON.stringify(props.json, null, 4)}</pre>
    </div>
  );
}

function ReplaceConnection(props: {
  connection: Connection,
  setConnection: (connection: Connection) => void,
}) {
  const [userType, setUserType] = useState<"participant" | "experimenter">(props.connection.userType);
  const [sessionId, setSessionId] = useState(props.connection.sessionId ?? "");
  const [participantId, setParticipantId] = useState(props.connection.participantId ?? "");

  const updateConnection = (userType: "participant" | "experimenter", sessionId: string, participantId: string) => {
    console.log(`%c[ReplaceConnection] Replaced connection with new parameters: ${userType}, ${sessionId}, ${participantId}`, "color:darkgreen");
    const connection = new Connection(userType, sessionId, participantId);
    props.setConnection(connection);
  };

  const handleUserType = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newUserType = e.target.value as "participant" | "experimenter";
    setUserType(newUserType);
    updateConnection(newUserType, sessionId, participantId);
  };

  const handleSessionId = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSessionId(e.target.value);
    updateConnection(userType, e.target.value, participantId);
  };

  const handleParticipantId = (e: React.ChangeEvent<HTMLInputElement>) => {
    setParticipantId(e.target.value);
    updateConnection(userType, sessionId, e.target.value);
  };

  const info = "Replace connection before connecting to change the user type, session id or participant id";

  return (
    <div className="replaceConnectionWrapper">
      <span title={info}>Replace Connection:</span>
      <form className="replaceConnectionForm">
        <label>Type:&nbsp;&nbsp;
          <select
            defaultValue={props.connection.userType}
            onChange={handleUserType}
          >
            <option value="participant">Participant</option>
            <option value="experimenter">Experimenter</option>
          </select>
        </label>
        {
          userType === "participant" ? <>
            <label>Session ID:&nbsp;&nbsp;
              <input
                type="text"
                onChange={handleSessionId}
                defaultValue={props.connection.sessionId}
              />
            </label>
            <label>ParticipantID:&nbsp;&nbsp;
              <input
                type="text"
                onChange={handleParticipantId}
                defaultValue={props.connection.participantId}
              />
            </label>
          </> : ""
        }
      </form>
    </div>
  );
}

function Video(props: { title: string, srcObject: MediaStream, }): JSX.Element {
  const refVideo = useRef<HTMLVideoElement>(null);

  const setSrcObj = (srcObj: MediaStream) => {
    if (refVideo.current && srcObj.active) {
      refVideo.current.srcObject = srcObj;
    }
  };

  useEffect(() => {
    setSrcObj(props.srcObject);

    const handler = () => setSrcObj(props.srcObject);
    props.srcObject.addEventListener("active", handler);
    return () => {
      props.srcObject.removeEventListener("active", handler);
    };
  }, [props.srcObject]);

  return (
    <div className={"videoWrapper"}>
      <p>{props.title}{props.srcObject.active ? "" : " [inactive]"}</p>
      <video ref={refVideo} autoPlay playsInline width={300}></video>
    </div>
  );
}
