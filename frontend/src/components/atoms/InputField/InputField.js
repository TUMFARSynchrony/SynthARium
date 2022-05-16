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
    ></input>
  );
}

export default InputField;
