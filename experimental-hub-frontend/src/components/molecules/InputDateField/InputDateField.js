import InputField from "../../atoms/InputField/InputField";
import Label from "../../atoms/Label/Label";
import "./InputDateField.css";

function InputDateField({ title, placeholder, readonly }) {
  return (
    <div className="inputDateFieldContainer">
      <Label title={title} />
      <InputField
        inputType={"date"}
        placeholder={placeholder}
        readonly={readonly}
      />
    </div>
  );
}

export default InputDateField;
