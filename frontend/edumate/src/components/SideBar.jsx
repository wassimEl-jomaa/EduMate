import React from "react";
import { Link } from "react-router-dom";

const SideBar = () => {
  return (
    <div className="bg-blue-100 py-2 mb-6">
      <div className="sidebar-container">
        <div className="sidebar-logo text-center mb-6">
          <h2 className="text-2xl font-semibold">My App</h2>
        </div>
        <nav className="sidebar-nav">
          <ul className="space-y-4">
            <li>
              <Link
                to="/home"
                className="block py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
              >
                Profil
              </Link>
            </li>
            <li>
              <Link
                to="/about"
                className="block py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
              >
                Betyg
              </Link>
            </li>

            <li>
              <Link
                to="/services"
                className="block py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
              >
                Feedback & Support
              </Link>
            </li>
            <li>
              <Link
                to="/contact"
                className="block py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
              >
                Pågående Läxor
              </Link>
            </li>
            <li>
              <Link
                to="/contact"
                className="block py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
              >
                Meddelande
              </Link>
            </li>
            <li>
              <Link
                to="/contact"
                className="block py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
              >
                Rekommenderade Resurser
              </Link>
            </li>
            <li>
              <Link
                to="/contact"
                className="block py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
              >
                AI-genererade Förslag
              </Link>
            </li>
            <li>
              <Link
                to="/about"
                className="block py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
              >
                Motiverande Innehåll
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default SideBar;
