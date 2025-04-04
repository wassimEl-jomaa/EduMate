import React, { useState, useEffect } from "react";
import axios from "axios";
import SideBar from "../components/SideBar";

const MinSida = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [homeworkList, setHomeworkList] = useState([]); // Define homeworkList state

  // Fetch user data
  useEffect(() => {
    const token = localStorage.getItem("token");
    console.log("Fetching user data for userId:", userId);

    const fetchUserData = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/users/${userId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        console.log("Fetched user data:", response.data);
        setUser(response.data);
      } catch (error) {
        console.error(
          "Error fetching user data:",
          error.response?.data || error.message
        );
      }
    };

    if (userId) {
      fetchUserData();
    }
  }, [userId]);

  // Fetch homework data
  useEffect(() => {
    const token = localStorage.getItem("token");
    console.log("Fetching homework list for userId:", userId);

    const fetchHomeworkData = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/homeworks/${userId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        console.log("Fetched homework data:", response.data);
        setHomeworkList(response.data);
      } catch (error) {
        console.error(
          "Error fetching homework data:",
          error.response?.data || error.message
        );
      }
    };

    if (userId) {
      fetchHomeworkData();
    }
  }, [userId]);

  // Handle homework completion
  const handleCompleteHomework = async (homeworkId) => {
    try {
      const response = await axios.patch(
        `http://localhost:8000/homeworks/${homeworkId}`,
        { status: "Klar" } // Updating homework status to "Klar"
      );
      console.log("Updated homework data:", response.data);
      setHomeworkList((prevList) =>
        prevList.map((homework) =>
          homework.id === homeworkId
            ? { ...homework, status: "Klar" } // Update the status of completed homework in local state
            : homework
        )
      );
    } catch (error) {
      console.error("Error completing homework:", error);
    }
  };

  if (!user) {
    return (
      <div className="flex min-h-screen">
        <SideBar />
        <div className="flex-1 p-6 bg-gray-100">
          <h1 className="text-4xl font-semibold text-center mb-8 blue shadow-lg rounded-lg p-6 bg-gradient-to-r from-blue-400 to-indigo-600 text-white">
            Laddar användardata...
          </h1>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen">
      <SideBar />
      <div className="flex-1 p-6 bg-gray-100">
        <h1 className="text-4xl font-semibold text-center mb-8 blue shadow-lg rounded-lg p-6 bg-gradient-to-r from-blue-400 to-indigo-600 text-white">
          Välkommen,{" "}
          {user.first_name && user.last_name
            ? `${user.first_name} ${user.last_name}`
            : "Användare"}
          !
        </h1>

        {/* Ongoing Homework Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Pågående Läxor</h2>
          <div className="space-y-4">
            {homeworkList.length === 0 ? (
              <p>Inga pågående läxor.</p>
            ) : (
              homeworkList.map((homework) => (
                <div
                  key={homework.id}
                  className="bg-white p-4 rounded-lg shadow-md"
                >
                  <h3 className="text-xl font-semibold">{homework.title}</h3>
                  <p>
                    <strong>Beskrivning:</strong> {homework.description}
                  </p>
                  <p>
                    <strong>Filuppladdning:</strong>{" "}
                    {homework.filuppladdning?.filepath || "Ej betygsatt"}
                  </p>
                  <p>
                    <strong>Förfallodatum:</strong> {homework.due_date}
                  </p>
                  <p>
                    <strong>Status:</strong> {homework.status}
                  </p>
                  <p>
                    <strong>Prioritet:</strong> {homework.priority}
                  </p>
                  <p>
                    <strong>Ämne:</strong> {homework.subject?.name}
                  </p>

                  {homework.status !== "Klar" && (
                    <button
                      onClick={() => handleCompleteHomework(homework.id)}
                      className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-all"
                    >
                      Markera som klar
                    </button>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MinSida;
