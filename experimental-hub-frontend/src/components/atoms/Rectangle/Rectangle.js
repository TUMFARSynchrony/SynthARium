import { useEffect, useRef } from "react";
import { Group, Rect, Text, Transformer } from "react-konva";
import { CANVAS_SIZE } from "../../../utils/constants";

const Rectangle = ({
  shapeProps,
  isSelected,
  onSelect,
  onChange,
  groupProps,
}) => {
  const shapeRef = useRef();
  const trRef = useRef();

  useEffect(() => {
    if (isSelected) {
      trRef.current.nodes([shapeRef.current]);
      trRef.current.getLayer().batchDraw();
    }
  }, [isSelected]);

  const onTransformEnd = () => {
    const old = shapeRef.current;
    const scaleX = old.scaleX();
    const scaleY = old.scaleY();

    old.scaleX(1);
    old.scaleY(1);
    onChange({
      ...groupProps,
      x: old.x(),
      y: old.y(),
      width: Math.max(5, old.width() * scaleX),
      height: Math.max(old.height() * scaleY),
    });
  };

  const onDragMove = (e) => {
    let newX = e.target.x();
    let newY = e.target.y();

    // console.log("newX", newX);
    // console.log("newY", newY);

    // const isOut =
    //   newX < 0 ||
    //   newY < 0 ||
    //   newX + groupProps.width > CANVAS_SIZE.width ||
    //   newY + groupProps.height > CANVAS_SIZE.height;

    // if (isOut) {
    //   newX = groupProps.x;
    //   newY = groupProps.y;
    // }

    onChange({
      ...groupProps,
      x: newX,
      y: newY,
    });
  };

  let first_name = shapeProps.first_name ? shapeProps.first_name : "";
  let last_name = shapeProps.last_name ? shapeProps.last_name : "";

  console.log("groupProps", groupProps);

  return (
    <>
      <Group
        draggable
        {...groupProps}
        onClick={onSelect}
        // onDragEnd={(e) => onDragEnd(e)}
        onTransformEnd={() => onTransformEnd()}
        onDragMove={(e) => onDragMove(e)}
        ref={shapeRef}
      >
        <Rect
          {...shapeProps}
          width={groupProps.width}
          height={groupProps.height}
        />
        <Text
          text={first_name.concat(" ", last_name)}
          x={shapeProps.x}
          y={shapeProps.y}
          fontSize={15}
          fill="white"
        />
      </Group>
      {isSelected && (
        <Transformer
          ref={trRef}
          rotateEnabled={false}
          boundBoxFunc={(oldBox, newBox) => {
            if (newBox.width < 5 || newBox.height < 5) {
              return oldBox;
            }

            const isOut =
              oldBox.x < 0 ||
              oldBox.y < 0 ||
              oldBox.x + oldBox.width > CANVAS_SIZE.width ||
              oldBox.y + oldBox.height > CANVAS_SIZE.height;

            if (isOut) {
              return oldBox;
            }
            return newBox;
          }}
        />
      )}
    </>
  );
};

export default Rectangle;
