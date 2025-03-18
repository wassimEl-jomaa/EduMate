import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import FeaturesSection from "./pages/FeaturesSection";
import HowItWorksSection from "./pages/HowItWorksSection";
import PlansSection from "./pages/PlansSection";
import RegisterForm from "./pages/RegisterForm";
import LoginForm from "./pages/LoginForm"; // Corrected this to match the component name
import MinSida from "./pages/MinSida"; // Import the MinSida component
import PersonligLärplan from "./pages/PersonligLärplan"; // Import PersonligLärplan
import AboutUs from "./pages/AboutUs";
import ContactUs from "./pages/ContactUs";
import SideBar from "./components/SideBar";
import Profil from "./pages/Profil"; // Import Profil component
import Admin from "./pages/Admin"; // Import Admin component

const App = () => {
  const [signedIn, setSignedIn] = useState(false);
  const [userId, setUserId] = useState(null); // Add userId state

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
          } // Pass setUserId to LoginForm
        />
        <Route path="/login" element={<SideBar />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/profil" element={<Profil userId={userId} />} />{" "}
        <Route path="/MinSida" element={<MinSida userId={userId} />} />{" "}
        <Route path="/Admin" element={<Admin userId={userId} />} />{" "}
        {/* Pass userId to Profil */}
        <Route path="/PersonligLärplan" element={<PersonligLärplan />} />
        <Route path="/AboutUs" element={<AboutUs />} />
        <Route path="/contactUs" element={<ContactUs />} />
      </Routes>
      <Footer />
    </div>
  );
};

export default App;
