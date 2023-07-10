/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect, useMemo, useRef } from "react";
import { Image } from "react-konva";
import { useUserStream } from "./streams";

const Video = ({ src, participantData }) => {
  const useVideo = (stream) => {
    const video = useMemo(() => {
      return document.createElement("video");
    });

    useEffect(() => {
      if (!stream) {
        return;
      }
      video.srcObject = src;
      video.onloadedmetadata = function () {
        video.play();
      };
    }, [stream, video]);

    return video;
  };

  const stream = useUserStream();
  const video = useVideo(stream);
  const shapeRef = useRef();

  useEffect(() => {
    const interval = setInterval(() => {
      shapeRef?.current.getLayer()?.batchDraw();
    }, 1000 / 50);

    return () => {
      clearInterval(interval);
    };
  }, [video]);

  return (
    <Image
      ref={shapeRef}
      image={video}
      width={participantData.size.width}
      height={participantData.size.height}
      x={participantData.position.x}
      y={participantData.position.y}
    />
  );
};

export default Video;
