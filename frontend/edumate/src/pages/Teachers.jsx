import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import TeacherCard from "../components/TeacherCard";

const Teachers = () => {
  const [homework, setHomework] = useState([]);
  const [betyg, setBetyg] = useState([]);
  const [meddelanden, setMeddelanden] = useState([]);
  const navigate = useNavigate(); // Initialize the navigate function

  const handleAddHomework = () => {
    // Navigate to the ManageHomework page
    navigate("/manage-homework");
  };

  const handleAddBetyg = () => {
    // Navigate to the ManageBetyg page
    navigate("/betyg");
  };

  const handleAddMeddelanden = () => {
    // Navigate to the ManageBetyg page
    navigate("/meddelande");
  };

  return (
    <div className="container mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold mb-6">Teacher Dashboard</h1>

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
      </div>

      <div className="mt-10">
        <h2 className="text-2xl font-bold mb-4">Teachers</h2>
        <TeacherCard
          teacher={{ name: "John Doe", subject: "Mathematics" }}
          onEdit={(id) => alert(`Edit teacher with ID: ${id}`)}
          onDelete={(id) => alert(`Delete teacher with ID: ${id}`)}
        />
      </div>
    </div>
  );
};

export default Teachers;
