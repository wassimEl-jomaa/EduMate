import React from "react";

const TeacherCard = ({ teacher, onEdit, onDelete }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-4">
      <h3 className="text-xl font-bold">{teacher.name}</h3>
      <p className="text-gray-700">Subject: {teacher.subject}</p>
      <div className="mt-4">
        <button
          onClick={() => onEdit(teacher.id)}
          className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 mr-2"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(teacher.id)}
          className="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TeacherCard;
