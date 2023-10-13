import "./InputField.css";

type InputFieldProps = {
  inputType: string;
  value: string;
  placeholder?: string;
  readonly?: boolean;
  onChange: (value: string) => void;
  checked?: boolean;
  required?: boolean;
  min?: number | string;
};

function InputField({
  inputType,
  value,
  placeholder,
  readonly,
  onChange,
  checked,
  required,
  min
}: InputFieldProps) {
  return (
    <input
      type={inputType}
      className={`inputField ${inputType}`}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      readOnly={readonly}
      checked={checked}
      min={min}
      required={required}
    />
  );
}

export default InputField;
