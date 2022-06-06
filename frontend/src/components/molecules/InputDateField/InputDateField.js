import InputField from "../../atoms/InputField/InputField";
import Label from "../../atoms/Label/Label";
import "./InputDateField.css";

function InputDateField({
  title,
  placeholder,
  readonly,
  onChange,
  register,
  label,
  required,
  value,
}) {
  return (
    <div className="inputDateFieldContainer">
      <Label title={title} />
      <InputField
        inputType={"datetime-local"}
        placeholder={placeholder}
        readonly={readonly}
        onChange={onChange}
        register={register}
        label={label}
        required={required}
        value={value}
      />
    </div>
  );
}

export default InputDateField;
