<form onSubmit={handleSubmit}>
        {/* Assignment Type Toggle */}
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-2">
            Assign To
          </label>
          <div className="flex items-center space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                name="assignmentType"
                value="single"
                checked={assignmentType === "single"}
                onChange={() => setAssignmentType("single")}
                className="mr-2"
              />
              Single Student
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                name="assignmentType"
                value="all"
                checked={assignmentType === "all"}
                onChange={() => setAssignmentType("all")}
                className="mr-2"
              />
              All Class Level
            </label>
          </div>
        </div>

        {/* Conditionally Render Fields */}
        {assignmentType === "single" && (
          <div className="mb-4">
            <label
              htmlFor="user_id"
              className="block text-gray-700 font-semibold"
            >
              Student ID
            </label>
            <input
              type="number"
              id="user_id"
              name="user_id"
              value={homeworkData.user_id}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter Student ID"
            />
          </div>
        )}

        {assignmentType === "all" && (
          <div className="mb-4">
            <label
              htmlFor="class_level_id"
              className="block text-gray-700 font-semibold"
            >
              Class Level
            </label>
            <select
              id="class_level_id"
              name="class_level_id"
              value={homeworkData.class_level_id}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select a class level</option>
              {classLevels.map((classLevel) => (
                <option key={classLevel.id} value={classLevel.id}>
                  {classLevel.name}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Other Form Fields */}
        <div className="mb-4">
          <label
            htmlFor="subject_id"
            className="block text-gray-700 font-semibold"
          >
            Subject
          </label>
          <select
            id="subject_id"
            name="subject_id"
            value={homeworkData.subject_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select a subject</option>
            {subjects.map((subject) => (
              <option key={subject.id} value={subject.id}>
                {subject.name}
              </option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label htmlFor="title" className="block text-gray-700 font-semibold">
            Title
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={homeworkData.title}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter title"
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
            value={homeworkData.description}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter description"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="due_date"
            className="block text-gray-700 font-semibold"
          >
            Due Date
          </label>
          <input
            type="date"
            id="due_date"
            name="due_date"
            value={homeworkData.due_date}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="status" className="block text-gray-700 font-semibold">
            Status
          </label>
          <select
            id="status"
            name="status"
            value={homeworkData.status}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="Pending">Pending</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
          </select>
        </div>
        <div className="mb-4">
          <label
            htmlFor="priority"
            className="block text-gray-700 font-semibold"
          >
            Priority
          </label>
          <select
            id="priority"
            name="priority"
            value={homeworkData.priority}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="Normal">Normal</option>
            <option value="High">High</option>
            <option value="Low">Low</option>
          </select>
        </div>

        <div className="mb-4">
          <label
            htmlFor="teacher_id"
            className="block text-gray-700 font-semibold"
          >
            Teacher
          </label>
          <select
            id="teacher_id"
            name="teacher_id"
            value={homeworkData.teacher_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select a teacher</option>
            {teachers.map((teacher) => (
              <option key={teacher.id} value={teacher.id}>
                {`Teacher ID: ${teacher.id}, Qualifications: ${teacher.qualifications}`}
              </option>
            ))}
          </select>
        </div>

        {/* Error and success messages */}
        {errorMessage && (
          <p className="text-red-500 text-sm mb-4">{errorMessage}</p>
        )}
        {successMessage && (
          <p className="text-green-500 text-sm mb-4">{successMessage}</p>
        )}

        {/* Submit button */}
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-all"
        >
          {editingHomeworkId ? "Update Homework" : "Add Homework"}
        </button>
      </form>

      <h2 className="text-xl font-bold mt-8 mb-4">Existing Homework</h2>
      <ul className="space-y-4">
        {homeworks.map((homework) => (
          <li
            key={homework.id}
            className="flex justify-between items-center bg-gray-100 p-4 rounded-md"
          >
            <span>
              {homework.title} (Due: {homework.due_date})
            </span>
            <div className="space-x-2">
              <button
                onClick={() => handleEdit(homework)}
                className="text-blue-500 hover:text-blue-700"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(homework.id)}
                className="text-red-500 hover:text-red-700"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>


      <form onSubmit={handleSubmit}>
          {/* Assignment Type Toggle */}
          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-2">
              Assign To
            </label>
            <div className="flex items-center space-x-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="assignmentType"
                  value="single"
                  checked={assignmentType === "single"}
                  onChange={() => setAssignmentType("single")}
                  className="mr-2"
                />
                Single Student
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="assignmentType"
                  value="all"
                  checked={assignmentType === "all"}
                  onChange={() => setAssignmentType("all")}
                  className="mr-2"
                />
                All Class Level
              </label>
            </div>
          </div>

          {/* Conditionally Render Fields */}
          {assignmentType === "single" && (
            <div className="mb-4">
              <label
                htmlFor="user_id"
                className="block text-gray-700 font-semibold"
              >
                Student ID
              </label>
              <input
                type="number"
                id="user_id"
                name="user_id"
                value={homeworkData.user_id}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter Student ID"
              />
            </div>
          )}

          {assignmentType === "all" && (
            <div className="mb-4">
              <label
                htmlFor="class_level_id"
                className="block text-gray-700 font-semibold"
              >
                Class Level
              </label>
              <select
                id="class_level_id"
                name="class_level_id"
                value={homeworkData.class_level_id}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select a class level</option>
                {classLevels.map((classLevel) => (
                  <option key={classLevel.id} value={classLevel.id}>
                    {classLevel.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Other Form Fields */}
          {/* Add the rest of the form fields here as provided */}
        </form>
      </div>