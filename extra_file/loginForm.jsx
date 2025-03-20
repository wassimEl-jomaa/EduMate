import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom"; // Import useNavigate for programmatic routing
import axios from "axios"; // Import axios

export default function LoginForm({ signedIn, setSignedIn, setUserId }) {
  const [email, setEmail] = useState(""); // State for email
  const [password, setPassword] = useState(""); // State for password
  const [errorMessage, setErrorMessage] = useState(""); // State for error message
  const navigate = useNavigate(); // Initialize the useNavigate hook

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload on form submit

    // Simple validation
    if (!email || !password) {
      setErrorMessage("Vänligen fyll i både e-post och lösenord.");
      return;
    }

    try {
      // Send login request to the backend as form data
      const formData = new URLSearchParams();
      formData.append("username", email); // Backend expects "username"
      formData.append("password", password); // Backend expects "password"

      const response = await axios.post(
        "http://localhost:8000/token",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded", // Set the correct content type
          },
        }
      );

      const { access_token } = response.data; // Extract the token from the response
      localStorage.setItem("token", access_token); // Store the token in localStorage
      setSignedIn(true); // Update signed-in state
      setErrorMessage(""); // Clear any error messages

      // Decode the token to get user information (optional)
      const decodedToken = JSON.parse(atob(access_token.split(".")[1])); // Decode JWT payload
      console.log("Decoded Token:", decodedToken);

      // Redirect based on user role (optional)
      if (decodedToken.role === "Admin") {
        navigate("/admin");
      } else {
        navigate("/minsida");
      }
    } catch (error) {
      console.error("Error logging in:", error);
      setErrorMessage("Fel användarnamn eller lösenord");
    }
  };
  useEffect(() => {
    if (signedIn) {
      navigate("/minsida");
    }
  }, [signedIn, navigate]);

  return (
    <div className="bg-gray-100">
      {/* Main Section */}
      <main className="container mx-auto px-6 py-10">
        <div className="max-w-lg mx-auto bg-white p-8 border rounded-lg shadow-md">
          <h2 className="text-3xl font-semibold text-center mb-6">Logga In</h2>

          {/* Login Form */}
          <form id="login-form" onSubmit={handleSubmit}>
            <div className="mb-4">
              <label
                htmlFor="email"
                className="block text-gray-700 font-semibold"
              >
                E-post
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)} // Handle email input
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
            </div>

            <div className="mb-4">
              <label
                htmlFor="password"
                className="block text-gray-700 font-semibold"
              >
                Lösenord
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)} // Handle password input
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
            </div>

            {/* Error Message */}
            {errorMessage && (
              <div id="error-message" className="text-red-500 mt-4 text-center">
                {errorMessage}
              </div>
            )}

            <div className="flex justify-center">
              <button
                type="submit"
                className="bg-blue-200 text-xl font-semibold text-center py-2 px-6 rounded-md hover:bg-blue-600 transition-all"
              >
                Logga In
              </button>
            </div>
          </form>

          {/* Registration Link */}
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-700">
              Har du inget konto?
              <Link
                to="/register"
                className="text-blue-500 hover:text-blue-700"
              >
                Registrera dig här
              </Link>
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
