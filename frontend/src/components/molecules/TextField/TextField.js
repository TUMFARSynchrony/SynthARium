import "./TextField.css";
import Label from "../../atoms/Label/Label";

function TextField({
  title,
  value,
  onChange,
  placeholder,
  register,
  required,
  label,
}) {
  return (
    <div className="textAreaContainer">
      <Label title={title} />
      <textarea
        {...register(label, { required })}
        className="textAreaField"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      ></textarea>
    </div>
  );
}

export default TextField;
