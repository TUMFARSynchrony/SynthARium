import "./Button.css";

function Button({ name, onClick }) {
  return (
    <button className="button" onClick={onClick}>
      {name}
    </button>
  );
}

export default Button;
