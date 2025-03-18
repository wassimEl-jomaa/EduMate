// Mocked data
const homeworkData = [
  {
    id: 1,
    title: "Matematik: Algebraövningar",
    dueDate: "2025-03-05",
    status: "Pågående",
  },
  {
    id: 2,
    title: "Engelska: Läsförståelse",
    dueDate: "2025-03-07",
    status: "Ej påbörjad",
  },
  {
    id: 3,
    title: "Historia: Franska Revolutionen",
    dueDate: "2025-03-10",
    status: "Pågående",
  },
];

const resourcesData = [
  { title: "Algebra 101", type: "Video", url: "https://example.com/video" },
  {
    title: "Engelska grammatik",
    type: "E-bok",
    url: "https://example.com/ebook",
  },
];

const aiSuggestionsData = [
  "Fokusera på att öva algebra för att förbättra dina matematikfärdigheter.",
  "Försök att läsa varje engelskt stycke minst tre gånger för bättre förståelse.",
  "Läs på om de viktigaste händelserna under den franska revolutionen.",
];

// Functions to simulate API calls
export const getHomework = async () => {
  try {
    const response = await fetch("http://localhost:8000/homeworks/");
    if (!response.ok) {
      throw new Error("Failed to fetch homework data");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching homework data:", error);
    return [];
  }
};

export const getResources = () => {
  return resourcesData;
};

export const getAiSuggestions = () => {
  return aiSuggestionsData;
};

// Function to fetch user details from the backend
export const getUserDetails = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/user");
    if (!response.ok) {
      throw new Error("Failed to fetch user details");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching user details:", error);
    return { first_name: "", last_name: "" };
  }
};
