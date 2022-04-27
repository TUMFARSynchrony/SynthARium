import { Stage, Layer, Text } from "react-konva";
import { useState } from "react";
import Rectangle from "../../atoms/Rectangle/Rectangle";
import { CANVAS_SIZE } from "../../../utils/constants";

function DragAndDrop({
  participantShapes,
  participantGroups,
  setParticipantGroups,
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
        width={CANVAS_SIZE.width}
        height={CANVAS_SIZE.height}
        onMouseDown={checkDeselect}
      >
        <Layer>
          {participantShapes.length > 0 ? (
            participantShapes.map((rect, index) => {
              return (
                <Rectangle
                  key={index}
                  shapeProps={rect}
                  groupProps={participantGroups[index]}
                  isSelected={index === selectedShape}
                  onSelect={() => {
                    setSelectShape(index);
                  }}
                  onChange={(newAttrs) => {
                    const groups = participantGroups.slice();
                    groups[index] = newAttrs;
                    setParticipantGroups(groups);
                  }}
                />
              );
            })
          ) : (
            <Text
              text="There are no participants in this session yet."
              x={CANVAS_SIZE.height / 2}
              y={CANVAS_SIZE.height / 2}
              fontSize={20}
            />
          )}
        </Layer>
      </Stage>
    </>
  );
}

export default DragAndDrop;
