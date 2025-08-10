import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Menu, X } from "lucide-react";
import { ThemeToggle } from "@/components/theme/ThemeToggle";

interface Item {
  name: string;
  path: string;
}

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const navigate = useNavigate();
  const isLoggedIn = Boolean(localStorage.getItem("access_token"));
  const logout = () => {
    localStorage.removeItem("access_token");
    navigate("/auth/login");
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const isActive = (path: string): boolean => {
    return location.pathname === path;
  };

  // Minimal links for notes app
  const links: Item[] = isLoggedIn
    ? [
        { name: "Home", path: "/" },
        { name: "Notes", path: "/notes" },
      ]
    : [{ name: "Home", path: "/" }];

  return (
    <nav className="py-4 bg-background border-b">
      <div className="container-custom flex justify-between items-center">
        {/* Logo */}
        <Link to="/" className="flex items-center">
          <span className="text-2xl font-bold text-blue-700">Notes App</span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center space-x-8">
          <div className="flex space-x-6">
            {links.map((link) => (
              <Link
                key={link.name}
                to={link.path}
                className={`text-base mt-[0.7vh] ${
                  isActive(link.path)
                    ? "text-blue-700 font-medium"
                    : "text-gray-500 hover:text-blue-700 transition-colors"
                }`}
              >
                {link.name}
              </Link>
            ))}
          </div>
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            {!isLoggedIn ? (
              <>
                <Link
                  to="/auth/login"
                  className="px-4 py-2 border rounded text-primary border-primary hover:bg-primary/10 transition-colors"
                >
                  Login
                </Link>
                <Link
                  to="/auth/signup"
                  className="px-4 py-2 rounded bg-primary text-white hover:bg-primary/80 transition-colors"
                >
                  Sign Up
                </Link>
              </>
            ) : (
              <Button variant="ghost" onClick={logout}>
                Log Out
              </Button>
            )}
          </div>
        </div>

        {/* Mobile Menu Button */}
        <div className="md:hidden">
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleMenu}
            aria-label="Toggle Menu"
          >
            {isMenuOpen ? (
              <X className="h-6 w-6" />
            ) : (
              <Menu className="h-6 w-6" />
            )}
          </Button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden absolute top-16 left-0 right-0 bg-background border-t z-50">
          <div className="flex flex-col px-4 py-4 space-y-4">
            {links.map((link) => (
              <Link
                key={link.name}
                to={link.path}
                className={`text-base py-2 ${
                  isActive(link.path)
                    ? "text-blue-700 font-medium"
                    : "text-gray-500"
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                {link.name}
              </Link>
            ))}
            <div className="pt-2 flex flex-col space-y-3">
              <div className="flex justify-center">
                <ThemeToggle />
              </div>
              {!isLoggedIn ? (
                <>
                  <Link
                    to="/auth/login"
                    className="w-full px-4 py-2 border rounded text-primary border-primary hover:bg-primary/10 transition-colors text-center"
                  >
                    Login
                  </Link>
                  <Link
                    to="/auth/signup"
                    className="w-full px-4 py-2 rounded bg-primary text-white hover:bg-primary/80 transition-colors text-center"
                  >
                    Sign Up
                  </Link>
                </>
              ) : (
                <Button variant="ghost" onClick={logout}>
                  Log Out
                </Button>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
