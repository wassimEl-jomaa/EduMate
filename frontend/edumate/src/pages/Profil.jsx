import React, { useState, useEffect } from "react";
import axios from "axios";

const Profil = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUser((prevUser) => ({
      ...prevUser,
      [name]: value,
    }));
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.patch(
        `http://localhost:8000/users/${userId}`,
        {
          first_name: user.first_name,
          last_name: user.last_name,
          phone_number: user.phone_number,
        }
      );
      console.log("Updated user data:", response.data);
      setUser(response.data);
      setIsEditing(false); // Switch back to view mode after submitting the form
    } catch (error) {
      console.error("Error updating user data:", error);
    }
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Main Content Section */}
      <div className="flex-1 p-8 bg-white shadow-lg rounded-lg max-w-4xl mx-auto mt-6">
        <h1 className="text-4xl font-semibold text-center mb-8 text-blue-900">
          Profil
        </h1>

        {/* Profile Image */}
        <div className="flex justify-center mb-6">
          <img
            src={user.image}
            alt="Profile"
            className="w-32 h-32 rounded-full border-4 border-blue-300"
          />
        </div>

        {/* User's Name and Email */}
        <div className="text-center mb-4">
          <h2 className="text-2xl font-bold text-blue-700">{user.name}</h2>
          <p className="text-lg text-gray-600">{user.email}</p>
        </div>

        {/* Toggle Edit/View Mode Button */}
        <div className="text-center mb-6">
          <button
            onClick={() => setIsEditing(!isEditing)}
            className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-all"
          >
            {isEditing ? "Avbryt Ändringar" : "Redigera Profil"}
          </button>
        </div>

        {/* Profile Information */}
        <form onSubmit={handleFormSubmit}>
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-blue-700 mb-4">
              Personlig Information
            </h3>
            <div className="space-y-2">
              {/* Edit fields only appear when in edit mode */}
              {isEditing ? (
                <>
                  <input
                    type="text"
                    name="first_name"
                    value={user.first_name}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    placeholder="Förnamn"
                  />
                  <input
                    type="text"
                    name="last_name"
                    value={user.last_name}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    placeholder="Efternamn"
                  />
                  <input
                    type="text"
                    name="phone_number"
                    value={user.phone_number}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    placeholder="Telefonnummer"
                  />
                </>
              ) : (
                <>
                  <p>
                    <strong>Förnamn:</strong> {user.first_name}
                  </p>
                  <p>
                    <strong>Efternamn:</strong> {user.last_name}
                  </p>
                  <p>
                    <strong>Telefonnummer:</strong> {user.phone_number}
                  </p>
                  <p>
                    <strong>Skola:</strong> {user.arskurs?.skola}
                  </p>
                  <p>
                    <strong>Klass:</strong> {user.arskurs?.klass}
                  </p>
                  <p>
                    <strong>Årskurs:</strong> {user.arskurs?.name}
                  </p>

                  <p>
                    <strong>Medlemskap:</strong>{" "}
                    {user.membership?.membership_type || "Ingen"}
                  </p>
                </>
              )}
            </div>
          </div>

          {/* Submit Button to Save Changes */}
          {isEditing && (
            <div className="text-center">
              <button
                type="submit"
                className="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-700 transition-all"
              >
                Spara Ändringar
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default Profil;
