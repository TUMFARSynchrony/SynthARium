import { useEffect, useState } from "react";

const constraints = { video: true, audio: true };
let userPromise: Promise<MediaStream> | null;
function getUserMedia() {
  if (!userPromise) {
    userPromise = navigator.mediaDevices.getUserMedia(constraints).catch(function (err) {
      console.log(err.name + ": " + err.message);
      throw err;
    });
  }
  return userPromise;
}

export const useUserStream = (): MediaStream | null => {
  const [stream, setStream] = useState<MediaStream | null>(null);

  useEffect(() => {
    getUserMedia().then(function (mediaStream: MediaStream) {
      setStream(mediaStream);
    });
  }, []);

  return stream;
};
