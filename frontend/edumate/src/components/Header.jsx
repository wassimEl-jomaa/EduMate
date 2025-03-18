import React from "react";
import { Link } from "react-router-dom";

export default function Header({ signedIn, setSignedIn }) {
  const logout = () => {
    setSignedIn(false); // Log the user out
  };

  return (
    <header className="bg-blue-100 py-2 mb-2">
      <nav className="mx-auto flex justify-between items-center">
        {/* Left section: Logo, Home, About Us */}
        <div className="flex items-center space-x-6">
          <img
            src="/Edumate_transparent-logo.png"
            alt="Logo"
            className="h-12 w-auto"
          />
          <Link
            to="/"
            className="font-bold font-sans text-xl text-white bg-blue-400 px-4 py-2 rounded hover:bg-blue-300 transition-all mr-4 "
          >
            Hem
          </Link>
          <Link
            to="/aboutUs"
            className="font-bold font-sans text-xl text-white bg-blue-400 px-4 py-2 rounded hover:bg-blue-300 transition-all"
          >
            Om Oss
          </Link>
        </div>

        {/* Right section: Login and Register */}
        {!signedIn ? (
          <ul className="flex space-x-4 text-white ml-auto">
            <li>
              <Link
                to="/admin"
                className="font-bold font-sans text-xl text-white bg-blue-400 px-4 py-2 rounded hover:bg-blue-300 transition-all mr-4 "
              >
                Admin
              </Link>
              <Link
                to="/login"
                className="font-bold font-sans text-xl text-white bg-blue-400 px-4 py-2 rounded hover:bg-blue-300 transition-all "
              >
                Logga in
              </Link>
            </li>
            <li>
              <Link
                to="/register"
                className="font-bold font-sans text-xl text-white bg-blue-400 px-4 py-2 rounded hover:bg-blue-300 transition-all mr-4"
              >
                Registrera
              </Link>
            </li>
          </ul>
        ) : (
          <ul className="flex space-x-4 text-white ml-auto">
            <li>
              <Link
                to="/Profil"
                className="font-bold font-sans text-xl text-white bg-blue-400 px-4 py-2 rounded hover:bg-blue-300 "
              >
                Profil
              </Link>
            </li>
            <li>
              <Link
                to="/MinSida"
                className="font-bold font-sans text-xl text-white bg-blue-400 px-4 py-2 rounded hover:bg-blue-300 "
              >
                Min sida
              </Link>
            </li>
            <li>
              <Link
                to="/"
                onClick={logout}
                className="font-bold font-sans text-xl text-white bg-blue-400 px-4 py-2 rounded hover:bg-blue-300 transition-all mr-4"
              >
                Logga ut
              </Link>
            </li>
          </ul>
        )}
      </nav>
    </header>
  );
}
