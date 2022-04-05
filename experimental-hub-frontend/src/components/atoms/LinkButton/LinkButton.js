import { Link } from "react-router-dom";
import "./LinkButton.css";

function LinkButton({ name, to }) {
  return (
    <Link className="linkButton" to={to}>
      {name}
    </Link>
  );
}

export default LinkButton;
