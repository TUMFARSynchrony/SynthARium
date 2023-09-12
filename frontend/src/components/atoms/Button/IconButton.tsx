import { IconType } from "react-icons";

type Props = {
  icon: IconType;
  size: number;
  onToggle: () => void;
};

export const IconButton = (props: Props) => {
  const { icon: Icon, size, onToggle } = props;
  return (
    <button
      className="px-3 py-1 bg-stone-100 rounded-xl hover:bg-stone-200"
      onClick={onToggle}
    >
      <Icon size={size} />
    </button>
  );
};
