import { Link, useLocation } from "react-router-dom";

const navLinks = [
  { path: "/", label: "Home" },
  { path: "/predictions", label: "Predictions" },
  { path: "/about", label: "The Model" },
];

function Navbar() {
  const location = useLocation();

  return (
    <nav className="bg-surface border-b border-white/5 sticky top-0 z-50 backdrop-blur">
      <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
        <Link to="/" className="flex items-center gap-2">
          <span className="w-1 h-6 bg-race-red skew-x-[-12deg]" />
          <span className="font-display font-black text-xl tracking-tight">
            GRID<span className="text-race-red">CAST</span>
          </span>
        </Link>
        <div className="flex gap-8 font-display font-semibold text-sm uppercase tracking-wider">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`transition-colors relative py-1 ${
                location.pathname === link.path
                  ? "text-race-red"
                  : "text-muted hover:text-ink"
              }`}
            >
              {link.label}
              {location.pathname === link.path && (
                <span className="absolute -bottom-1 left-0 right-0 h-0.5 bg-race-red" />
              )}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;