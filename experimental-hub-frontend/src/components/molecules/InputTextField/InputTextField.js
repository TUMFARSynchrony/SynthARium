import InputField from "../../atoms/InputField/InputField";
import Label from "../../atoms/Label/Label";
import "./InputTextField.css";

function InputTextField({ title, value, placeholder, readonly, onChange }) {
  return (
    <div className="inputFieldContainer">
      <Label title={title} />
      <InputField
        inputType={"text"}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        readonly={readonly}
      />
    </div>
  );
}

export default InputTextField;
