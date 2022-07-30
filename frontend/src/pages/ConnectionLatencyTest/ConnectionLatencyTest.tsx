import * as React from "react";
import { useRef, useEffect, useState } from "react";

import "./ConnectionLatencyTest.css";
import Connection from "../../networking/Connection";
import ConnectionState from "../../networking/ConnectionState";
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
  const defaultConfig = {
    participantId: connection.participantId ?? "",
    sessionId: connection.sessionId ?? "",
    fps: 30,
    background: true,
    width: 640,
    height: 480,
    qrCodeSize: 200
  };
  const [connectionState, setConnectionState] = useState(connection.state);
  const [startedRemoteStreamLoop, setStartedRemoteStreamLoop] = useState(false);
  const [data, setData] = useState([]);
  const [config, setConfig] = useState<TestConfigObj>(defaultConfig);
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

  const streamChangeHandler = async (_: MediaStream) => {
    console.log("%cRemote Stream Change Handler", "color:blue");
    // Start update loop for remote canvas when remote stream is received;
    if (!startedRemoteStreamLoop) {
      setStartedRemoteStreamLoop(true);
      updateRemoteCanvas();
    }
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
  }, [connection, config, startedRemoteStreamLoop]);

  /** Start the connection experiment */
  const start = async () => {
    console.log("Start Test. Config:", config);

    // Setup local canvas stream
    const localCanvasStream = canvasLocalRef.current.captureStream();
    props.setLocalStream(localCanvasStream); // Note: setLocalStream is not executed / updated right away. See useState react docs 

    // Start update loop for local stream canvas
    try {
      await updateLocalCanvas();
    } catch (error) {
      console.warn("Aborting start");
      return;
    }

    // Start connection
    connection.start(localCanvasStream);
  };

  /** Stop the connection experiment */
  const stop = async () => {
    connection.stop();

    setTimeout(() => {
      evaluate();
      if (latencyRef.current) {
        latencyRef.current.innerText = "-";
      }
    }, 500);
  };

  /** Small, in-browser evaluation */
  const evaluate = () => {
    const avg = (arr: number[]) => arr.reduce((a, b) => a + b, 0) / arr.length;
    const median = (arr: number[]) => {
      const sorted = arr.sort((a, b) => a - b);
      const half = Math.floor(arr.length / 2);
      if (arr.length % 2) {
        return sorted[half];
      }
      return (sorted[half - 1] + sorted[half]) / 2;
    };

    const durationTotalMs = (data[data.length - 1].timestamp - data[0].timestamp);
    const durationSec = Math.floor((durationTotalMs / 1000) % 60);
    const durationMin = Math.floor((durationTotalMs / 1000) / 60);
    const durationMs = durationTotalMs % 1000;

    const invalidLatencyDataPoints = data.map(entry => entry.latency).filter(l => l === -1).length;
    const invalidLatencyDataPointsPercent = Math.round((invalidLatencyDataPoints / data.length) * 100);
    const latencyArr: number[] = data.map(entry => entry.latency).filter(l => l !== -1);
    const avgLatency = avg(latencyArr);
    const medianLatency = median(latencyArr);

    const latencyMethodArr: number[] = data.map(entry => entry.latencyMethodRuntime);
    const avgLatencyMethod = avg(latencyMethodArr);
    const medianLatencyMethod = median(latencyMethodArr);

    const latencyFilteredMethodArr: number[] = data.filter(e => {
      return e.dimensions.width === config.width && e.dimensions.height === config.height;
    }).map(entry => entry.latencyMethodRuntime);
    const avgFilteredLatencyMethod = avg(latencyFilteredMethodArr);
    const medianFilteredLatencyMethod = median(latencyFilteredMethodArr);

    const fpsArr: number[] = data.map(entry => entry.fps);
    const avgFps = avg(fpsArr);
    const medianFps = median(fpsArr);

    console.group("Evaluation");
    console.log(`Recorded Data Points: ${data.length}`);
    console.log(`Duration: ${durationMin}m, ${durationSec}s, ${durationMs}ms`);
    console.log(`Invalid Latency Data Points: ${invalidLatencyDataPoints} (${invalidLatencyDataPointsPercent}%)`);
    console.log("Average Latency:", avgLatency, "ms");
    console.log("Median Latency:", medianLatency, "ms");
    console.log("Average FPS:", avgFps);
    console.log("Median FPS:", medianFps);
    console.log("Average Latency Method Runtime:", avgLatencyMethod, "ms");
    console.log("Median Latency Method Runtime:", medianLatencyMethod, "ms");
    console.log("Average Filtered (Full-Resolution only) Latency Method Runtime:", avgFilteredLatencyMethod, "ms");
    console.log("Median Filtered (Full-Resolution only) Latency Method Runtime:", medianFilteredLatencyMethod, "ms");
    console.groupEnd();
  };

  /** Measure latency between the remote stream QR-code and current time. */
  const getLatency = () => {
    const localTimestamp = window.performance.now();
    const remoteTimestamp = parseQRCode(canvasRemoteRef.current);
    const diff = localTimestamp - remoteTimestamp;
    if (latencyRef.current) {
      latencyRef.current.innerText = `${diff.toFixed(4)}`;
    }
    return [diff, localTimestamp];
  };

  /** Log a data point in `data`. */
  const makeLogEntry = async () => {
    let latency: number, timestamp: number;
    const startTime = window.performance.now();
    try {
      [latency, timestamp] = getLatency();
    } catch (error) {
      latency = -1;
      timestamp = window.performance.now();
    }
    const latencyMethodRuntime = window.performance.now() - startTime;

    const remoteStreamSettings = connection.remoteStream.getVideoTracks()[0].getSettings();
    const entry = {
      latency: latency,
      fps: remoteStreamSettings.frameRate,
      timestamp: timestamp,
      num: data.length,
      latencyMethodRuntime: latencyMethodRuntime,
      dimensions: {
        width: remoteStreamSettings.width,
        height: remoteStreamSettings.height
      }
      // connectionStats: await connection.getStats()
    };
    console.log(entry);
    data.push(entry);
  };

  /** Parse the QR code in `canvas`. */
  const parseQRCode = (canvas: HTMLCanvasElement) => {
    // Calculate position of QR code, in case transmitted image is scaled down.
    const qrCodeWidth = Math.floor((canvas.width / config.width) * config.qrCodeSize);
    const qrCodeHeight = Math.floor((canvas.height / config.height) * config.qrCodeSize);
    const context = canvas.getContext("2d");

    // Get image data for expected position of QR code. Getting only part of the image saves a lot of time in `jsQR` (optimization).
    const imageData = context.getImageData(0, 0, qrCodeWidth, qrCodeHeight);

    // Uncomment to draw a rectangle around the expected position of the QR code (debugging)
    /*
    console.log(qrCodeWidth, qrCodeHeight);
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = "red";
    context.rect(0, 0, qrCodeWidth, qrCodeHeight);
    context.stroke();
    */

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

    const readRemoteFrame = async () => {
      const { done, value } = await reader.read();
      if (!value) {
        return;
      }
      // Resize canvas if necessary
      if (canvasRemoteRef.current.height !== value.displayHeight) {
        canvasRemoteRef.current.height = value.displayHeight;
      }
      if (canvasRemoteRef.current.width !== value.displayWidth) {
        canvasRemoteRef.current.width = value.displayWidth;
      }

      // context.clearRect(0, 0, canvasRemoteRef.current.width, canvasRemoteRef.current.height);
      context.drawImage(value, 0, 0);
      value.close();

      // Calculate latency for current frame
      await makeLogEntry();

      if (!done && !stopped.current) {
        readRemoteFrame();
      }
    };
    readRemoteFrame();
  };

  /** Get a video only local stream according to config */
  const getLocalStream = async () => {
    const constraints = {
      video: {
        width: { exact: config.width },
        height: { exact: config.height },
        frameRate: { exact: config.fps },
      },
      audio: false,
    };
    try {
      return await navigator.mediaDevices.getUserMedia(constraints);
    } catch (error) {
      console.error("Failed to open video camera. The constraints set in the config may be not possible.", error);
    }
  };

  const updateLocalCanvas = async () => {
    const context = canvasLocalRef.current.getContext("2d");
    const track = (await getLocalStream())?.getVideoTracks()[0];
    if (!track) throw new Error("Failed to get local stream");
    const processor = new window.MediaStreamTrackProcessor(track);
    const reader = processor.readable.getReader();

    const readLocalFrame = async () => {
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
      if (config.background) {
        context.drawImage(value, 0, 0);
      }

      // Put QRcode on canvas
      const timestamp = window.performance.now();
      QRCode.toCanvas(canvasQRRef.current, `${timestamp}`, { width: config.qrCodeSize });

      context.drawImage(canvasQRRef.current, 0, 0);
      // context.font = "16px Arial";
      // context.fillText(timestamp.toFixed(10), 20, 20);

      value.close(); // close the VideoFrame when we're done with it
      if (!done && !stopped.current) {
        readLocalFrame();
      }
    };
    readLocalFrame();
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


  // Get the main action button. Start, Stop or Reload button.
  let mainActionBtn = <></>;
  switch (connectionState) {
    case ConnectionState.NEW:
      mainActionBtn = <button onClick={start}>Start Experiment</button>;
      break;
    case ConnectionState.CONNECTING:
    case ConnectionState.CONNECTED:
      mainActionBtn = <button onClick={stop} disabled={connection.state !== ConnectionState.CONNECTED}>Stop Experiment</button>;
      break;
    default:
      mainActionBtn = <button onClick={() => window.location.reload()}>Reload Page</button>;;
      break;
  }

  return (
    <div className="ConnectionTestPageWrapper">
      <h1>Connection Latency Test</h1>
      <p>Connection State:
        <span className={`connectionState ${ConnectionState[connectionState]}`}>{ConnectionState[connectionState]}</span>
      </p>
      <TestConfig
        start={start}
        config={config}
        defaultConfig={defaultConfig}
        setConfig={setConfig}
        disabled={connectionState !== ConnectionState.NEW}
      />
      <div className="container controls">
        {mainActionBtn}
      </div>

      <button onClick={() => console.log(connection)}>Log Connection</button>

      <canvas ref={canvasQRRef} hidden />
      <div className="canvasWrapper">
        <div>
          <label>Local Stream</label>
          <canvas ref={canvasLocalRef} />
        </div>
        <div>
          <label>Remote Stream</label>
          <canvas ref={canvasRemoteRef} />
        </div>
      </div>

      <p>Latency: <span ref={latencyRef}>unknown</span> ms</p>

      {/* <div className="canvasWrapper">
        <Video title="local stream" srcObject={props.localStream ?? new MediaStream()} ignoreAudio />
        <Video title={getRemoteStreamTitle()} srcObject={connection.remoteStream} ignoreAudio />
      </div> */}
    </div >
  );
};


export default ConnectionLatencyTest;

type TestConfigObj = {
  participantId: string,
  sessionId: string,
  fps: number,
  background: boolean,
  width: number,
  height: number,
  qrCodeSize: number,
};

function TestConfig(props: {
  disabled?: boolean,
  config: TestConfigObj,
  defaultConfig: TestConfigObj,
  setConfig: (config: TestConfigObj) => void,
  start: () => void,
}) {
  const disabled = props.disabled ?? false;
  const config = props.config;

  const handleSubmit = (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    props.start();
  };

  const handleChange = (key: keyof TestConfigObj, value: string | number | boolean) => {
    const newConfig = { ...props.config };
    // @ts-ignore
    newConfig[key] = value;
    props.setConfig(newConfig);
    console.log("set", key, "to", value, newConfig);
  };

  // TODO hotkeys & reset btn

  return (
    <form onSubmit={handleSubmit} className="testConfig container">
      <Input disabled={disabled} label="Session ID" defaultValue={config.sessionId} setValue={(v) => handleChange("sessionId", v)} />
      <Input disabled={disabled} label="Participant ID" defaultValue={config.participantId} setValue={(v) => handleChange("participantId", v)} />
      <Input disabled={disabled} label="Frames per Second" type="number" defaultValue={config.fps} setValue={(v) => handleChange("fps", v)} />
      <Input disabled={disabled} label="Background Video" type="checkbox" defaultChecked={config.background} setValue={(v) => handleChange("background", v)} />
      <Input disabled={disabled} label="Video width (px)" type="number" defaultValue={config.width} setValue={(v) => handleChange("width", v)} />
      <Input disabled={disabled} label="Video height (px)" type="number" defaultValue={config.height} setValue={(v) => handleChange("height", v)} />
      <Input disabled={disabled} label="QR Code Size (px)" type="number" defaultValue={config.qrCodeSize} setValue={(v) => handleChange("qrCodeSize", v)} />
      <button type="submit" disabled={disabled} hidden />
    </form>
  );
}

function Input(props: {
  disabled: boolean,
  label: string,
  type?: string,
  defaultValue?: string | number,
  defaultChecked?: boolean,
  setValue: (value: string | number | boolean) => void;
}) {
  const handleChange = (e: any) => {
    let { value } = e.target;
    // Parse value to correct type
    if (props.type === "number") {
      value = parseInt(value) || 0;
    } else if (props.type === "checkbox") {
      value = e.target.checked;
    }
    props.setValue(value);
  };
  return (
    <>
      <label>{props.label}:</label>
      <input
        disabled={props.disabled}
        type={props.type ?? "text"}
        defaultValue={props.defaultValue}
        defaultChecked={props.defaultChecked}
        onChange={handleChange}
      />
    </>
  );
}
