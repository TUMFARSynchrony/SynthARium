import InputField from "../../atoms/InputField/InputField";
import Label from "../../atoms/Label/Label";
import "./InputTextField.css";

function InputTextField({ title, value, onChange }) {
  return (
    <div className="inputFieldContainer">
      <Label title={title} />
      <InputField inputType={"text"} value={value} onChange={onChange} />
    </div>
  );
}

export default InputTextField;
