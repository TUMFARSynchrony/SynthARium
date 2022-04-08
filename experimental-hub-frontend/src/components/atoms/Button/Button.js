import "./Button.css";

function Button({ name, onClick, design, icon }) {
  return (
    <button className={"button " + design} onClick={onClick}>
      {icon}
      {name}
    </button>
  );
}

export default Button;
