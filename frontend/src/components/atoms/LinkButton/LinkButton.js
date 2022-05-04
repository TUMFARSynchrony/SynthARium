import { Link } from "react-router-dom";
import "./LinkButton.css";

function LinkButton({ name, to, onClick, state }) {
  return (
    <Link className="linkButton" to={to} onClick={onClick} state={state}>
      {name}
    </Link>
  );
}

export default LinkButton;
