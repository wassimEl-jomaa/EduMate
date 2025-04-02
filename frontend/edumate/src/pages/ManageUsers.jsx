import React, { useState, useEffect } from "react";
import axios from "axios";

const ManageUsers = () => {
  const [users, setUsers] = useState([]); // State for the list of users
  const [userData, setUserData] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    phone_number: "",
    arskurs_id: 0,
    role_id: 0,
    membership_id: 0,
  }); // State for user data
  const [editingUserId, setEditingUserId] = useState(null); // State for editing user ID
  const [successMessage, setSuccessMessage] = useState(""); // State for success message
  const [errorMessage, setErrorMessage] = useState(""); // State for error message

  // Fetch users from the backend
  useEffect(() => {
    const fetchUsers = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await axios.get("http://localhost:8000/users/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUsers(response.data);
      } catch (error) {
        console.error(
          "Error fetching users:",
          error.response?.data || error.message
        );
      }
    };

    fetchUsers();
  }, []);
  // Add or update a user
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!userData.username || !userData.email) {
      setErrorMessage("Username and email are required.");
      return;
    }

    const token = localStorage.getItem("token");

    try {
      if (editingUserId) {
        // Update user
        const response = await axios.patch(
          `http://localhost:8000/users/${editingUserId}`,
          userData,
          {
            headers: {
              Authorization: `Bearer ${token}`, // Include the token
            },
          }
        );
        setUsers((prevUsers) =>
          prevUsers.map((user) =>
            user.id === editingUserId ? response.data : user
          )
        );
        setSuccessMessage(
          `User "${response.data.username}" updated successfully!`
        );
      } else {
        // Add user
        const response = await axios.post(
          "http://localhost:8000/users/",
          userData,
          {
            headers: {
              Authorization: `Bearer ${token}`, // Include the token
            },
          }
        );
        setUsers((prevUsers) => [...prevUsers, response.data]);
        setSuccessMessage(
          `User "${response.data.username}" added successfully!`
        );
      }

      setErrorMessage("");
      setUserData({
        username: "",
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        phone_number: "",
        arskurs_id: 0,
        role_id: 0,
        membership_id: 0,
      });
      setEditingUserId(null);
    } catch (error) {
      console.error(
        "Error managing user:",
        error.response?.data || error.message
      );
      setErrorMessage("Failed to manage user. Please try again.");
      setSuccessMessage("");
    }
  };

  // Delete a user
  const handleDelete = async (userId) => {
    const token = localStorage.getItem("token"); // Retrieve the token from localStorage
    try {
      await axios.delete(`http://localhost:8000/users/${userId}/`, {
        headers: {
          Authorization: `Bearer ${token}`, // Include the token in the Authorization header
        },
      });
      setUsers((prevUsers) => prevUsers.filter((user) => user.id !== userId));
      setSuccessMessage("User deleted successfully!");
      setErrorMessage("");
    } catch (error) {
      console.error(
        "Error deleting user:",
        error.response?.data || error.message
      );
      setErrorMessage("Failed to delete user. Please try again.");
      setSuccessMessage("");
    }
  };

  // Start editing a user
  const handleEdit = (user) => {
    setUserData({
      username: user.username,
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      password: "", // Leave password empty for security
      phone_number: user.phone_number,
      arskurs_id: user.arskurs_id || 0,
      role_id: user.role_id || 0,
      membership_id: user.membership_id || 0,
    });
    setEditingUserId(user.id);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="max-w-lg mx-auto bg-white p-8 border rounded-lg shadow-md mt-10">
      <h1 className="text-2xl font-bold mb-6">Manage Users</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label
            htmlFor="username"
            className="block text-gray-700 font-semibold"
          >
            Username
          </label>
          <input
            type="text"
            id="username"
            name="username"
            value={userData.username}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter username"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="first_name"
            className="block text-gray-700 font-semibold"
          >
            First Name
          </label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={userData.first_name}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter first name"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="last_name"
            className="block text-gray-700 font-semibold"
          >
            Last Name
          </label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={userData.last_name}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter last name"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 font-semibold">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={userData.email}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter email"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="password"
            className="block text-gray-700 font-semibold"
          >
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={userData.password}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter password"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="phone_number"
            className="block text-gray-700 font-semibold"
          >
            Phone Number
          </label>
          <input
            type="text"
            id="phone_number"
            name="phone_number"
            value={userData.phone_number}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter phone number"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="arskurs_id"
            className="block text-gray-700 font-semibold"
          >
            Arskurs ID
          </label>
          <input
            type="number"
            id="arskurs_id"
            name="arskurs_id"
            value={userData.arskurs_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter arskurs ID"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="role_id"
            className="block text-gray-700 font-semibold"
          >
            Role ID
          </label>
          <input
            type="number"
            id="role_id"
            name="role_id"
            value={userData.role_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter role ID"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="membership_id"
            className="block text-gray-700 font-semibold"
          >
            Membership ID
          </label>
          <input
            type="number"
            id="membership_id"
            name="membership_id"
            value={userData.membership_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter membership ID"
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
          {editingUserId ? "Update User" : "Add User"}
        </button>
      </form>

      <h2 className="text-xl font-bold mt-8 mb-4">Existing Users</h2>
      <ul className="space-y-4">
        {users.map((user) => (
          <li
            key={user.id}
            className="flex justify-between items-center bg-gray-100 p-4 rounded-md"
          >
            <span>
              {user.username} ({user.email})
            </span>
            <div className="space-x-2">
              <button
                onClick={() => handleEdit(user)}
                className="text-blue-500 hover:text-blue-700"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(user.id)}
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

export default ManageUsers;
