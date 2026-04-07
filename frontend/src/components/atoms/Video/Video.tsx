import React, { useEffect, useRef } from "react";
import { Image, Group, Text } from "react-konva";
import { Participant } from "../../../types";
import Konva from "konva";

type VideoProps = {
  src: MediaProvider;
  participantData: Participant;
  title?: string; // Add a title prop
  shouldMute?: boolean;
};

const Video = ({ src, participantData, title, shouldMute }: VideoProps) => {
  const useVideo = () => {
    const videoRef = useRef(document.createElement("video"));

    useEffect(() => {
      const video = videoRef.current;
      if (!src) {
        return;
      }

      if (shouldMute) {
        video.muted = true;
      }

      video.srcObject = src;
      video.onloadedmetadata = function () {
        video.play();
      };
    }, [src]);

    return videoRef.current;
  };

  const video = useVideo();
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
    <Group>
      <Image
        ref={shapeRef}
        image={video}
        width={participantData.size.width}
        height={participantData.size.height}
        x={participantData.position.x}
        y={participantData.position.y}
      />
      <Text
        text={title}
        fontSize={16}
        fontFamily="Arial"
        fill="black"
        align="center"
        x={participantData.position.x} // Adjust X-coordinate to position the title
        y={participantData.position.y + participantData.size.height} // Adjust Y-coordinate to position below the video
        width={participantData.size.width}
      />
    </Group>
  );
};

export default Video;
