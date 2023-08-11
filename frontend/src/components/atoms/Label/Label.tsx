import "./Label.css";

type LabelProps = {
  title: string;
};
function Label({ title }: LabelProps) {
  return <label className="label">{title}</label>;
}

export default Label;
