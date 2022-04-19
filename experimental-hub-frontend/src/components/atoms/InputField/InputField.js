import "./InputField.css";

function InputField({ inputType, value, placeholder, readonly, onChange }) {
  return (
    <input
      type={inputType}
      className={"inputField " + inputType}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      readOnly={readonly}
      defaultChecked={false}
    ></input>
  );
}

export default InputField;
