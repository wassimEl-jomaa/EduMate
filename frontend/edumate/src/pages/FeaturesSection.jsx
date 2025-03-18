import React from "react";

const FeaturesSection = () => {
  return (
    <section id="features" className="py-20 px-6 bg-white">
      {/* Välkommen Sektion */}
      <div className="text-center mb-12">
        <h2 className="text-3xl font-semibold text-blue-800 mb-4">
          Välkommen till vår AI-drivna Läxhjälp!
        </h2>
        <p className="text-lg text-gray-700 mb-6">
          Välkommen till vår innovativa lärplattform där AI hjälper dig att nå
          dina akademiska mål. Vi erbjuder en personlig lärplan som anpassar sig
          efter dina behov och framsteg, så att du kan lära dig på ditt sätt och
          i din egen takt.
        </p>
        <p className="text-lg text-gray-700 mb-6">
          Med vår plattform får du skräddarsydda uppgifter och övningar, och
          kontinuerlig feedback som hjälper dig att förbättra dina färdigheter.
          AI:n följer din utveckling och justerar övningarna i realtid, vilket
          ger dig en unik och effektiv inlärningsupplevelse.
        </p>
        <p className="text-lg text-gray-700">
          Låt oss hjälpa dig att nå dina mål och ta nästa steg mot framgång!
        </p>
      </div>

      {/* Funktioner Sektion */}
      <h2 className="text-3xl font-semibold text-center text-blue-800 mb-12">
        Viktiga Funktioner
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-12">
        <div className="bg-gray-100 p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold text-blue-800 mb-4">
            Anpassad Lärplan
          </h3>
          <p className="text-gray-700">
            AI analyserar styrkor och svagheter för att skapa en individuell
            lärplan som hjälper till att förbättra svaga områden.
          </p>
        </div>
        <div className="bg-gray-100 p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold text-blue-800 mb-4">
            Progressionsspårning
          </h3>
          <p className="text-gray-700">
            AI följer din utveckling och justerar svårighetsgraden för att passa
            din inlärningstakt.
          </p>
        </div>
        <div className="bg-gray-100 p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold text-blue-800 mb-4">
            Omfattande Rapportering
          </h3>
          <p className="text-gray-700">
            Detaljerade rapporter för att följa framsteg och identifiera
            problemområden som behöver åtgärdas.
          </p>
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
