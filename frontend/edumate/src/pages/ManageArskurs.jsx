import React, { useState, useEffect } from "react";
import axios from "axios";

const ManageArskurs = () => {
  const [arskursList, setArskursList] = useState([]); // State for the list of Arskurs
  const [arskursData, setArskursData] = useState({
    name: "",
    description: "",
    skola: "",
    klass: "",
  }); // State for Arskurs data
  const [editingArskursId, setEditingArskursId] = useState(null); // State for editing Arskurs ID
  const [successMessage, setSuccessMessage] = useState(""); // State for success message
  const [errorMessage, setErrorMessage] = useState(""); // State for error message

  // Fetch Arskurs from the backend
  useEffect(() => {
    const fetchArskurs = async () => {
      const token = localStorage.getItem("token"); // Retrieve the token from localStorage
      try {
        const response = await axios.get("http://localhost:8000/arskurs/", {
          headers: {
            Authorization: `Bearer ${token}`, // Include the token in the Authorization header
          },
        });
        setArskursList(response.data);
      } catch (error) {
        console.error(
          "Error fetching Arskurs:",
          error.response?.data || error.message
        );
        setErrorMessage("Failed to fetch Arskurs. Please try again.");
      }
    };

    fetchArskurs();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!arskursData.name || !arskursData.description) {
      setErrorMessage("Name and description are required.");
      return;
    }

    const token = localStorage.getItem("token"); // Retrieve the token from localStorage

    try {
      if (editingArskursId) {
        // Update Arskurs
        const response = await axios.patch(
          `http://localhost:8000/arskurs/${editingArskursId}/`,
          arskursData,
          {
            headers: {
              Authorization: `Bearer ${token}`, // Include the token in the Authorization header
            },
          }
        );
        setArskursList((prevArskurs) =>
          prevArskurs.map((arskurs) =>
            arskurs.id === editingArskursId ? response.data : arskurs
          )
        );
        setSuccessMessage(
          `Arskurs "${response.data.name}" updated successfully!`
        );
      } else {
        // Add Arskurs
        const response = await axios.post(
          "http://localhost:8000/arskurs/",
          arskursData,
          {
            headers: {
              Authorization: `Bearer ${token}`, // Include the token in the Authorization header
            },
          }
        );
        setArskursList((prevArskurs) => [...prevArskurs, response.data]);
        setSuccessMessage(
          `Arskurs "${response.data.name}" added successfully!`
        );
      }

      setErrorMessage("");
      setArskursData({
        name: "",
        description: "",
        skola: "",
        klass: "",
      });
      setEditingArskursId(null);
    } catch (error) {
      console.error(
        "Error managing Arskurs:",
        error.response?.data || error.message
      );
      setErrorMessage("Failed to manage Arskurs. Please try again.");
      setSuccessMessage("");
    }
  };

  // Delete an Arskurs
  const handleDelete = async (arskursId) => {
    const token = localStorage.getItem("token"); // Retrieve the token from localStorage
    try {
      await axios.delete(`http://localhost:8000/arskurs/${arskursId}/`, {
        headers: {
          Authorization: `Bearer ${token}`, // Include the token in the Authorization header
        },
      });
      setArskursList((prevArskurs) =>
        prevArskurs.filter((arskurs) => arskurs.id !== arskursId)
      );
      setSuccessMessage("Arskurs deleted successfully!");
      setErrorMessage("");
    } catch (error) {
      console.error(
        "Error deleting Arskurs:",
        error.response?.data || error.message
      );
      setErrorMessage("Failed to delete Arskurs. Please try again.");
      setSuccessMessage("");
    }
  };

  // Start editing an Arskurs
  const handleEdit = (arskurs) => {
    setArskursData({
      name: arskurs.name,
      description: arskurs.description,
      skola: arskurs.skola,
      klass: arskurs.klass,
    });
    setEditingArskursId(arskurs.id);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setArskursData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="max-w-lg mx-auto bg-white p-8 border rounded-lg shadow-md mt-10">
      <h1 className="text-2xl font-bold mb-6">Manage Arskurs</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="name" className="block text-gray-700 font-semibold">
            Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={arskursData.name}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter name"
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
            value={arskursData.description}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter description"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="skola" className="block text-gray-700 font-semibold">
            Skola
          </label>
          <input
            type="text"
            id="skola"
            name="skola"
            value={arskursData.skola}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter skola"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="klass" className="block text-gray-700 font-semibold">
            Klass
          </label>
          <input
            type="text"
            id="klass"
            name="klass"
            value={arskursData.klass}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter klass"
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
          {editingArskursId ? "Update Arskurs" : "Add Arskurs"}
        </button>
      </form>

      <h2 className="text-xl font-bold mt-8 mb-4">Existing Arskurs</h2>
      <ul className="space-y-4">
        {arskursList.map((arskurs) => (
          <li
            key={arskurs.id}
            className="flex justify-between items-center bg-gray-100 p-4 rounded-md"
          >
            <span>
              {arskurs.name} - {arskurs.description} ({arskurs.skola},{" "}
              {arskurs.klass})
            </span>
            <div className="space-x-2">
              <button
                onClick={() => handleEdit(arskurs)}
                className="text-blue-500 hover:text-blue-700"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(arskurs.id)}
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

export default ManageArskurs;
