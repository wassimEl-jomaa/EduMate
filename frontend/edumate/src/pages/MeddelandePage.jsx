import React, { useEffect, useState } from "react";
import axios from "axios";

const MeddelandePage = ({ userId }) => {
  const [meddelanden, setMeddelanden] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    console.log("Fetching meddelanden for userId:", userId);
    axios
      .get(`http://127.0.0.1:8000/meddelanden/user/${userId}`) // Updated URL
      .then((response) => {
        setMeddelanden(response.data);
        setLoading(false);
        console.log("User ID:", userId);
      })
      .catch((err) => {
        setError(err.response?.data?.detail || "Failed to fetch messages");
        setLoading(false);
      });
  }, [userId]);

  const handleStatusUpdate = (meddelandeId) => {
    axios
      .put(`http://127.0.0.1:8000/meddelanden/${meddelandeId}/mark_as_read`)
      .then(() => {
        // Update the status locally after a successful request
        setMeddelanden((prevMeddelanden) =>
          prevMeddelanden.map((meddelande) =>
            meddelande.id === meddelandeId
              ? { ...meddelande, read_status: "Read" }
              : meddelande
          )
        );
      })
      .catch((err) => {
        console.error("Failed to update status:", err);
      });
    axios
      .put(
        `http://127.0.0.1:8000/meddelanden/${meddelandeId}/?mark_as_read=true`
      )
      .then((response) => {
        console.log("Meddelande marked as read:", response.data);
      })
      .catch((error) => {
        console.error("Failed to mark as read:", error);
      });
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="p-6 bg-white rounded shadow-md">
      <h2 className="text-2xl font-bold mb-4">Meddelanden</h2>
      {meddelanden.length === 0 ? (
        <p className="text-gray-600">Inga meddelanden att visa.</p>
      ) : (
        <ul className="space-y-4">
          {meddelanden.map((meddelande) => (
            <li
              key={meddelande.id}
              className="p-4 border rounded bg-gray-100 hover:bg-gray-200 transition"
            >
              <h3 className="text-lg font-semibold">{meddelande.message}</h3>
              <p className="text-gray-700">{meddelande.description}</p>
              <p className="text-sm text-gray-500">
                Skapad: {new Date(meddelande.created_at).toLocaleString()}
              </p>
              <p className="text-sm text-gray-500">
                Status: {meddelande.read_status}
              </p>
              <button
                onClick={() => handleStatusUpdate(meddelande.id)}
                className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
                disabled={meddelande.read_status === "Read"} // Disable if already "Read"
              >
                {meddelande.read_status === "Read"
                  ? "Already Read"
                  : "Mark as Read"}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MeddelandePage;
