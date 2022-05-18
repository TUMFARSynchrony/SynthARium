import * as React from "react";
import { useRef, useEffect, useState } from "react"

import "./ConnectionTest.css"
import Connection, { ConnectionState } from "../../networking/Connection";


const ConnectionTest = (props: {
  localStream: MediaStream,
  connection: Connection
}) => {
  const connection = props.connection;
  const [connectionState, setConnectionState] = useState(connection.state);

  const streamChangeHandler = (_: MediaStream) => {
    console.log("%cRemote Stream Change Handler", "color:blue");
  }
  const stateChangeHandler = (state: ConnectionState) => {
    console.log(`%cConnection state change Handler: ${state}`, "color:blue");
    setConnectionState(state);
  }

  useEffect(() => {
    connection.remoteStreamChange.on(streamChangeHandler);
    connection.connectionStateChange.on(stateChangeHandler);
    return () => {
      // Remove event handlers when component is deconstructed
      connection.remoteStreamChange.off(streamChangeHandler);
      connection.connectionStateChange.off(stateChangeHandler);
    }
  }, [connection.connectionStateChange, connection.remoteStreamChange]);


  return (
    <>
      <h1>ConnectionTest</h1>
      <p>Connection State:
        <span className={`connectionState ${ConnectionState[connectionState]}`}>{ConnectionState[connectionState]}</span>
      </p>
      <button onClick={() => connection.start(props.localStream)}>Start Connection</button>
      <button onClick={() => connection.stop()}>Stop Connection</button>
      <div className="ownStreams">
        {props.localStream ? <Video title="local stream" srcObject={props.localStream} /> : "Local Stream Loading..."}
        <Video title="remote stream" srcObject={connection.remoteStream} />
      </div>
    </>
  )
}

export default ConnectionTest


function Video(props: {
  title: string
  srcObject: MediaStream,
  className?: string
  style?: React.CSSProperties
}) {
  const refVideo = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (refVideo.current) {
      refVideo.current.srcObject = props.srcObject;
    }
  }, [props.srcObject])

  return (
    <div className={"videoWrapper " + props.className ?? ""} style={props.style}>
      <p>{props.title}</p>
      <video ref={refVideo} autoPlay playsInline height={255} width={300}></video>
    </div>
  )
}
