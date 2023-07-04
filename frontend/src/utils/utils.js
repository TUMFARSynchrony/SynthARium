import { useContext, useEffect } from "react";
import { UNSAFE_NavigationContext } from "react-router-dom";

export const getRandomColor = () => {
  let letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};

export const filterListByIndex = (list, index) => {
  let filteredList = list.filter((_, i) => {
    return i !== index;
  });

  return filteredList;
};

export const filterListById = (list, id) => {
  let filteredList = list.filter((obj) => {
    return obj.id !== id;
  });

  return filteredList;
};

export const getSessionById = (id, list) => {
  let session = list.filter((obj) => {
    return obj.id === id;
  });

  return session;
};

export const integerToDateTime = (integerDate) => {
  return new Date(integerDate).toLocaleString();
};

export const getTotalBox = (boxes) => {
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;

  boxes.forEach((box) => {
    minX = Math.min(minX, box.x);
    minY = Math.min(minY, box.y);
    maxX = Math.max(maxX, box.x + box.width);
    maxY = Math.max(maxY, box.y + box.height);
  });
  return {
    x: minX,
    y: minY,
    width: maxX - minX,
    height: maxY - minY
  };
};

export const getLocalStream = async () => {
  // TODO: allow the user to select a specific camera / audio device?
  const constraints = {
    video: true,
    audio: true
  };
  try {
    return await navigator.mediaDevices.getUserMedia(constraints);
  } catch (error) {
    console.error("Error opening video camera.", error);
  }
};

export const getParticipantDimensions = (participants) => {
  let dimensions = [];

  participants.forEach((participant) => {
    dimensions.push({
      shapes: {
        x: 0,
        y: 0,
        fill: getRandomColor(),
        first_name: participant.first_name,
        last_name: participant.last_name
      },
      groups: {
        x: participant.position.x,
        y: participant.position.y,
        width: participant.size.width,
        height: participant.size.height
      }
    });
  });

  return dimensions;
};

/*
 * Correct format: YYYY-MM-DDTHH:MM, e.g. 2018-06-07T00:00
 * date - Date input in form of an integer
 */
export const formatDate = (date) => {
  date = new Date(date);

  var dd = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
  var mm =
    date.getMonth() + 1 < 10
      ? "0" + (date.getMonth() + 1)
      : date.getMonth() + 1;
  var yyyy = date.getFullYear();
  var mins =
    date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
  var hh = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();

  return `${yyyy}-${mm}-${dd}T${hh}:${mins}`;
};

export const sortArray = (array) => {
  array.sort(function (a, b) {
    return new Date(a.date) - new Date(b.date);
  });

  return array;
};

export const getPastAndFutureSessions = (sessionsList) => {
  let pastSessions = [];
  let futureSessions = [];

  let today = new Date().getTime();

  sessionsList.forEach((session) => {
    // Sessions in the past are in the past and cannot be started.
    // end_time needs to be > 0 for a session to be past as well.
    if (session.date < today || session.end_time > 0) {
      pastSessions.push(session);
    } else {
      futureSessions.push(session);
    }
  });

  return { pastSession: pastSessions, futureSession: futureSessions };
};

// Required: "title", "description", "date", "time_limit"
export const checkValidSession = (sessionData) => {
  return (
    sessionData.title !== "" &&
    sessionData.description !== "" &&
    // TO DO : remove session time_limit from the check and session.json, as it is no longer needed.
    // Because the session is not going to end after the session duration has passed.
    // sessionData.time_limit !== 0 &&
    sessionData.date !== 0
  );
};

export const isFutureSession = (sessionData) => {
  let today = new Date().getTime();

  return today < sessionData.date;
};

export const useBackListener = (callback) => {
  const navigator = useContext(UNSAFE_NavigationContext).navigator;

  useEffect(() => {
    const listener = ({ location, action }) => {
      if (action === "POP") {
        callback({ location, action });
      }
    };

    const unlisten = navigator.listen(listener);
    return unlisten;
  }, [callback, navigator]);
};

export const getVideoTitle = (peer, index) => {
  if (peer) {
    return `${peer.first_name} ${peer.last_name}`;
  }
  return `Peer stream ${index + 1}`;
};

export const getParticipantById = (participantId, sessionData) => {
  let participants = sessionData.participants;

  return getSessionById(participantId, participants)[0];
};

// Generating the dynamic participant invite link based on the host domain.
export const getParticipantInviteLink = (participantId, sessionId) => {
  return `${window.location.origin}/lobby?participantId=${participantId}&sessionId=${sessionId}`;
};
