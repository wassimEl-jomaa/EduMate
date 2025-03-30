import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate for programmatic routing

const RegisterForm = () => {
  const navigate = useNavigate(); // Initialize the useNavigate hook
  // Skapa state för formulärdata
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  // Skapa en state för eventuella fel
  const [error, setError] = useState("");

  // Hantera formulärändringar
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  // Hantera form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setError("Lösenorden matchar inte.");
    } else {
      // Här kan du skicka formuläruppgifter till en server eller API
      const data = {
        username:
          formData.first_name.substring(0, 3) +
          formData.last_name.substring(0, 3),
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        password: formData.password,
        phone_number: formData.phone_number,
      };
      const options = {
        headers: { "Content-Type": "application/json" },
        method: "POST",
        mode: "cors",
        body: JSON.stringify(data),
      };
      try {
        const result = await fetch(`http://localhost:8000/users/`, options);
        if (!result.ok) {
          const errorData = await result.json();
          throw new Error(
            errorData.detail || "Det gick inte att skapa användaren."
          );
        }
        alert("Användare skapades!");
        navigate("/login");
      } catch (error) {
        console.error("Error creating user:", error.message);
        setError(error.message);
      }
    }
  };

  return (
    <main className="container mx-auto px-6 py-10">
      <div className="max-w-lg mx-auto bg-white p-8 border rounded-lg shadow-md">
        <h2 className="text-3xl font-semibold text-center mb-6">
          Skapa ett Konto
        </h2>
        {error && <div className="text-red-500 text-center mb-4">{error}</div>}
        <form onSubmit={handleSubmit}>
          {/* Namn */}
          <div className="mb-4">
            <label
              htmlFor="first_name"
              className="block text-gray-700 font-semibold"
            >
              Förnamn
            </label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          <div className="mb-4">
            <label
              htmlFor="last_name"
              className="block text-gray-700 font-semibold"
            >
              Efternamn
            </label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          {/* E-post */}
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
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          {/* Telefonnummer */}
          <div className="mb-4">
            <label
              htmlFor="phone_number"
              className="block text-gray-700 font-semibold"
            >
              Telefonnummer
            </label>
            <input
              type="tel"
              id="phone_number"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          {/* Lösenord */}
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
              value={formData.password}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          {/* Bekräfta Lösenord */}
          <div className="mb-4">
            <label
              htmlFor="confirmPassword"
              className="block text-gray-700 font-semibold"
            >
              Bekräfta Lösenord
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />
          </div>

          {/* Submit Button */}
          <div className="flex justify-center">
            <button
              type="submit"
              className="bg-yellow-500 text-white py-2 px-6 rounded-md hover:bg-yellow-600 transition-all"
            >
              Registrera
            </button>
          </div>
        </form>

        <div className="mt-4 text-center">
          <p className="text-sm text-gray-700">
            Har du redan ett konto?{" "}
            <a href="/login" className="text-blue-500 hover:text-blue-700">
              Logga in här
            </a>
          </p>
        </div>
      </div>
    </main>
  );
};

export default RegisterForm;
