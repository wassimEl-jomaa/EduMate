import React, { useState, useEffect } from "react";
import axios from "axios";

const ShowAllHomework = () => {
  const [studentHomeworks, setStudentHomeworks] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false); // Modal visibility state
  const [editingHomework, setEditingHomework] = useState(null); // Homework being edited
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    due_date: "",
    priority: "Normal",
    status: "Pending",
  });

  const fetchStudentHomeworks = async () => {
    const token = localStorage.getItem("token");

    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/student_homeworks",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setStudentHomeworks(response.data);
    } catch (error) {
      console.error("Error fetching student homeworks:", error);
      setErrorMessage("Failed to fetch student homeworks.");
    }
  };
  useEffect(() => {
    fetchStudentHomeworks();
  }, []);

  const handleEdit = (studentHomework) => {
    // Populate the modal with the selected homework's data
    setEditingHomework(studentHomework);
    setFormData({
      title: studentHomework.homework?.title || "",
      description: studentHomework.homework?.description || "",
      due_date: studentHomework.homework?.due_date || "",
      priority: studentHomework.homework?.priority || "Normal",
      status: studentHomework.homework?.status || "Pending",
    });
    setIsModalOpen(true); // Open the modal
  };

  const handleDelete = (id) => {
    const delete_homework = async () => {
      const token = localStorage.getItem("token");

      try {
        await axios.delete(`http://127.0.0.1:8000/student_homeworks/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert(`Delete Student Homework ID`);
        fetchStudentHomeworks();
      } catch (error) {
        console.error("Error fetching student homeworks:", error);
        setErrorMessage("Failed to fetch student homeworks.");
      }
    };
    delete_homework();
  };

  const handleModalSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    try {
      await axios.put(
        `http://127.0.0.1:8000/homework/${editingHomework.homework.id}/`,
        formData,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setIsModalOpen(false); // Close the modal
      setEditingHomework(null);
      fetchStudentHomeworks(); // Refresh the list
    } catch (error) {
      console.error("Error updating homework:", error);
      setErrorMessage("Failed to update homework.");
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-xl border border-gray-200">
      <h2 className="text-3xl font-semibold text-gray-700 mb-6">
        Show Homework
      </h2>

      {errorMessage && (
        <p className="text-red-500 text-sm mb-4">{errorMessage}</p>
      )}

      <h2 className="text-2xl font-bold mt-8 mb-6">Existing Homework</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-300 rounded-lg">
          <thead className="bg-gray-50">
            <tr>
              <th className="py-3 px-6 border-b text-left text-gray-700 font-semibold">
                Student Name
              </th>
              <th className="py-3 px-6 border-b text-left text-gray-700 font-semibold">
                Title
              </th>
              <th className="py-3 px-6 border-b text-left text-gray-700 font-semibold">
                Description
              </th>
              <th className="py-3 px-6 border-b text-left text-gray-700 font-semibold">
                Due Date
              </th>
              <th className="py-3 px-6 border-b text-left text-gray-700 font-semibold">
                Status
              </th>
              <th className="py-3 px-6 border-b text-left text-gray-700 font-semibold">
                Teacher
              </th>
              <th className="py-3 px-6 border-b text-left text-gray-700 font-semibold">
                Subject
              </th>
              <th className="py-3 px-6 border-b text-left text-gray-700 font-semibold">
                Class Level
              </th>
              <th className="py-3 px-6 border-b text-left text-gray-700 font-semibold">
                Grade
              </th>
              <th className="py-3 px-6 border-b text-left text-gray-700 font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {studentHomeworks.map((studentHomework) => (
              <tr key={studentHomework.id} className="hover:bg-gray-100">
                {/* Student Name */}
                <td className="py-3 px-6 border-b">
                  {studentHomework.student?.user?.first_name &&
                  studentHomework.student?.user?.last_name
                    ? `${studentHomework.student.user.first_name} ${studentHomework.student.user.last_name}`
                    : "N/A"}
                </td>

                {/* Homework Title */}
                <td className="py-3 px-6 border-b">
                  {studentHomework.homework?.title || "N/A"}
                </td>

                {/* Homework Description */}
                <td className="py-3 px-6 border-b">
                  {studentHomework.homework?.description || "N/A"}
                </td>

                {/* Homework Due Date */}
                <td className="py-3 px-6 border-b">
                  {studentHomework.homework?.due_date || "N/A"}
                </td>

                {/* Homework Status */}
                <td className="py-3 px-6 border-b">
                  {studentHomework.homework?.status || "N/A"}
                </td>

                {/* Teacher Name */}
                <td className="py-3 px-6 border-b">
                  {studentHomework.homework?.subject_class_level?.teacher?.user
                    ?.first_name &&
                  studentHomework.homework?.subject_class_level?.teacher?.user
                    ?.last_name
                    ? `${studentHomework.homework.subject_class_level.teacher.user.first_name} ${studentHomework.homework.subject_class_level.teacher.user.last_name}`
                    : "N/A"}
                </td>

                {/* Subject Name */}
                <td className="py-3 px-6 border-b">
                  {studentHomework.homework?.subject_class_level?.subject
                    ?.name || "N/A"}
                </td>

                {/* Class Level Name */}
                <td className="py-3 px-6 border-b">
                  {studentHomework.student?.class_level?.name ||
                    studentHomework.homework?.subject_class_level?.class_level
                      ?.name ||
                    "N/A"}
                </td>

                {/* Grade */}
                <td className="py-3 px-6 border-b">
                  {studentHomework.grade || "Not Graded"}
                </td>

                {/* Actions */}
                <td className="py-3 px-6 border-b">
                  <button
                    onClick={() => handleEdit(studentHomework)}
                    className="text-blue-500 hover:text-blue-700 mr-4"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(studentHomework.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-8 rounded-lg shadow-lg w-1/2">
            <h2 className="text-2xl font-bold mb-4">Edit Homework</h2>
            <form onSubmit={handleModalSubmit}>
              <div className="mb-4">
                <label
                  htmlFor="title"
                  className="block text-gray-700 font-semibold mb-2"
                >
                  Title
                </label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="mb-4">
                <label
                  htmlFor="description"
                  className="block text-gray-700 font-semibold mb-2"
                >
                  Description
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                ></textarea>
              </div>

              <div className="mb-4">
                <label
                  htmlFor="due_date"
                  className="block text-gray-700 font-semibold mb-2"
                >
                  Due Date
                </label>
                <input
                  type="date"
                  id="due_date"
                  name="due_date"
                  value={formData.due_date}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="mb-4">
                <label
                  htmlFor="priority"
                  className="block text-gray-700 font-semibold mb-2"
                >
                  Priority
                </label>
                <select
                  id="priority"
                  name="priority"
                  value={formData.priority}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Normal">Normal</option>
                  <option value="High">High</option>
                  <option value="Low">Low</option>
                </select>
              </div>

              <div className="mb-4">
                <label
                  htmlFor="status"
                  className="block text-gray-700 font-semibold mb-2"
                >
                  Status
                </label>
                <select
                  id="status"
                  name="status"
                  value={formData.status}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Pending">Pending</option>
                  <option value="Completed">Completed</option>
                  <option value="In Progress">In Progress</option>
                </select>
              </div>

              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 bg-gray-500 text-white rounded-md"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-500 text-white rounded-md"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ShowAllHomework;
