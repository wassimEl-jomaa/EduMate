import React, { useState, useEffect } from "react";
import axios from "axios";

const ManageHomework = () => {
  const [homeworks, setHomeworks] = useState([]); // State for the list of homework
  const [teachers, setTeachers] = useState([]);
  const [homeworkData, setHomeworkData] = useState({
    title: "",
    description: "",
    due_date: "",
    status: "Pending",
    priority: "Normal",
    user_id: "",
    subject_id: "",
    teacher_name: "",
  }); // State for homework data
  const [editingHomeworkId, setEditingHomeworkId] = useState(null); // State for editing homework ID
  const [successMessage, setSuccessMessage] = useState(""); // State for success message
  const [errorMessage, setErrorMessage] = useState(""); // State for error message
  // Fetch teachers from the backend
  useEffect(() => {
    const fetchTeachers = async () => {
      const token = localStorage.getItem("token"); // Retrieve the token from localStorage
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/teachers/names/",
          {
            headers: {
              Authorization: `Bearer ${token}`, // Include the token
            },
          }
        );
        setTeachers(response.data); // Ensure teacher_name is part of the response
      } catch (error) {
        console.error("Error fetching teachers:", error);
        setErrorMessage("Failed to fetch teacher data.");
      }
    };
    fetchTeachers();
  }, []); // Fetch teachers when the component mounts
  // Fetch homework from the backend
  useEffect(() => {
    const fetchHomeworks = async () => {
      const token = localStorage.getItem("token"); // Retrieve the token from localStorage
      try {
        const response = await axios.get("http://localhost:8000/homeworks/", {
          headers: {
            Authorization: `Bearer ${token}`, // Include the token
          },
        });
        setHomeworks(response.data); // Ensure teacher_name is part of the response
      } catch (error) {
        console.error("Error fetching homeworks:", error);
        setErrorMessage("Failed to fetch homework data.");
      }
    };

    fetchHomeworks();
  }, []);
  // Add or update homework
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate required fields
    if (
      !homeworkData.title ||
      !homeworkData.description ||
      !homeworkData.due_date ||
      !homeworkData.user_id ||
      !homeworkData.subject_id
    ) {
      setErrorMessage("All fields are required.");
      return;
    }

    try {
      const token = localStorage.getItem("token"); // Retrieve the token from localStorage
      if (editingHomeworkId) {
        // Update homework
        const response = await axios.put(
          `http://localhost:8000/homeworks/${editingHomeworkId}/`,
          homeworkData,
          {
            headers: {
              Authorization: `Bearer ${token}`, // Include the token
            },
          }
        );
        setHomeworks((prevHomeworks) =>
          prevHomeworks.map((homework) =>
            homework.id === editingHomeworkId ? response.data : homework
          )
        );
        setSuccessMessage("Homework updated successfully!");
      } else {
        // Add new homework
        const response = await axios.post(
          "http://localhost:8000/homeworks/",
          homeworkData,
          {
            headers: {
              Authorization: `Bearer ${token}`, // Include the token
            },
          }
        );
        setHomeworks((prevHomeworks) => [...prevHomeworks, response.data]);
        setSuccessMessage("Homework added successfully!");
      }

      // Reset form and state
      setErrorMessage("");
      setHomeworkData({
        title: "",
        description: "",
        due_date: "",
        status: "Pending",
        priority: "Normal",
        user_id: "",
        subject_id: "",
      });
      setEditingHomeworkId(null);
    } catch (error) {
      console.error(
        "Error managing homework:",
        error.response?.data || error.message
      );
      setErrorMessage("Failed to manage homework. Please try again.");
      setSuccessMessage("");
    }
  };

  // Delete homework
  const handleDelete = async (homeworkId) => {
    const token = localStorage.getItem("token"); // Retrieve the token from localStorage
    try {
      await axios.delete(`http://localhost:8000/homeworks/${homeworkId}/`, {
        headers: {
          Authorization: `Bearer ${token}`, // Include the token
        },
      });
      setHomeworks((prevHomeworks) =>
        prevHomeworks.filter((homework) => homework.id !== homeworkId)
      );
      setSuccessMessage("Homework deleted successfully!");
      setErrorMessage("");
    } catch (error) {
      console.error(
        "Error deleting homework:",
        error.response?.data || error.message
      );
      setErrorMessage("Failed to delete homework. Please try again.");
      setSuccessMessage("");
    }
  };

  // Start editing homework
  const handleEdit = (homework) => {
    setHomeworkData({
      title: homework.title,
      description: homework.description,
      due_date: homework.due_date,
      status: homework.status,
      priority: homework.priority,
      user_id: homework.user_id,
      subject_id: homework.subject_id,
    });
    setEditingHomeworkId(homework.id);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setHomeworkData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="max-w-lg mx-auto bg-white p-8 border rounded-lg shadow-md mt-10">
      <h1 className="text-2xl font-bold mb-6">Manage Homework</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="title" className="block text-gray-700 font-semibold">
            Title
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={homeworkData.title}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter title"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="description"
            className="block text-gray-700 font-semibold"
          >
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={homeworkData.description}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter description"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="due_date"
            className="block text-gray-700 font-semibold"
          >
            Due Date
          </label>
          <input
            type="date"
            id="due_date"
            name="due_date"
            value={homeworkData.due_date}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="status" className="block text-gray-700 font-semibold">
            Status
          </label>
          <select
            id="status"
            name="status"
            value={homeworkData.status}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="Pending">Pending</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
          </select>
        </div>
        <div className="mb-4">
          <label
            htmlFor="priority"
            className="block text-gray-700 font-semibold"
          >
            Priority
          </label>
          <select
            id="priority"
            name="priority"
            value={homeworkData.priority}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="Normal">Normal</option>
            <option value="High">High</option>
            <option value="Low">Low</option>
          </select>
        </div>
        <div className="mb-4">
          <label
            htmlFor="user_id"
            className="block text-gray-700 font-semibold"
          >
            Student_id
          </label>
          <input
            type="number"
            id="user_id"
            name="user_id"
            value={homeworkData.user_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter Student  ID"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="teacher_id"
            className="block text-gray-700 font-semibold"
          >
            Teacher
          </label>
          <select
            id="teacher_id"
            name="teacher_id"
            value={homeworkData.teacher_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select a teacher</option>
            {teachers.map((teacher) => (
              <option key={teacher.id} value={teacher.id}>
                {teacher.first_name} {teacher.last_name}
              </option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label
            htmlFor="subject_id"
            className="block text-gray-700 font-semibold"
          >
            Subject ID
          </label>
          <input
            type="number"
            id="subject_id"
            name="subject_id"
            value={homeworkData.subject_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter subject ID"
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
          {editingHomeworkId ? "Update Homework" : "Add Homework"}
        </button>
      </form>

      <h2 className="text-xl font-bold mt-8 mb-4">Existing Homework</h2>
      <ul className="space-y-4">
        {homeworks.map((homework) => (
          <li
            key={homework.id}
            className="flex justify-between items-center bg-gray-100 p-4 rounded-md"
          >
            <span>
              {homework.title} (Due: {homework.due_date})
            </span>
            <div className="space-x-2">
              <button
                onClick={() => handleEdit(homework)}
                className="text-blue-500 hover:text-blue-700"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(homework.id)}
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

export default ManageHomework;
