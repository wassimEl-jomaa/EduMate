import React, { useState, useEffect } from "react";
import axios from "axios";

const ManageUsers = () => {
  const [users, setUsers] = useState([]); // State for the list of users
  const [arskurser, setArskurser] = useState([]); // State for the list of Arskurs
  const [userData, setUserData] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    phone_number: "",
    arskurs_id: "",
    role_id: 0,
  }); // State for user data
  const [editingUserId, setEditingUserId] = useState(null); // State for editing user ID
  const [successMessage, setSuccessMessage] = useState(""); // State for success message
  const [userType, setUserType] = useState("Student"); // State for user type (default: Student)
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

  // Fetch Arskurs options from the backend
  useEffect(() => {
    const fetchArskurser = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await axios.get("http://localhost:8000/arskurs/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setArskurser(response.data);
      } catch (error) {
        console.error(
          "Error fetching Arskurser:",
          error.response?.data || error.message
        );
      }
    };

    fetchArskurser();
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
        arskurs_id: "",
        role_id: "",
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
  const handleUserTypeChange = (e) => {
    setUserType(e.target.value);
    setUserData({
      username: "",
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      phone_number: "",
      arskurs_id: "",
      role_id: 0,

      subject_id: null,
      qualifications: "",
    });
  };
  return (
    <div className="container mx-auto px-6 py-10">
      <h1 className="text-4xl font-extrabold text-gray-800 mb-8 text-center tracking-wide leading-tight">
        User Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-8">
        {/* Student Section */}
        <div className="bg-white p-6 rounded-lg shadow-xl border border-blue-200">
          <h2 className="text-2xl font-semibold text-blue-700 mb-6">Student</h2>

          <div className="space-y-4">
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Add Student
            </button>
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get all Students
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-green-600 text-white rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get Students by Årskurs
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-yellow-600 text-white rounded-md hover:bg-yellow-700 focus:ring-2 focus:ring-yellow-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get Students by Name
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-orange-600 text-white rounded-md hover:bg-orange-700 focus:ring-2 focus:ring-orange-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Update a Student
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-red-600 text-white rounded-md hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Delete a Student
            </button>
          </div>
        </div>

        {/* Parents Section */}
        <div className="bg-white p-6 rounded-lg shadow-xl border border-blue-200">
          <h2 className="text-2xl font-semibold text-blue-700 mb-6">Parents</h2>

          <div className="space-y-4">
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Add Parent
            </button>
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get all Parents
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-green-600 text-white rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get Parents by Årskurs
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-yellow-600 text-white rounded-md hover:bg-yellow-700 focus:ring-2 focus:ring-yellow-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get Parents by Student Name
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-orange-600 text-white rounded-md hover:bg-orange-700 focus:ring-2 focus:ring-orange-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Update a Parent
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-red-600 text-white rounded-md hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Delete a Parent
            </button>
          </div>
        </div>

        {/* Teachers Section */}
        <div className="bg-white p-6 rounded-lg shadow-xl border border-blue-200">
          <h2 className="text-2xl font-semibold text-blue-700 mb-6">
            Teachers
          </h2>

          <div className="space-y-4">
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Add Teacher
            </button>
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get all Teachers
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-green-600 text-white rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get Teachers by Årskurs
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-yellow-600 text-white rounded-md hover:bg-yellow-700 focus:ring-2 focus:ring-yellow-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get Teachers by Student Name
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-orange-600 text-white rounded-md hover:bg-orange-700 focus:ring-2 focus:ring-orange-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Update a Teacher
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-red-600 text-white rounded-md hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Delete a Teacher
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-lg mx-auto bg-white p-8 border rounded-lg shadow-md mt-10">
        <h1 className="text-2xl font-bold mb-6">Manage Users</h1>
        <form onSubmit={handleSubmit}>
          {/* User Type Selection */}
          <div className="mb-4">
            <label
              htmlFor="user_type"
              className="block text-gray-700 font-semibold"
            >
              User Type
            </label>
            <select
              id="user_type"
              name="user_type"
              value={userType}
              onChange={handleUserTypeChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Student">Student</option>
              <option value="Teacher">Teacher</option>
              <option value="Parent">Parent</option>
            </select>
          </div>

          {/* Other input fields */}
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

          {/* Other input fields for first_name, last_name, email, etc. */}

          {/* Arskurs Dropdown */}
          <div className="mb-4">
            <label
              htmlFor="arskurs_id"
              className="block text-gray-700 font-semibold"
            >
              Årskurs
            </label>
            <select
              id="arskurs_id"
              name="arskurs_id"
              value={userData.arskurs_id}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={0}>Select Arskurs</option>
              {arskurser.map((arskurs) => (
                <option key={arskurs.id} value={arskurs.id}>
                  {arskurs.name}
                </option>
              ))}
            </select>
          </div>

          {/* Success and Error messages */}
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
      </div>

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
