import "./InputField.css";

function InputField({
  inputType,
  value,
  placeholder,
  readonly,
  onChange,
  defaultChecked,
}) {
  return (
    <input
      type={inputType}
      className={"inputField " + inputType}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      readOnly={readonly}
      defaultChecked={defaultChecked}
    ></input>
  );
}

export default InputField;
