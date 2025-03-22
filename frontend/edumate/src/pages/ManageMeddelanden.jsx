import React, { useState, useEffect } from "react";
import axios from "axios";

const ManageMeddelanden = () => {
  const [meddelanden, setMeddelanden] = useState([]); // State for the list of messages
  const [meddelandeData, setMeddelandeData] = useState({
    message: "",
    description: "",
    read_status: "Unread",
    homework_id: "",
  }); // State for message data
  const [editingMeddelandeId, setEditingMeddelandeId] = useState(null); // State for editing message ID
  const [successMessage, setSuccessMessage] = useState(""); // State for success message
  const [errorMessage, setErrorMessage] = useState(""); // State for error message

  // Fetch messages from the backend
  useEffect(() => {
    const fetchMeddelanden = async () => {
      try {
        const response = await axios.get("http://localhost:8000/meddelanden/");
        setMeddelanden(response.data);
      } catch (error) {
        console.error("Error fetching meddelanden:", error);
      }
    };

    fetchMeddelanden();
  }, []);

  // Add or update a message
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!meddelandeData.message || !meddelandeData.homework_id) {
      setErrorMessage("Message and Homework ID are required.");
      return;
    }

    try {
      if (editingMeddelandeId) {
        // Update message
        const response = await axios.put(
          `http://localhost:8000/meddelanden/${editingMeddelandeId}/`,
          meddelandeData
        );
        setMeddelanden((prevMeddelanden) =>
          prevMeddelanden.map((meddelande) =>
            meddelande.id === editingMeddelandeId ? response.data : meddelande
          )
        );
        setSuccessMessage("Message updated successfully!");
      } else {
        // Add new message
        const response = await axios.post(
          "http://localhost:8000/meddelanden/",
          meddelandeData
        );
        setMeddelanden((prevMeddelanden) => [
          ...prevMeddelanden,
          response.data,
        ]);
        setSuccessMessage("Message added successfully!");
      }

      setErrorMessage("");
      setMeddelandeData({
        message: "",
        description: "",
        read_status: "Unread",
        homework_id: "",
      });
      setEditingMeddelandeId(null);
    } catch (error) {
      console.error(
        "Error managing meddelande:",
        error.response?.data || error.message
      );
      setErrorMessage("Failed to manage message. Please try again.");
      setSuccessMessage("");
    }
  };

  // Delete a message
  const handleDelete = async (meddelandeId) => {
    try {
      await axios.delete(`http://localhost:8000/meddelanden/${meddelandeId}/`);
      setMeddelanden((prevMeddelanden) =>
        prevMeddelanden.filter((meddelande) => meddelande.id !== meddelandeId)
      );
      setSuccessMessage("Message deleted successfully!");
      setErrorMessage("");
    } catch (error) {
      console.error(
        "Error deleting meddelande:",
        error.response?.data || error.message
      );
      setErrorMessage("Failed to delete message. Please try again.");
      setSuccessMessage("");
    }
  };

  // Start editing a message
  const handleEdit = (meddelande) => {
    setMeddelandeData({
      message: meddelande.message,
      description: meddelande.description,
      read_status: meddelande.read_status,
      homework_id: meddelande.homework_id,
    });
    setEditingMeddelandeId(meddelande.id);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setMeddelandeData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="max-w-lg mx-auto bg-white p-8 border rounded-lg shadow-md mt-10">
      <h1 className="text-2xl font-bold mb-6">Manage Meddelanden</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label
            htmlFor="message"
            className="block text-gray-700 font-semibold"
          >
            Message
          </label>
          <textarea
            id="message"
            name="message"
            value={meddelandeData.message}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter message"
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
            value={meddelandeData.description}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter description"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="read_status"
            className="block text-gray-700 font-semibold"
          >
            Read Status
          </label>
          <select
            id="read_status"
            name="read_status"
            value={meddelandeData.read_status}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="Unread">Unread</option>
            <option value="Read">Read</option>
          </select>
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
            value={meddelandeData.homework_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter homework ID"
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
          {editingMeddelandeId ? "Update Message" : "Add Message"}
        </button>
      </form>

      <h2 className="text-xl font-bold mt-8 mb-4">Existing Messages</h2>
      <ul className="space-y-4">
        {meddelanden.map((meddelande) => (
          <li
            key={meddelande.id}
            className="flex justify-between items-center bg-gray-100 p-4 rounded-md"
          >
            <span>
              {meddelande.message} (Homework ID: {meddelande.homework_id})
            </span>
            <div className="space-x-2">
              <button
                onClick={() => handleEdit(meddelande)}
                className="text-blue-500 hover:text-blue-700"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(meddelande.id)}
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

export default ManageMeddelanden;
