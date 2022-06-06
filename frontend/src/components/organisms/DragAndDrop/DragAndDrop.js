import { Stage, Layer, Text } from "react-konva";
import { useState } from "react";
import Rectangle from "../../atoms/Rectangle/Rectangle";
import { CANVAS_SIZE } from "../../../utils/constants";

function DragAndDrop({ participantDimensions, setParticipantDimensions }) {
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
          {participantDimensions.length > 0 ? (
            participantDimensions.map((rect, index) => {
              return (
                <Rectangle
                  key={index}
                  shapeProps={rect.shapes}
                  groupProps={rect.groups}
                  isSelected={index === selectedShape}
                  onSelect={() => {
                    setSelectShape(index);
                  }}
                  onChange={(newAttrs) => {
                    const dimensions = participantDimensions.slice();
                    dimensions[index].groups = newAttrs;
                    setParticipantDimensions(dimensions);
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
