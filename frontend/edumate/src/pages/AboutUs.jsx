import React from "react";
import { Link } from "react-router-dom";

const AboutUs = () => {
  return (
    <div className="container mx-auto px-6 py-10">
      <h1 className="text-4xl font-semibold text-center mb-8 text-black shadow-lg rounded-lg p-6 bg-gradient-to-r from-blue-400 to-indigo-600 text-white">
        Om Oss
      </h1>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <p className="text-lg mb-4">
          <strong>Vår vision</strong> är att revolutionera lärande med hjälp av
          avancerad artificiell intelligens. På vår plattform strävar vi efter
          att ge varje student en unik och effektiv inlärningsupplevelse, genom
          att erbjuda skräddarsydda läxuppgifter, resurser och kontinuerlig
          feedback.
        </p>

        <p className="text-lg mb-4">
          Med hjälp av den senaste AI-teknologin analyserar vi studentens
          individuella framsteg och behov för att skapa en personlig lärplan som
          ständigt anpassas för att ge optimala resultat. Vårt mål är att ge
          eleverna verktygen de behöver för att lyckas, oavsett deras nivå,
          genom att erbjuda stöd i realtid och inspirera till kontinuerlig
          förbättring.
        </p>

        <p className="text-lg">
          Vi är en grupp passionerade teknologer och pedagoger som tror på
          kraften av anpassat lärande och dess potential att förändra utbildning
          för framtiden. Vi arbetar ständigt för att förbättra vår plattform så
          att vi kan ge dig den bästa möjliga upplevelsen och stödja dig på din
          läranderesa.
        </p>
      </div>

      {/* Kontakta oss knapp */}
      <div className="text-center mt-8">
        <Link to="/contactUs">
          <button className="bg-blue-500 text-white px-8 py-3 rounded-md hover:bg-blue-600 transition-all">
            Kontakta Oss
          </button>
        </Link>
      </div>
    </div>
  );
};

export default AboutUs;
