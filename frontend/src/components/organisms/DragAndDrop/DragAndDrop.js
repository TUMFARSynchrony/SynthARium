import { useState } from "react";
import { Layer, Stage, Text } from "react-konva";
import { useAppDispatch } from "../../../redux/hooks";
import { changeParticipantDimensions } from "../../../redux/slices/openSessionSlice";
import { CANVAS_SIZE } from "../../../utils/constants";
import Rectangle from "../../atoms/Rectangle/Rectangle";

function DragAndDrop({
  participantDimensions,
  setParticipantDimensions,
  addDimensionToHistory
}) {
  const [selectedShape, setSelectShape] = useState(null);
  const dispatch = useAppDispatch();

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
                    addDimensionToHistory();
                    const dimensions = participantDimensions.slice();
                    dimensions[index].groups = newAttrs;
                    setParticipantDimensions(dimensions);

                    dispatch(
                      changeParticipantDimensions({
                        index: index,
                        position: {
                          x: newAttrs.x,
                          y: newAttrs.y,
                          z: 0
                        },
                        size: {
                          width: newAttrs.width,
                          height: newAttrs.height
                        }
                      })
                    );
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
