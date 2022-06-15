import { formatDate } from "../../../utils/utils";
import InputField from "../../atoms/InputField/InputField";
import Label from "../../atoms/Label/Label";
import "./InputDateField.css";

function InputDateField({
  title,
  placeholder,
  readonly,
  onChange,
  required,
  value,
}) {
  const today = formatDate(new Date().getTime());
  return (
    <div className="inputDateFieldContainer">
      <Label title={title} />
      <InputField
        inputType={"datetime-local"}
        placeholder={placeholder}
        readonly={readonly}
        onChange={onChange}
        required={required}
        value={value}
        min={today}
      />
    </div>
  );
}

export default InputDateField;
