import React, { useEffect, useState } from "react";
import axios from "axios";

const BetygPage = ({ userId }) => {
  const [betygList, setBetygList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    console.log("Fetching betyg for userId:", userId);
    axios
      .get(`http://127.0.0.1:8000/betyg/user/${userId}`) // Replace with the correct endpoint
      .then((response) => {
        setBetygList(response.data);
        setLoading(false);
        console.log("User ID:", userId);
      })
      .catch((err) => {
        setError(err.response?.data?.detail || "Failed to fetch grades");
        setLoading(false);
      });
  }, [userId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="p-6 bg-white rounded shadow-md">
      <h2 className="text-2xl font-bold mb-4">Betyg</h2>
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
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default BetygPage;
