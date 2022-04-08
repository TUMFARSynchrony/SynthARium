import "./InputField.css";

function InputField({ inputType, value, onChange }) {
  return (
    <input
      type={inputType}
      className={"inputField " + inputType}
      value={value}
      onChange={(e) => onChange(e.target.value)}
    ></input>
  );
}

export default InputField;
