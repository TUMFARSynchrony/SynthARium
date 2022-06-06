import "./InputField.css";

function InputField({
  inputType,
  value,
  placeholder,
  readonly,
  onChange,
  checked,
  register,
  required,
  label,
  max,
  min,
}) {
  return (
    <input
      {...register(label, { required })}
      type={inputType}
      className={"inputField " + inputType}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      readOnly={readonly}
      checked={checked}
      max={max}
      min={min}
    ></input>
  );
}

export default InputField;
