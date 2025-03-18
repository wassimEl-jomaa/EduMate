import React, { useState, useEffect } from "react";
import axios from "axios";
import HomeworkForm from "./HomeworkForm";
import BetygForm from "./BetygForm";
import MembershipForm from "./MembershipForm";
import MeddelandeForm from "./MeddelandeForm";

const AdminPage = () => {
  const [homeworks, setHomeworks] = useState([]);
  const [betygs, setBetygs] = useState([]);
  const [memberships, setMemberships] = useState([]);
  const [meddelanden, setMeddelanden] = useState([]);

  useEffect(() => {
    // Fetch data from the backend
    axios.get("/api/homeworks").then((response) => setHomeworks(response.data));
    axios.get("/api/betygs").then((response) => setBetygs(response.data));
    axios
      .get("/api/memberships")
      .then((response) => setMemberships(response.data));
    axios
      .get("/api/meddelanden")
      .then((response) => setMeddelanden(response.data));
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <HomeworkForm homeworks={homeworks} setHomeworks={setHomeworks} />
        <BetygForm betygs={betygs} setBetygs={setBetygs} />
        <MembershipForm
          memberships={memberships}
          setMemberships={setMemberships}
        />
        <MeddelandeForm
          meddelanden={meddelanden}
          setMeddelanden={setMeddelanden}
        />
      </div>
    </div>
  );
};

export default AdminPage;
