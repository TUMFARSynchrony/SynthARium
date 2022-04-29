import "./Button.css";

function Button({ name, onClick, design, icon, title }) {
  return (
    <button className={"button " + design} onClick={onClick} title={title}>
      {icon}
      {name}
    </button>
  );
}

export default Button;
