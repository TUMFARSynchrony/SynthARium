import * as React from "react";
import { useRef, useEffect, useState } from "react";

import "./ConnectionTest.css";
import Connection, { ConnectionState } from "../../networking/Connection";


const ConnectionTest = (props: {
  localStream?: MediaStream,
  connection: Connection;
}) => {
  const connection = props.connection;
  const [connectionState, setConnectionState] = useState(connection.state);

  const streamChangeHandler = (_: MediaStream) => {
    console.log("%cRemote Stream Change Handler", "color:blue");
  };
  const stateChangeHandler = (state: ConnectionState) => {
    console.log(`%cConnection state change Handler: ${state}`, "color:blue");
    setConnectionState(state);
  };

  useEffect(() => {
    connection.remoteStreamChange.on(streamChangeHandler);
    connection.connectionStateChange.on(stateChangeHandler);
    return () => {
      // Remove event handlers when component is deconstructed
      connection.remoteStreamChange.off(streamChangeHandler);
      connection.connectionStateChange.off(stateChangeHandler);
    };
  }, [connection.connectionStateChange, connection.remoteStreamChange]);


  return (
    <div className="ConnectionTestPageWrapper">
      <h1>ConnectionTest</h1>
      <p>Connection State:
        <span className={`connectionState ${ConnectionState[connectionState]}`}>{ConnectionState[connectionState]}</span>
      </p>
      <button onClick={() => connection.start(props.localStream)} disabled={connection.state !== ConnectionState.NotStarted}>Start Connection</button>
      <button onClick={() => connection.stop()} disabled={connection.state !== ConnectionState.Connected}>Stop Connection</button>
      <div className="ownStreams">
        <Video title="local stream" srcObject={props.localStream ?? new MediaStream()} />
        <Video title="remote stream" srcObject={connection.remoteStream} />
      </div>
      <ApiTests connection={connection} />
    </div>
  );
};

export default ConnectionTest;


function ApiTests(props: { connection: Connection, }): JSX.Element {
  const [responses, setResponses] = useState<{ endpoint: string, data: string; }[]>([]);
  const [highlightedResponse, setHighlightedResponse] = useState(0);
  useEffect(() => {
    const sessionListHandler = (data: any) => {
      setResponses([...responses, { endpoint: "SESSION_LIST", data: data }]);
      setHighlightedResponse(0);
    };

    props.connection.api.on("SESSION_LIST", sessionListHandler);

    return () => {
      props.connection.api.off("SESSION_LIST", sessionListHandler);
    };
  }, [props.connection.api, responses]);

  return (
    <>
      <div className="requestButtons">
        <button onClick={() => props.connection.sendMessage("GET_SESSION_LIST", {})}>
          Request Sessions
        </button>
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


function Video(props: {
  title: string;
  srcObject: MediaStream,
  className?: string;
  style?: React.CSSProperties;
}): JSX.Element {
  const refVideo = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (refVideo.current) {
      refVideo.current.srcObject = props.srcObject;
    }
  }, [props.srcObject]);

  return (
    <div className={"videoWrapper " + props.className ?? ""} style={props.style}>
      <p>{props.title}</p>
      <video ref={refVideo} autoPlay playsInline height={255} width={300}></video>
    </div>
  );
}
