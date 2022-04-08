import InputField from "../../atoms/InputField/InputField";
import Label from "../../atoms/Label/Label";
import "./InputDateField.css";

function InputDateField({ title }) {
  return (
    <div className="inputDateFieldContainer">
      <Label title={title} />
      <InputField inputType={"date"} />
    </div>
  );
}

export default InputDateField;
