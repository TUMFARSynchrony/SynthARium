import { Link } from "react-router-dom";
import "./Button.css";

function Button({ name, to }) {
  return (
    <Link className="btn" to={to}>
      {name}
    </Link>
  );
}

export default Button;
