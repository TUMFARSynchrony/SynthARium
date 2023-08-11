import { useEffect, useRef } from "react";
import { Image } from "react-konva";
import { useUserStream } from "./Streams";
import { Participant } from "../../../types";
import Konva from "konva";

type VideoProps = {
  src: MediaProvider;
  participantData: Participant;
};

const Video = ({ src, participantData }: VideoProps) => {
  const useVideo = (stream: MediaStream | null) => {
    const videoRef = useRef(document.createElement("video"));

    useEffect(() => {
      const video = videoRef.current;
      if (!stream) {
        return;
      }
      video.srcObject = src;
      video.onloadedmetadata = function () {
        video.play();
      };
    }, [stream]);

    return videoRef.current;
  };

  const stream = useUserStream();
  const video = useVideo(stream);
  const shapeRef: React.MutableRefObject<Konva.Image> = useRef();

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
