import React from "react";
import { useNavigate } from "react-router-dom";

import { FaPlus, FaListUl } from "react-icons/fa";

const ManageHomework = () => {
  const navigate = useNavigate();

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-10 py-10">
      <h1 className="text-5xl font-extrabold text-gray-900 mb-12 text-center tracking-tight leading-snug">
        📝 Homework Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
        {/* Single Student Homework Card */}
        <div className="bg-white p-8 rounded-2xl shadow-2xl border border-blue-100 hover:shadow-blue-200 transition-shadow duration-300">
          <h2 className="text-2xl font-bold text-blue-700 mb-6">
            📘 Student-Specific Homework
          </h2>

          <div className="space-y-5">
            <button
              onClick={() => navigate("/add-homework")}
              className="w-full flex items-center justify-center gap-2 py-3 px-6 bg-gradient-to-r from-blue-600 to-blue-500 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-blue-600 transition duration-300 shadow-md hover:shadow-lg"
            >
              <FaPlus /> Add Homework
            </button>
            <button
              onClick={() => navigate("/homeworks")}
              className="w-full flex items-center justify-center gap-2 py-3 px-6 bg-gradient-to-r from-blue-600 to-blue-500 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-blue-600 transition duration-300 shadow-md hover:shadow-lg"
            >
              <FaListUl /> View / Update / Delete Homework
            </button>
          </div>
        </div>

        {/* Class Level Homework Card */}
        <div className="bg-white p-8 rounded-2xl shadow-2xl border border-blue-100 hover:shadow-blue-200 transition-shadow duration-300">
          <h2 className="text-2xl font-bold text-blue-700 mb-6">
            🏫 Class-Level Homework
          </h2>

          <div className="space-y-5">
            <button
              onClick={() => navigate("/add-class-homework")}
              className="w-full flex items-center justify-center gap-2 py-3 px-6 bg-gradient-to-r from-blue-600 to-blue-500 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-blue-600 transition duration-300 shadow-md hover:shadow-lg"
            >
              <FaPlus /> Add Homework
            </button>
            <button
              onClick={() => navigate("/class-homeworks")}
              className="w-full flex items-center justify-center gap-2 py-3 px-6 bg-gradient-to-r from-blue-600 to-blue-500 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-blue-600 transition duration-300 shadow-md hover:shadow-lg"
            >
              <FaListUl /> View / Update / Delete Homework
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ManageHomework;
