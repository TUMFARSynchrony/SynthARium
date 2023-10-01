import { useRef, useState, useEffect } from "react";
import { Layer, Stage, Text } from "react-konva";
import { useAppDispatch } from "../../../redux/hooks";
import { changeParticipantDimensions } from "../../../redux/slices/openSessionSlice";
import Rectangle from "../../atoms/Rectangle/Rectangle";

function DragAndDrop({ participantDimensions, setParticipantDimensions }) {
  const [selectedShape, setSelectShape] = useState(null);
  const divRef = useRef(null);
  const [dimensions, setDimensions] = useState({
    width: 0,
    height: 0
  });
  const dispatch = useAppDispatch();

  // We cant set the h & w on Stage to 100% it only takes px values so we have to
  // find the parent container's w and h and then manually set those !
  useEffect(() => {
    if (divRef.current?.offsetHeight && divRef.current?.offsetWidth) {
      setDimensions({
        width: divRef.current.offsetWidth,
        height: divRef.current.offsetHeight
      });
    }
  }, []);

  const checkDeselect = (e) => {
    const clickedOnEmpty = e.target === e.target.getStage();
    if (clickedOnEmpty) {
      setSelectShape(null);
    }
  };

  return (
    <div className="w-full h-full" ref={divRef}>
      <Stage
        className="flex items-center justify-center"
        width={dimensions.width}
        height={dimensions.height}
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
                width={dimensions.width}
                height={dimensions.height}
              />
            </div>
          )}
        </Layer>
      </Stage>
    </div>
  );
}

export default DragAndDrop;
