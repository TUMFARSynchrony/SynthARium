import InputField from "../../atoms/InputField/InputField";
import Label from "../../atoms/Label/Label";
import "./Checkbox.css";

function Checkbox({ title }) {
  return (
    <div className="checkboxContainer">
      <Label title={title} />
      <InputField inputType={"checkbox"} />
    </div>
  );
}

export default Checkbox;
