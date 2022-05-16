import InputField from "../../atoms/InputField/InputField";
import Label from "../../atoms/Label/Label";
import "./Checkbox.css";

function Checkbox({
  title,
  value,
  onChange,
  checked,
  register,
  label,
  required,
}) {
  return (
    <div className="checkboxContainer">
      <Label title={title} />
      <InputField
        inputType={"checkbox"}
        value={value}
        onChange={onChange}
        checked={checked}
        register={register}
        label={label}
        required={required}
      />
    </div>
  );
}

export default Checkbox;
