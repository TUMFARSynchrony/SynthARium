import { Link } from "react-router-dom";
import "./PostProcessing.css";

function PostProcessing() {
  return (
    <div>
      <h1>Post-Processing Room</h1>
      <Link to="/">
        <span>Main Page</span>
      </Link>
    </div>
  );
}

export default PostProcessing;
