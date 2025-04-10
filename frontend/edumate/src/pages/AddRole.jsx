import React, { useState, useEffect } from "react";
import axios from "axios";

const AddRole = () => {
  const [role_name, setRoleName] = useState(""); // State for role name
  const [roles, setRoles] = useState([]); // State for the list of roles
  const [successMessage, setSuccessMessage] = useState(""); // State for success message
  const [errorMessage, setErrorMessage] = useState(""); // State for error message
  const [editingRoleId, setEditingRoleId] = useState(null); // State for editing role ID

  // Fetch roles from the backend
  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const token = localStorage.getItem("token"); // Retrieve the token from localStorage
        const response = await axios.get("http://localhost:8000/roles", {
          headers: {
            Authorization: `Bearer ${token}`, // Include the token in the Authorization header
          },
        });
        console.log("Fetched Roles:", response.data); // Debugging log
        setRoles(response.data);
      } catch (error) {
        console.error("Error fetching roles:", error.response || error);
        setErrorMessage("Failed to fetch roles. Please try again.");
      }
    };

    fetchRoles();
  }, []);

  // Add or update a role
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!role_name) {
      setErrorMessage("Role name is required.");
      return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
      setErrorMessage("You are not authenticated. Please log in.");
      return;
    }

    try {
      if (editingRoleId) {
        // Update role
        const response = await axios.put(
          `http://localhost:8000/roles/${editingRoleId}/`,
          { name: role_name }, // Use "name" instead of "role_name"
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setRoles((prevRoles) =>
          prevRoles.map((role) =>
            role.id === editingRoleId ? response.data : role
          )
        );
        setSuccessMessage(`Role "${response.data.name}" updated successfully!`);
      } else {
        // Add role
        const response = await axios.post(
          "http://localhost:8000/roles/",
          { name: role_name }, // Use "name" instead of "role_name"
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setRoles((prevRoles) => [...prevRoles, response.data]);
        setSuccessMessage(`Role "${response.data.name}" added successfully!`);
      }

      setErrorMessage("");
      setRoleName("");
      setEditingRoleId(null);
    } catch (error) {
      console.error(
        "Error managing role:",
        error.response?.data?.detail || error.message
      );
      if (error.response?.status === 422) {
        setErrorMessage("Invalid role data. Please check your input.");
      } else if (error.response?.status === 403) {
        setErrorMessage("You do not have permission to manage roles.");
      } else {
        setErrorMessage("Failed to manage role. Please try again.");
      }
      setSuccessMessage("");
    }
  };

  // Edit a role
  const handleEdit = (role) => {
    setEditingRoleId(role.id); // Set the ID of the role being edited
    setRoleName(role.name); // Populate the role name in the input field
    setErrorMessage(""); // Clear any error messages
    setSuccessMessage(""); // Clear any success messages
  };

  // Delete a role
  const handleDelete = async (roleId) => {
    const token = localStorage.getItem("token");
    if (!token) {
      setErrorMessage("You are not authenticated. Please log in.");
      return;
    }

    try {
      await axios.delete(`http://localhost:8000/roles/${roleId}/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setRoles((prevRoles) => prevRoles.filter((role) => role.id !== roleId));
      setSuccessMessage("Role deleted successfully!");
      setErrorMessage("");
    } catch (error) {
      console.error(
        "Error deleting role:",
        error.response?.data?.detail || error.message
      );
      if (error.response?.status === 403) {
        setErrorMessage("You do not have permission to delete roles.");
      } else if (error.response?.status === 404) {
        setErrorMessage("Role not found.");
      } else {
        setErrorMessage("Failed to delete role. Please try again.");
      }
      setSuccessMessage("");
    }
  };

  return (
    <div className="max-w-lg mx-auto bg-white p-8 border rounded-lg shadow-md mt-10">
      <h1 className="text-2xl font-bold mb-6">Manage Roles</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label
            htmlFor="roleName"
            className="block text-gray-700 font-semibold"
          >
            Role Name
          </label>
          <input
            type="text"
            id="roleName"
            name="roleName"
            value={role_name}
            onChange={(e) => setRoleName(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter role name"
          />
        </div>
        {errorMessage && (
          <p className="text-red-500 text-sm mb-4">{errorMessage}</p>
        )}
        {successMessage && (
          <p className="text-green-500 text-sm mb-4">{successMessage}</p>
        )}
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-all"
        >
          {editingRoleId ? "Update Role" : "Add Role"}
        </button>
      </form>

      <h2 className="text-xl font-bold mt-8 mb-4">Existing Roles</h2>
      <ul className="space-y-4">
        {roles.map((role) => (
          <li
            key={role.id}
            className="flex justify-between items-center bg-gray-100 p-4 rounded-md"
          >
            <span>{role.name}</span>
            <div className="space-x-2">
              <button
                onClick={() => handleEdit(role)}
                className="text-blue-500 hover:text-blue-700"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(role.id)}
                className="text-red-500 hover:text-red-700"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AddRole;
