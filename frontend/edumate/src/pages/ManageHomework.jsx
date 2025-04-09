import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const ManageHomework = () => {
  const navigate = useNavigate();

  return (
    <div className="container mx-auto px-6 py-10">
      <h1 className="text-4xl font-extrabold text-gray-800 mb-8 text-center tracking-wide leading-tight">
        HomeWork Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-8">
        {/* Student Section */}
        <div className="bg-white p-6 rounded-lg shadow-xl border border-blue-200">
          <h2 className="text-2xl font-semibold text-blue-700 mb-6">
            Homework for one student
          </h2>

          <div className="space-y-4">
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Add Homework
            </button>
            <button
              onClick={() => navigate("/homeworks")}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Show All Homework
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-green-600 text-white rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get Homework by class Level
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-yellow-600 text-white rounded-md hover:bg-yellow-700 focus:ring-2 focus:ring-yellow-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get homework by Teacher
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-orange-600 text-white rounded-md hover:bg-orange-700 focus:ring-2 focus:ring-orange-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Update a Homework
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-red-600 text-white rounded-md hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Delete a Homework
            </button>
          </div>
        </div>

        {/* Parents Section */}
        <div className="bg-white p-6 rounded-lg shadow-xl border border-blue-200">
          <h2 className="text-2xl font-semibold text-blue-700 mb-6">
            Homework for Class Level
          </h2>

          <div className="space-y-4">
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Add Homework
            </button>
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get all Homework
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-green-600 text-white rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get Homeworks by class Level
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-yellow-600 text-white rounded-md hover:bg-yellow-700 focus:ring-2 focus:ring-yellow-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get Homeworks by Teacher
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-orange-600 text-white rounded-md hover:bg-orange-700 focus:ring-2 focus:ring-orange-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Update a Homework
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-red-600 text-white rounded-md hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Delete a Homework
            </button>
          </div>
        </div>

        {/* Teachers Section */}
        <div className="bg-white p-6 rounded-lg shadow-xl border border-blue-200">
          <h2 className="text-2xl font-semibold text-blue-700 mb-6">
            Homeworks
          </h2>

          <div className="space-y-4">
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            ></button>
            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get all Homeworks by Subject
            </button>

            <button
              onClick={() => {}}
              className="w-full py-3 px-6 bg-yellow-600 text-white rounded-md hover:bg-yellow-700 focus:ring-2 focus:ring-yellow-500 focus:outline-none transition transform hover:scale-105 duration-300"
            >
              Get Teachers by Student Name
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ManageHomework;
