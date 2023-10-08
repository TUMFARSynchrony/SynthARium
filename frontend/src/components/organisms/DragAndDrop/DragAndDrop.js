import { useState } from "react";
import { Layer, Stage, Text } from "react-konva";
import { useAppDispatch } from "../../../redux/hooks";
import { changeParticipantDimensions } from "../../../redux/slices/openSessionSlice";
import Rectangle from "../../atoms/Rectangle/Rectangle";
import useMeasure from "react-use-measure";

function DragAndDrop({ participantDimensions, setParticipantDimensions }) {
  const [selectedShape, setSelectShape] = useState(null);

  const dispatch = useAppDispatch();
  const [ref, bounds] = useMeasure();

  const checkDeselect = (e) => {
    const clickedOnEmpty = e.target === e.target.getStage();
    if (clickedOnEmpty) {
      setSelectShape(null);
    }
  };
  return (
    <div className="w-full h-full" ref={ref}>
      <Stage
        className="flex items-center justify-center"
        width={bounds.width}
        height={bounds.height}
        onMouseDown={checkDeselect}
      >
        <Layer>
          {participantDimensions.length > 0 ? (
            participantDimensions.map((rect, index) => {
              return (
                <Rectangle
                  key={index}
                  bounds={bounds}
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
            <div className="w-full h-full">
              <Text
                text="There are no participants in this session yet."
                fontSize={20}
                align={"center"}
                verticalAlign={"middle"}
                width={bounds.width}
                height={bounds.height}
              />
            </div>
          )}
        </Layer>
      </Stage>
    </div>
  );
}

export default DragAndDrop;
