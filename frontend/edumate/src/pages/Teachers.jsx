import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Teachers = () => {
  const [teacher, setTeacher] = useState(null); // State to store teacher's information
  const navigate = useNavigate(); // Initialize the navigate function

  // Fetch teacher data from the backend
  useEffect(() => {
    const fetchTeacher = async () => {
      const token = localStorage.getItem("token"); // Retrieve the token from localStorage
      try {
        const response = await axios.get("http://127.0.0.1:8000/teachers/me/", {
          headers: {
            Authorization: `Bearer ${token}`, // Include the token
          },
        });
        console.log("Fetched teacher data:", response.data); // Debug log
        setTeacher(response.data); // Set the fetched teacher data in state
      } catch (error) {
        console.error(
          "Error fetching teacher data:",
          error.response?.data || error.message
        );
      }
    };

    fetchTeacher();
  }, []);

  const handleAddHomework = () => {
    navigate("/manage-homework"); // Navigate to the ManageHomework page
  };

  const handleAddBetyg = () => {
    navigate("/betyg"); // Navigate to the ManageBetyg page
  };

  const handleAddMeddelanden = () => {
    navigate("/manage-meddelanden"); // Navigate to the ManageMeddelanden page
  };

  const handleAddRecommendedResource = () => {
    navigate("/manage-recommended-resource"); // Navigate to the ManageRecommendedResource page
  };

  const handleAddFiluppladdning = () => {
    navigate("/manage-filuppladdning"); // Navigate to the ManageFiluppladdning page
  };

  return (
    <div className="container mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold mb-6">Teacher Dashboard</h1>

      {/* Display the teacher's name */}
      {teacher ? (
        <p className="text-lg mb-6">
          Welcome,{" "}
          <span className="font-semibold">
            {teacher.user.first_name} {teacher.user.last_name}
          </span>
          !
        </p>
      ) : (
        <p className="text-lg mb-6">Loading teacher information...</p>
      )}

      <div className="grid grid-cols-3 gap-6">
        <div className="bg-blue-100 p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Manage Homework</h2>
          <button
            onClick={handleAddHomework}
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
          >
            Add Homework
          </button>
        </div>

        <div className="bg-green-100 p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Manage Betyg</h2>
          <button
            onClick={handleAddBetyg}
            className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
          >
            Add Betyg
          </button>
        </div>

        <div className="bg-yellow-100 p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Manage Meddelanden</h2>
          <button
            onClick={handleAddMeddelanden}
            className="bg-yellow-500 text-white px-4 py-2 rounded-md hover:bg-yellow-600"
          >
            Add Meddelanden
          </button>
        </div>

        <div className="bg-purple-100 p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">
            Manage Recommended Resources
          </h2>
          <button
            onClick={handleAddRecommendedResource}
            className="bg-purple-500 text-white px-4 py-2 rounded-md hover:bg-purple-600"
          >
            Add Recommended Resource
          </button>
        </div>

        <div className="bg-red-100 p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Manage Filuppladdning</h2>
          <button
            onClick={handleAddFiluppladdning}
            className="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
          >
            Add Filuppladdning
          </button>
        </div>
      </div>
    </div>
  );
};

export default Teachers;
