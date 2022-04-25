import InputField from "../../atoms/InputField/InputField";
import Label from "../../atoms/Label/Label";
import "./Checkbox.css";

function Checkbox({ title, value, onChange, defaultChecked }) {
  return (
    <div className="checkboxContainer">
      <Label title={title} />
      <InputField
        inputType={"checkbox"}
        value={value}
        onChange={onChange}
        defaultChecked={defaultChecked}
      />
    </div>
  );
}

export default Checkbox;
