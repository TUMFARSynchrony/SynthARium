import * as React from "react";
import { useRef, useEffect, useState } from "react";

import "./ConnectionLatencyTest.css";
import Connection from "../../networking/Connection";
import ConnectionState from "../../networking/ConnectionState";
import { getLocalStream } from "../../utils/utils";
import jsQR from "jsqr";

var QRCode = require('qrcode');

/**
 * Test page for testing the {@link Connection} & api.
 */
const ConnectionLatencyTest = (props: {
  localStream?: MediaStream,
  setLocalStream: (localStream: MediaStream) => void,
  connection: Connection,
  setConnection: (connection: Connection) => void,
}) => {
  const connection = props.connection;
  const [connectionState, setConnectionState] = useState(connection.state);
  const [canvasStream, setCanvasStream] = useState(null);
  const [data, setData] = useState([]);
  const canvasQRRef = useRef<HTMLCanvasElement>(null);
  const canvasLocalRef = useRef<HTMLCanvasElement>(null);
  const canvasRemoteRef = useRef<HTMLCanvasElement>(null);
  const latencyRef = useRef<HTMLSpanElement>(null);
  const stopped = useRef(false);

  /** Handle `connectionStateChange` event of {@link Connection}. */
  const stateChangeHandler = async (state: ConnectionState) => {
    console.log(`%cConnection state change Handler: ${ConnectionState[state]}`, "color:blue");
    setConnectionState(state);
    if (state === ConnectionState.CLOSED || state === ConnectionState.FAILED) {
      stopped.current = true;
      console.group("data");
      console.log(data);
      console.groupEnd();
    }
  };

  const streamChangeHandler = async (remoteStream: MediaStream) => {
    console.log("%cRemote Stream Change Handler", "color:blue");
    updateRemoteCanvas();
  };

  // Register Connection event handlers 
  useEffect(() => {
    connection.on("remoteStreamChange", streamChangeHandler);
    connection.on("connectionStateChange", stateChangeHandler);
    return () => {
      // Remove event handlers when component is deconstructed
      connection.off("remoteStreamChange", streamChangeHandler);
      connection.off("connectionStateChange", stateChangeHandler);
    };
  }, [connection]);

  useEffect(() => {
    updateLocalCanvas();
  }, []);

  /** Set canvasStream state */
  useEffect(() => {
    if (canvasLocalRef.current && !canvasStream) {
      console.log("setCanvasStream(...)");
      setCanvasStream(canvasLocalRef.current.captureStream(30));
    }
  }, [canvasLocalRef, canvasStream]);

  /** Update local stream when canvasStream state changes */
  useEffect(() => {
    console.log("props.setLocalStream(canvasStream);");
    props.setLocalStream(canvasStream);
  }, [canvasStream, props]);

  const getLatency = () => {
    const localTimestamp = window.performance.now(); // parseQRCode(canvasLocalRef.current);
    const remoteTimestamp = parseQRCode(canvasRemoteRef.current);
    // console.log("checkLatency - remoteTimestamp - runtime: ", window.performance.now() - localTimestamp, "ms");
    const diff = localTimestamp - remoteTimestamp;
    if (latencyRef.current) {
      latencyRef.current.innerText = `${diff.toFixed(4)}`;
    }
    // console.log("Time diff:", diff, "ms");
    // console.log("checkLatency runtime: ", window.performance.now() - localTimestamp, "ms");
    return diff;
  };

  const makeLogEntry = () => {
    const latency = getLatency();
    const entry = {
      latency: latency,
      num: data.length
    };
    console.log("Store entry:", entry);
    data.push(entry);
  };

  const parseQRCode = (canvas: HTMLCanvasElement) => {
    const imageData = canvas.getContext("2d").getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(imageData.data, imageData.width, imageData.height, {
      inversionAttempts: "dontInvert",
    });
    const timestamp = parseFloat(code.data);
    return timestamp;
  };

  const updateRemoteCanvas = () => {
    const context = canvasRemoteRef.current.getContext("2d");
    const track = connection.remoteStream.getVideoTracks()[0];
    const processor = new window.MediaStreamTrackProcessor(track);
    const reader = processor.readable.getReader();

    const readFrame = async () => {
      const { done, value } = await reader.read();

      // Resize canvas if necessary
      if (canvasRemoteRef.current.height !== value.displayHeight) {
        canvasRemoteRef.current.height = value.displayHeight;
      }
      if (canvasRemoteRef.current.width !== value.displayWidth) {
        canvasRemoteRef.current.width = value.displayWidth;
      }

      // context.clearRect(0, 0, canvasRemoteRef.current.width, canvasRemoteRef.current.height);
      context.drawImage(value, 0, 0);

      // context.beginPath();
      // context.lineWidth = 2;
      // context.strokeStyle = "red";
      // context.rect(0, 0, 200, 200);
      // context.stroke();

      value.close();

      // Calculate latency for current frame
      try {
        makeLogEntry();
      } catch (_) { }

      if (!done && !stopped.current) {
        readFrame();
      }
    };
    readFrame();
  };

  const updateLocalCanvas = async () => {
    const context = canvasLocalRef.current.getContext("2d");
    const track = (await getLocalStream()).getVideoTracks()[0];
    const processor = new window.MediaStreamTrackProcessor(track);
    const reader = processor.readable.getReader();

    const readFrame = async () => {
      const { done, value } = await reader.read();

      // Resize canvas if necessary
      if (canvasLocalRef.current.height !== value.displayHeight) {
        canvasLocalRef.current.height = value.displayHeight;
      }
      if (canvasLocalRef.current.width !== value.displayWidth) {
        canvasLocalRef.current.width = value.displayWidth;
      }

      // Put current VideoFrame on canvas
      // context.clearRect(0, 0, canvasLocalRef.current.width, canvasLocalRef.current.height);
      context.drawImage(value, 0, 0);

      // Put QRcode on canvas
      const timestamp = window.performance.now();
      QRCode.toCanvas(canvasQRRef.current, `${timestamp}`, { width: 200 });

      context.drawImage(canvasQRRef.current, 0, 0);
      context.font = "16px Arial";
      context.fillText(timestamp.toFixed(10), 20, 20);

      value.close(); // close the VideoFrame when we're done with it
      if (!done && !stopped.current) {
        readFrame();
      }
    };
    readFrame();
  };

  /** Get the title displayed in a {@link Video} element for the remote stream of this client. */
  const getRemoteStreamTitle = () => {
    if (connection.participantSummary) {
      if (connection.participantSummary instanceof Object) {
        return `remote stream (${connection.participantSummary.first_name} ${connection.participantSummary.last_name})`;
      }
      return `remote stream: ${connection.participantSummary}`;
    }
    return "remote stream";
  };



  if (!window.MediaStreamTrackProcessor) {
    return "This Page requires the MediaStreamTrackProcessor. See: https://developer.mozilla.org/en-US/docs/Web/API/MediaStreamTrackProcessor#browser_compatibility";
  }

  return (
    <div className="ConnectionTestPageWrapper">
      <h1>Connection Latency Test</h1>
      <p>Connection State:
        <span className={`connectionState ${ConnectionState[connectionState]}`}>{ConnectionState[connectionState]}</span>
      </p>
      <button onClick={() => connection.start(props.localStream)} disabled={connection.state !== ConnectionState.NEW}>Start Connection</button>
      <button onClick={() => connection.stop()} disabled={connection.state !== ConnectionState.CONNECTED}>Stop Connection</button>
      <button onClick={() => console.log(connection)}>Log Connection</button>

      <canvas ref={canvasQRRef} hidden />
      <div className="canvasWrapper">
        <canvas ref={canvasLocalRef} width={640} height={480} />
        <canvas ref={canvasRemoteRef} width={640} height={480} />
      </div>

      <p>Latency: <span ref={latencyRef}>unknown</span> ms</p>

      {/* <div className="canvasWrapper">
        <Video title="local stream" srcObject={props.localStream ?? new MediaStream()} ignoreAudio />
        <Video title={getRemoteStreamTitle()} srcObject={connection.remoteStream} ignoreAudio />
      </div> */}
    </div>
  );
};


export default ConnectionLatencyTest;
