import React, { useState, useEffect } from "react";
import axios from "axios";

const ManageHomework = () => {
  const [homeworks, setHomeworks] = useState([]); // State for the list of homework
  const [subjects, setSubjects] = useState([]);

  const [teachers, setTeachers] = useState([]); // State for the list of teachers
  const [arskursList, setArskursList] = useState([]); // State for the list of årskurs
  const [homeworkData, setHomeworkData] = useState({
    title: "",
    description: "",
    due_date: "",
    status: "Pending",
    priority: "Normal",
    user_id: "",
    subject_id: "",
    teacher_id: "",
    arskurs_id: "", // Add arskurs_id to the state
  });
  const [assignmentType, setAssignmentType] = useState("single");
  const [editingHomeworkId, setEditingHomeworkId] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  // Fetch teachers from the backend
  useEffect(() => {
    const fetchTeachers = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/teachers/names/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setTeachers(response.data);
      } catch (error) {
        console.error("Error fetching teachers:", error);
        setErrorMessage("Failed to fetch teacher data.");
      }
    };
    fetchTeachers();
  }, []);

  // Fetch årskurs from the backend
  useEffect(() => {
    const fetchArskurs = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await axios.get("http://127.0.0.1:8000/arskurs/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setArskursList(response.data);
      } catch (error) {
        console.error("Error fetching årskurs:", error);
        setErrorMessage("Failed to fetch årskurs data.");
      }
    };
    fetchArskurs();
  }, []);

  // Fetch homework from the backend
  useEffect(() => {
    const fetchHomeworks = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await axios.get("http://localhost:8000/homeworks/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setHomeworks(response.data);
      } catch (error) {
        console.error("Error fetching homeworks:", error);
        setErrorMessage("Failed to fetch homework data.");
      }
    };

    fetchHomeworks();
  }, []);
  // Fetch subjects from the backend
  useEffect(() => {
    const fetchSubjects = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await axios.get("http://127.0.0.1:8000/subjects/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setSubjects(response.data); // Set the fetched subjects in state
      } catch (error) {
        console.error("Error fetching subjects:", error);
        setErrorMessage("Failed to fetch subjects.");
      }
    };
    fetchSubjects();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate required fields
    if (
      !homeworkData.title ||
      !homeworkData.description ||
      !homeworkData.due_date ||
      !homeworkData.subject_id ||
      (assignmentType === "single" && !homeworkData.user_id) || // Validate user_id only for single assignment
      (assignmentType === "all" && !homeworkData.arskurs_id) // Validate arskurs_id only for all årskurs
    ) {
      setErrorMessage("All fields are required.");
      return;
    }

    try {
      const token = localStorage.getItem("token");

      // Prepare the payload based on assignment type
      const payload = {
        title: homeworkData.title,
        description: homeworkData.description,
        due_date: homeworkData.due_date,
        status: homeworkData.status,
        priority: homeworkData.priority,
        subject_id: homeworkData.subject_id,
        teacher_id: homeworkData.teacher_id,
        ...(assignmentType === "single" && { user_id: homeworkData.user_id }), // Include user_id only if single
        ...(assignmentType === "all" && {
          arskurs_id: homeworkData.arskurs_id,
        }), // Include arskurs_id only if all
      };

      console.log("Payload:", payload); // Debugging log

      if (editingHomeworkId) {
        // Update homework
        const response = await axios.put(
          `http://localhost:8000/homeworks/${editingHomeworkId}/`,
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`,
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
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`,
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
        teacher_id: "",
        arskurs_id: "",
      });
      setEditingHomeworkId(null);
    } catch (error) {
      console.error(
        "Error managing homework:",
        error.response?.data || error.message
      );
      if (error.response?.data) {
        setErrorMessage(`Error: ${JSON.stringify(error.response.data)}`);
      } else {
        setErrorMessage("Failed to manage homework. Please try again.");
      }
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
      teacher_id: homework.teacher_id,
      arskurs_id: homework.arskurs_id,
    });
    setEditingHomeworkId(homework.id); // Ensure this is set correctly
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
        {/* Assignment Type Toggle */}
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-2">
            Assign To
          </label>
          <div className="flex items-center space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                name="assignmentType"
                value="single"
                checked={assignmentType === "single"}
                onChange={() => setAssignmentType("single")}
                className="mr-2"
              />
              Single Student
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                name="assignmentType"
                value="all"
                checked={assignmentType === "all"}
                onChange={() => setAssignmentType("all")}
                className="mr-2"
              />
              All Årskurs
            </label>
          </div>
        </div>

        {/* Conditionally Render Fields */}
        {assignmentType === "single" && (
          <div className="mb-4">
            <label
              htmlFor="user_id"
              className="block text-gray-700 font-semibold"
            >
              Student ID
            </label>
            <input
              type="number"
              id="user_id"
              name="user_id"
              value={homeworkData.user_id}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter Student ID"
            />
          </div>
        )}

        {assignmentType === "all" && (
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
              value={homeworkData.arskurs_id}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Årskurs</option>
              {arskursList.map((arskurs) => (
                <option key={arskurs.id} value={arskurs.id}>
                  {arskurs.name}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Other Form Fields */}
        <div className="mb-4">
          <label
            htmlFor="subject_id"
            className="block text-gray-700 font-semibold"
          >
            Subject
          </label>
          <select
            id="subject_id"
            name="subject_id"
            value={homeworkData.subject_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select a subject</option>
            {subjects.map((subject) => (
              <option key={subject.id} value={subject.id}>
                {subject.name}
              </option>
            ))}
          </select>
        </div>
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

        {/* Error and success messages */}
        {errorMessage && (
          <p className="text-red-500 text-sm mb-4">{errorMessage}</p>
        )}
        {successMessage && (
          <p className="text-green-500 text-sm mb-4">{successMessage}</p>
        )}

        {/* Submit button */}
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
