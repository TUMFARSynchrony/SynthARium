import { Link } from "react-router-dom";
import "../IconButton/IconButton.css";

function IconButton({to, state, onClick, IconName }) {
    return (
      <Link className="iconButton" to={to} state={state} onClick={onClick}>
        <IconName />
      </Link>
    );
  }
  
  export default IconButton;