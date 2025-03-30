import React, { useEffect, useState } from "react";
import axios from "axios";

const BetygPage = ({ userId }) => {
  const [betygList, setBetygList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editingBetyg, setEditingBetyg] = useState(null); // State for editing betyg
  const [updatedBetyg, setUpdatedBetyg] = useState({
    grade: "",
    comments: "",
    feedback: "",
  }); // State for updated betyg
  const [newBetyg, setNewBetyg] = useState({
    grade: "",
    comments: "",
    feedback: "",
    homework_id: "",
  }); // State for adding new betyg

  useEffect(() => {
    const token = localStorage.getItem("token"); // Retrieve the token from localStorage

    const fetchBetyg = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/betyg/user/${userId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`, // Include the token
            },
          }
        );
        setBetygList(response.data);
        setLoading(false);
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to fetch grades");
        setLoading(false);
      }
    };

    fetchBetyg();
  }, [userId]);

  // Handle delete betyg
  const handleDelete = async (betygId) => {
    const token = localStorage.getItem("token");
    try {
      await axios.delete(`http://127.0.0.1:8000/betyg/${betygId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setBetygList((prevList) =>
        prevList.filter((betyg) => betyg.id !== betygId)
      );
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to delete betyg");
    }
  };

  // Handle edit betyg
  const handleEdit = (betyg) => {
    setEditingBetyg(betyg.id);
    setUpdatedBetyg({
      grade: betyg.grade,
      comments: betyg.comments,
      feedback: betyg.feedback,
    });
  };

  // Handle update betyg
  const handleUpdate = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    try {
      const response = await axios.put(
        `http://127.0.0.1:8000/betyg/${editingBetyg}`,
        updatedBetyg,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setBetygList((prevList) =>
        prevList.map((betyg) =>
          betyg.id === editingBetyg ? response.data : betyg
        )
      );
      setEditingBetyg(null);
      setUpdatedBetyg({ grade: "", comments: "", feedback: "" });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to update betyg");
    }
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    // Validate the data
    if (
      !newBetyg.grade ||
      !newBetyg.comments ||
      !newBetyg.feedback ||
      !newBetyg.homework_id
    ) {
      setError("All fields are required.");
      return;
    }

    console.log("Payload being sent:", {
      grade: newBetyg.grade,
      comments: newBetyg.comments,
      feedback: newBetyg.feedback,
      homework_id: Number(newBetyg.homework_id),
      user_id: userId, // Use userId passed as a prop
    });

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/betyg/",
        {
          grade: newBetyg.grade,
          comments: newBetyg.comments,
          feedback: newBetyg.feedback,
          homework_id: Number(newBetyg.homework_id), // Ensure homework_id is a number
          user_id: userId, // Use userId passed as a prop
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setBetygList((prevList) => [...prevList, response.data]);
      setNewBetyg({ grade: "", comments: "", feedback: "", homework_id: "" });
      setError(""); // Clear any previous errors
    } catch (err) {
      console.error("Error adding betyg:", err.response?.data || err.message);
      setError(err.response?.data?.detail || "Failed to add betyg");
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return (
      <div className="text-red-500">
        {typeof error === "string"
          ? error
          : error.msg || error.detail || "An unknown error occurred"}
      </div>
    );
  }

  return (
    <div className="p-6 bg-white rounded shadow-md">
      <h2 className="text-2xl font-bold mb-4">Betyg</h2>

      {/* Add New Betyg Form */}
      <form onSubmit={handleAdd} className="mb-6">
        <h3 className="text-xl font-bold mb-4">Add New Betyg</h3>
        <div className="mb-4">
          <label htmlFor="grade" className="block text-gray-700 font-semibold">
            Grade
          </label>
          <input
            type="text"
            id="grade"
            name="grade"
            value={newBetyg.grade}
            onChange={(e) =>
              setNewBetyg({ ...newBetyg, grade: e.target.value })
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="comments"
            className="block text-gray-700 font-semibold"
          >
            Comments
          </label>
          <textarea
            id="comments"
            name="comments"
            value={newBetyg.comments}
            onChange={(e) =>
              setNewBetyg({ ...newBetyg, comments: e.target.value })
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="feedback"
            className="block text-gray-700 font-semibold"
          >
            Feedback
          </label>
          <textarea
            id="feedback"
            name="feedback"
            value={newBetyg.feedback}
            onChange={(e) =>
              setNewBetyg({ ...newBetyg, feedback: e.target.value })
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="homework_id"
            className="block text-gray-700 font-semibold"
          >
            Homework ID
          </label>
          <input
            type="number"
            id="homework_id"
            name="homework_id"
            value={newBetyg.homework_id}
            onChange={(e) =>
              setNewBetyg({ ...newBetyg, homework_id: e.target.value })
            }
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
        >
          Add Betyg
        </button>
      </form>

      {/* Existing Betyg List */}
      {betygList.length === 0 ? (
        <p className="text-gray-600">Inga betyg att visa.</p>
      ) : (
        <ul className="space-y-4">
          {betygList.map((betyg) => (
            <li
              key={betyg.id}
              className="p-4 border rounded bg-gray-100 hover:bg-gray-200 transition"
            >
              <h3 className="text-lg font-semibold">Grade: {betyg.grade}</h3>
              <p className="text-gray-700">Comments: {betyg.comments}</p>
              <p className="text-gray-700">Feedback: {betyg.feedback}</p>
              <p className="text-sm text-gray-500">
                Homework ID: {betyg.homework_id}
              </p>
              <div className="mt-2 space-x-2">
                <button
                  onClick={() => handleEdit(betyg)}
                  className="text-blue-500 hover:text-blue-700"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(betyg.id)}
                  className="text-red-500 hover:text-red-700"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {/* Update Form */}
      {editingBetyg && (
        <form onSubmit={handleUpdate} className="mt-6">
          <h3 className="text-xl font-bold mb-4">Update Betyg</h3>
          <div className="mb-4">
            <label
              htmlFor="grade"
              className="block text-gray-700 font-semibold"
            >
              Grade
            </label>
            <input
              type="text"
              id="grade"
              name="grade"
              value={updatedBetyg.grade}
              onChange={(e) =>
                setUpdatedBetyg({ ...updatedBetyg, grade: e.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="comments"
              className="block text-gray-700 font-semibold"
            >
              Comments
            </label>
            <textarea
              id="comments"
              name="comments"
              value={updatedBetyg.comments}
              onChange={(e) =>
                setUpdatedBetyg({ ...updatedBetyg, comments: e.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="feedback"
              className="block text-gray-700 font-semibold"
            >
              Feedback
            </label>
            <textarea
              id="feedback"
              name="feedback"
              value={updatedBetyg.feedback}
              onChange={(e) =>
                setUpdatedBetyg({ ...updatedBetyg, feedback: e.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
          >
            Update
          </button>
        </form>
      )}
    </div>
  );
};

export default BetygPage;
