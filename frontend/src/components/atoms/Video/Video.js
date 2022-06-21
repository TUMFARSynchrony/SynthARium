import { useEffect, useRef, useState } from "react";

function Video({ title, srcObject, ignoreAudio }) {
  const refVideo = useRef(null);
  const [info, setInfo] = useState("");

  useEffect(() => {
    const setSrcObj = (srcObj) => {
      if (refVideo.current && srcObj.active) {
        if (ignoreAudio) {
          refVideo.current.srcObject = new MediaStream(srcObj.getVideoTracks());
        } else {
          refVideo.current.srcObject = srcObj;
        }
      }
    };

    setSrcObj(srcObject);

    const handler = () => setSrcObj(srcObject);
    srcObject.addEventListener("active", handler);
    return () => {
      srcObject.removeEventListener("active", handler);
    };
  }, [ignoreAudio, srcObject]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (refVideo.current?.srcObject === null) return;

      const videoTracks = srcObject.getVideoTracks();
      if (videoTracks.length === 0) return;

      const fps = videoTracks[0].getSettings().frameRate;
      if (!fps) {
        if (info !== "") {
          setInfo("");
        }
        return;
      }
      const newInfo = `${fps.toFixed(3)} fps`;
      if (info !== newInfo) {
        setInfo(newInfo);
      }
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }, [info, srcObject]);

  return (
    <div className={"videoWrapper"}>
      <p>
        {title}
        {srcObject.active ? "" : " [inactive]"}
      </p>
      <video ref={refVideo} autoPlay playsInline width={300}></video>
      <div className="fpsCounter">{info}</div>
    </div>
  );
}

export default Video;
