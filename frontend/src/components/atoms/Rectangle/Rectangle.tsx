import React, { useEffect, useRef } from "react";
import Konva from "konva";
import { Group, Rect, Text, Transformer } from "react-konva";
import { getTotalBox } from "../../../utils/utils";
import { Shape, Group as GroupProps } from "../../../types";
import { CANVAS_SIZE } from "../../../utils/constants";

type RectangleProps = {
  shapeProps: Shape;
  groupProps: GroupProps;
  isSelected: boolean;
  onSelect: () => void;
  onChange: (newAttr: GroupProps) => void;
};

const Rectangle = ({
  shapeProps,
  groupProps,
  isSelected,
  onSelect,
  onChange
}: RectangleProps) => {
  const shapeRef = useRef<Konva.Group>();
  const trRef = useRef<Konva.Transformer>();
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

  const onDragMove = () => {
    onSelect();
    let newAbsPos: { x: number; y: number } | undefined = undefined;

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

  const participant_name = shapeProps.participant_name
    ? shapeProps.participant_name
    : "";

  return (
    <>
      <Group
        draggable
        {...groupProps}
        onClick={onSelect}
        onTransformEnd={() => onTransformEnd()}
        onDragMove={() => onDragMove()}
        ref={shapeRef}
      >
        <Rect
          {...shapeProps}
          width={groupProps.width}
          height={groupProps.height}
        />
        <Text
          text={participant_name}
          x={shapeProps.x + 5}
          y={shapeProps.y + 5}
          fontSize={20}
          fill="white"
          stroke="#F5F5F5"
          strokeWidth={0.25}
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
