import InputField from "../../atoms/InputField/InputField";
import Label from "../../atoms/Label/Label";
import "./InputDateField.css";

function InputDateField({ title, placeholder, readonly, onChange }) {
  return (
    <div className="inputDateFieldContainer">
      <Label title={title} />
      <InputField
        inputType={"datetime-local"}
        placeholder={placeholder}
        readonly={readonly}
        onChange={onChange}
      />
    </div>
  );
}

export default InputDateField;
