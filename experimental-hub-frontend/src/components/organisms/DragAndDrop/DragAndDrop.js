import "./DragAndDrop.css";
import { Stage, Layer } from "react-konva";
import { useState } from "react";
import Rectangle from "../../atoms/Rectangle/Rectangle";

function DragAndDrop({
  width,
  height,
  rectangles,
  participantGroup,
  setParticipantGroup,
}) {
  const [selectedShape, setSelectShape] = useState(null);

  const checkDeselect = (e) => {
    const clickedOnEmpty = e.target === e.target.getStage();
    if (clickedOnEmpty) {
      setSelectShape(null);
    }
  };

  return (
    <>
      <Stage
        width={width}
        height={height}
        onMouseDown={checkDeselect}
        className="stageCanvas"
        style={{
          backgroundColor: "lightgrey",
          borderRadius: "15px",
          overflow: "hidden",
        }}
      >
        <Layer>
          {rectangles.map((rect, index) => {
            return (
              <Rectangle
                shapeProps={rect}
                groupProps={participantGroup[index]}
                isSelected={index === selectedShape}
                onSelect={() => {
                  setSelectShape(index);
                }}
                onChange={(newAttrs) => {
                  const groups = participantGroup.slice();
                  groups[index] = newAttrs;
                  setParticipantGroup(groups);
                }}
              />
            );
          })}
        </Layer>
      </Stage>
    </>
  );
}

export default DragAndDrop;
