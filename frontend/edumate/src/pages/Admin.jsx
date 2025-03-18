import React from "react";
import { Link } from "react-router-dom";

const Admin = () => {
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-1/4 bg-blue-100 p-4">
        <h2 className="text-2xl font-bold mb-6">Manage Panel</h2>
        <ul className="space-y-4">
          <li>
            <Link
              to="/manage-users"
              className="block text-lg text-blue-800 hover:text-blue-600"
            >
              User
            </Link>
          </li>
          <li>
            <Link
              to="/ManageUsers"
              className="block text-lg text-blue-800 hover:text-blue-600"
            >
              Beytg
            </Link>
          </li>
          <li>
            <Link
              to="/add-role"
              className="block text-lg text-blue-800 hover:text-blue-600"
            >
              Meddelanden
            </Link>
          </li>
          <li>
            <Link
              to="/add-role"
              className="block text-lg text-blue-800 hover:text-blue-600"
            >
              Arskurs
            </Link>
          </li>
          <li>
            <Link
              to="/add-role"
              className="block text-lg text-blue-800 hover:text-blue-600"
            >
              Roles
            </Link>
          </li>
          <li>
            <Link
              to="/manage-memberships"
              className="block text-lg text-blue-800 hover:text-blue-600"
            >
              Membership
            </Link>
          </li>
          <li>
            <Link
              to="/add-homework"
              className="block text-lg text-blue-800 hover:text-blue-600"
            >
              Homework
            </Link>
          </li>
          <li>
            <Link
              to="/add-subject"
              className="block text-lg text-blue-800 hover:text-blue-600"
            >
              Subject
            </Link>
          </li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="w-3/4 p-6">
        <h1 className="text-3xl font-bold mb-4">Welcome to the Admin Page</h1>
        <p className="text-lg text-gray-700">
          Select an option from the sidebar to manage roles, memberships,
          homework, or subjects.
        </p>
      </div>
    </div>
  );
};

export default Admin;
