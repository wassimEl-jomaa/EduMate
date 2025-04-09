import React, { useState, useEffect } from "react";
import axios from "axios";

const ShowAllHomework = () => {
  const [studentHomeworks, setStudentHomeworks] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
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

    fetchStudentHomeworks();
  }, []);

  const handleEdit = (studentHomework) => {
    alert(`Edit Student Homework ID: ${studentHomework.id}`);
  };

  const handleDelete = (id) => {
    alert(`Delete Student Homework ID: ${id}`);
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
    </div>
  );
};

export default ShowAllHomework;
