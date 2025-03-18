import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import FeaturesSection from "./pages/FeaturesSection";
import HowItWorksSection from "./pages/HowItWorksSection";
import PlansSection from "./pages/PlansSection";
import RegisterForm from "./pages/RegisterForm";
import LoginForm from "./pages/LoginForm";
import MinSida from "./pages/MinSida";
import PersonligLärplan from "./pages/PersonligLärplan";
import AboutUs from "./pages/AboutUs";
import ContactUs from "./pages/ContactUs";
import AddRole from "./pages/AddRole";
import Profil from "./pages/Profil";
import Admin from "./pages/Admin"; // Import the Admin component
import ManageUsers from "./pages/ManageUsers";
import ManageMemberships from "./pages/ManageMemberships";
import ManageArskurs from "./pages/ManageArskurs";
import ManageMeddelanden from "./pages/ManageMeddelanden";

import ManageBetyg from "./pages/ManageBetyg";
import ManageSubjects from "./pages/ManageSubjects";
const App = () => {
  const [signedIn, setSignedIn] = useState(false);
  const [userId, setUserId] = useState(null);

  return (
    <div className="bg-gray-100">
      <Header signedIn={signedIn} setSignedIn={setSignedIn} />
      <Routes>
        <Route
          path="/"
          element={
            <>
              <FeaturesSection />
              <HowItWorksSection />
              <PlansSection />
            </>
          }
        />
        <Route
          path="/login"
          element={
            <LoginForm
              signedIn={signedIn}
              setSignedIn={setSignedIn}
              setUserId={setUserId}
            />
          }
        />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/profil" element={<Profil userId={userId} />} />
        <Route path="/minsida" element={<MinSida userId={userId} />} />
        <Route path="/admin" element={<Admin />} /> {/* Add the Admin route */}
        <Route path="/personliglarplan" element={<PersonligLärplan />} />
        <Route path="/aboutus" element={<AboutUs />} />
        <Route path="/contactus" element={<ContactUs />} />
        <Route path="/add-role" element={<AddRole />} />
        <Route path="/manage-users" element={<ManageUsers />} />
        <Route path="/manage-memberships" element={<ManageMemberships />} />
        <Route path="/manage-arskurs" element={<ManageArskurs />} />
        <Route path="/betyg" element={<ManageBetyg />} />
        <Route path="/manage-subjects" element={<ManageSubjects />} />
        <Route path="/manage-meddelanden" element={<ManageMeddelanden />} />
      </Routes>
      <Footer />
    </div>
  );
};

export default App;
