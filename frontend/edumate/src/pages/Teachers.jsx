import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Teachers = ({ userId }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate(); // Initialize navigate

  // Fetch user data
  useEffect(() => {
    const token = localStorage.getItem("token");
    console.log("Fetching user data for userId:", userId);

    const fetchUserData = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/users/${userId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        console.log("Fetched user data:", response.data);
        setUser(response.data);
      } catch (error) {
        console.error(
          "Error fetching user data:",
          error.response?.data || error.message
        );
      }
    };

    if (userId) {
      fetchUserData();
    }
  }, [userId]);

  if (!user) {
    return <p>Loading...</p>;
  }

  return (
    <div className="container mx-auto px-6 py-12">
      <h1 className="text-4xl font-extrabold text-gray-800 mb-8">
        Teacher Dashboard
      </h1>

      {/* Display the teacher's name */}
      <p className="text-lg text-gray-600 mb-8">
        Welcome,{" "}
        <span className="font-semibold text-gray-800">
          {user.first_name} {user.last_name}
        </span>
        !
      </p>

      <div className="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {/* Manage Homework Card */}
        <div className="bg-blue-50 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            Manage Homework
          </h2>
          <button
            onClick={() => navigate("/manage-homework")}
            className="bg-blue-600 text-white text-lg font-semibold px-6 py-3 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Add Homework
          </button>
        </div>

        {/* Manage Betyg Card */}
        <div className="bg-green-50 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            Manage Betyg
          </h2>
          <button
            onClick={() => navigate("/betyg")}
            className="bg-green-600 text-white text-lg font-semibold px-6 py-3 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Add Betyg
          </button>
        </div>

        {/* Manage Meddelanden Card */}
        <div className="bg-yellow-50 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            Manage Meddelanden
          </h2>
          <button
            onClick={() => navigate("/manage-meddelanden")}
            className="bg-yellow-600 text-white text-lg font-semibold px-6 py-3 rounded-md hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-500"
          >
            Add Meddelanden
          </button>
        </div>
      </div>
    </div>
  );
};

export default Teachers;
