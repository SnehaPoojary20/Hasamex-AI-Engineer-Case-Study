import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">Call Analysis</div>

      <div className="navbar-links">
        <Link to="/">Ask</Link>
        <Link to="/guide">Guide</Link>
        <Link to="/themes">Themes</Link>
        <Link to="/quotes">Quotes</Link>
      </div>
    </nav>
  );
}

export default Navbar;