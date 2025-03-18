import React, { useState } from "react";
import axios from "axios";

const BetygForm = ({ betygs, setBetygs }) => {
  const [formData, setFormData] = useState({
    grade: "",
    comments: "",
    feedback: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post("/api/betygs", formData).then((response) => {
      setBetygs([...betygs, response.data]);
      setFormData({ grade: "", comments: "", feedback: "" });
    });
  };

  return (
    <div className="p-4 bg-white rounded shadow-md">
      <h2 className="text-xl font-bold mb-4">Add Betyg</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700">Grade</label>
          <input
            type="text"
            name="grade"
            value={formData.grade}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Comments</label>
          <textarea
            name="comments"
            value={formData.comments}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          ></textarea>
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Feedback</label>
          <textarea
            name="feedback"
            value={formData.feedback}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          ></textarea>
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white p-2 rounded"
        >
          Add Betyg
        </button>
      </form>
    </div>
  );
};

export default BetygForm;
