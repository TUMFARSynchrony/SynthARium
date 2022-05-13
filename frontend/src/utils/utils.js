export const getRandomColor = () => {
  let letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};

export const filterListByIndex = (list, index) => {
  let filteredList = list.filter((obj, i) => {
    return i !== index;
  });

  return filteredList;
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
    height: maxY - minY,
  };
};

export const getLocalStream = async () => {
  // TODO: allow the user to select a specific camera / audio device?
  const constraints = {
    video: true,
    audio: true,
  };
  try {
    return await navigator.mediaDevices.getUserMedia(constraints);
  } catch (error) {
    console.error("Error opening video camera.", error);
  }
};

export const getShapesFromParticipants = (participants) => {
  const shapesArray = [];
  let groupArray = [];

  participants.forEach((participant, _) => {
    shapesArray.push({
      x: 0,
      y: 0,
      fill: getRandomColor(),
      first_name: participant.first_name,
      last_name: participant.last_name,
    });
    groupArray.push({
      x: participant.position.x,
      y: participant.position.y,
      width: participant.size.width,
      height: participant.size.height,
    });
  });

  return { shapesArray: shapesArray, groupArray: groupArray };
};
