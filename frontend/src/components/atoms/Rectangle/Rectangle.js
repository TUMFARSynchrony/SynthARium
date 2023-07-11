import { useEffect, useRef } from "react";
import { Group, Rect, Text, Transformer } from "react-konva";
import { CANVAS_SIZE } from "../../../utils/constants";
import { getTotalBox } from "../../../utils/utils";

const Rectangle = ({
  shapeProps,
  groupProps,
  isSelected,
  onSelect,
  onChange
}) => {
  const shapeRef = useRef();
  const trRef = useRef();

  useEffect(() => {
    if (!trRef.current) {
      return;
    }

    if (isSelected) {
      trRef.current.nodes([shapeRef.current]);
      trRef.current.getLayer().batchDraw();
    }
  }, [isSelected]);

  const onTransformEnd = () => {
    if (!shapeRef.current) {
      return;
    }
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
      height: Math.max(old.height() * scaleY)
    });
  };

  const onDragMove = (e) => {
    onSelect(e);
    let newAbsPos = {};

    if (!trRef.current) {
      return;
    }

    const boxes = trRef.current.nodes().map((node) => node.getClientRect());
    const box = getTotalBox(boxes);
    trRef.current.nodes().forEach((shape) => {
      const absPos = shape.getAbsolutePosition();
      const offsetX = box.x - absPos.x;
      const offsetY = box.y - absPos.y;

      newAbsPos = { ...absPos };
      if (box.x < 0) {
        newAbsPos.x = -offsetX;
      }
      if (box.y < 0) {
        newAbsPos.y = -offsetY;
      }
      if (box.x + box.width > CANVAS_SIZE.width) {
        newAbsPos.x = CANVAS_SIZE.width - box.width - offsetX;
      }
      if (box.y + box.height > CANVAS_SIZE.height) {
        newAbsPos.y = CANVAS_SIZE.height - box.height - offsetY;
      }
    });
    shapeRef.current.x(newAbsPos.x);
    shapeRef.current.y(newAbsPos.y);

    onChange({
      ...groupProps,
      ...newAbsPos
    });
  };

  let participant_name = shapeProps.participant_name
    ? shapeProps.participant_name
    : "";

  return (
    <>
      <Group
        draggable
        {...groupProps}
        onClick={onSelect}
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
          text={participant_name}
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
              newBox.x < 0 ||
              newBox.y < 0 ||
              newBox.x + newBox.width > CANVAS_SIZE.width ||
              newBox.y + newBox.height > CANVAS_SIZE.height;

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
