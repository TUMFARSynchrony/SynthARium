import { Link } from "react-router-dom";
import "./LinkButton.css";

function LinkButton({ name, to, onClick, design }) {
  return (
    <Link className={"linkButton " + design} to={to} onClick={onClick}>
      {name}
    </Link>
  );
}

export default LinkButton;
