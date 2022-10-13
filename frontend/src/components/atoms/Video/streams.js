import { useEffect, useState } from "react";

var constraints = { video: true, audio: true };
let userPromise;
function getUserMedia() {
  if (!userPromise) {
    userPromise = navigator.mediaDevices
      .getUserMedia(constraints)
      .catch(function (err) {
        console.log(err.name + ": " + err.message);
      });
  }
  return userPromise;
}

export const useUserStream = () => {
  const [stream, setStream] = useState(null);

  useEffect(() => {
    getUserMedia().then(function (mediaStream) {
      setStream(mediaStream);
    });
  }, []);

  return stream;
};
