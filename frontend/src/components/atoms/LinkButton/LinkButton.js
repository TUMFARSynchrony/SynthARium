import { Link } from "react-router-dom";
import "./LinkButton.css";

function LinkButton({ name, to, state, onClick }) {
  return (
    <Link className="linkButton" to={to} state={state} onClick={onClick}>
      {name}
    </Link>
  );
}

export default LinkButton;
