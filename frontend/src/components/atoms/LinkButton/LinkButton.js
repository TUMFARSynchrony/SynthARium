import { Link } from "react-router-dom";
import "./LinkButton.css";

function LinkButton({ name, to, onClick }) {
  return (
    <Link className="linkButton" to={to} onClick={onClick}>
      {name}
    </Link>
  );
}

export default LinkButton;
