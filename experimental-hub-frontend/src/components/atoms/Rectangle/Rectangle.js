import { useEffect, useRef } from "react";
import { Group, Rect, Text, Transformer } from "react-konva";

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

  const onDragEnd = (e) => {
    onChange({
      ...groupProps,
      x: e.target.x(),
      y: e.target.y(),
    });
  };

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

  console.log("groupProps", groupProps);
  console.log("shapeProps", shapeProps);
  return (
    <>
      <Group
        draggable
        {...groupProps}
        onClick={onSelect}
        onDragEnd={(e) => onDragEnd(e)}
        onTransformEnd={() => onTransformEnd()}
        ref={shapeRef}
      >
        <Rect
          {...shapeProps}
          width={groupProps.width}
          height={groupProps.height}
        />
        <Text
          text={shapeProps.text}
          align="center"
          x={shapeProps.x}
          y={shapeProps.y}
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
            return newBox;
          }}
        />
      )}
    </>
  );
};

export default Rectangle;
