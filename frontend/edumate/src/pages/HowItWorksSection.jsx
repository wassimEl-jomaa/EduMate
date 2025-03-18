import React from "react";
import { Link } from "react-router-dom";

const HurDetFungerarSektion = () => {
  return (
    <section id="om" className="py-20 px-6 bg-blue-50">
      <h2 className="text-3xl font-semibold text-center text-blue-800 mb-8">
        Så Här Fungerar Det
      </h2>
      <div className="text-center max-w-3xl mx-auto mb-12">
        <p className="text-lg text-gray-700 mb-4">
          Plattformen använder avancerad AI för att skapa en personlig lärplan,
          följa din utveckling och ge dig kontinuerlig feedback för att
          förbättra dina färdigheter.
        </p>
        <p className="text-lg text-gray-700">
          Användare kan ta del av anpassade uppgifter och övningar som anpassas
          i realtid beroende på elevens framsteg och behov.
        </p>
      </div>

      <div className="mx-auto p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Punkt Ett */}
        <div className="kort bg-white p-6 border rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold">
            Anpassad Lärandeupplevelse Personlig lärplan:
          </h2>
          <p className="mt-4 text-gray-700">
            Plattformen använder AI för att analysera elevens styrkor och
            svagheter och skapar en individuell lärplan som fokuserar på de
            områden där eleven behöver mest stöd. Progressionsspårning: AI kan
            följa elevens framsteg över tid och justera svårighetsgraden på
            uppgifter och övningar baserat på hur snabbt eleven lär sig.
          </p>

          <div className="mt-6 flex justify-center">
            {/* PersonligLärplan */}
            <Link
              to="./PersonligLärplan"
              className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition-all"
            >
              Läs Mer
            </Link>
          </div>
        </div>

        {/* Punkt Två */}
        <div className="kort bg-white p-6 border rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold">
            Interaktiv Läxhjälp Omedelbar feedback:
          </h2>
          <p className="mt-4 text-gray-700">
            När elever löser uppgifter får de direkt feedback på sina svar,
            vilket gör att de kan rätta sina misstag på en gång. Fråga AI:
            Elever kan ställa frågor till AI:n när de inte förstår ett koncept,
            och AI:n kan förklara det på ett enkelt och begripligt sätt, kanske
            till och med genom att ge olika exempel.
          </p>
          {/* Knapp Sektion */}
          <div className="mt-6 flex justify-center">
            <Link
              to="/"
              className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition-all"
            >
              Läs Mer
            </Link>
          </div>
        </div>

        {/* Punkt Tre */}
        <div className="kort bg-white p-6 border rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold">
            Multimodal Lärande Text, ljud och video:
          </h2>
          <p className="mt-4 text-gray-700">
            För att möta olika lärstilar kan plattformen använda olika medier
            som text, ljudinspelningar eller videolektioner. AI kan även hjälpa
            till att skapa förklarande videor baserat på elevens behov.
            Gamification: För att hålla elever engagerade kan plattformen
            inkludera spelbaserade element, där eleverna kan samla poäng, klara
            av nivåer och få belöningar för sina framsteg.
          </p>
          {/* Knapp Sektion */}
          <div className="mt-6 flex justify-center">
            <Link
              to="/"
              className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition-all"
            >
              Läs Mer
            </Link>
          </div>
        </div>

        {/* Punkt Fyra */}
        <div className="kort bg-white p-6 border rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold">
            Automatiserad Prov och Bedömning Smart provgenerering:
          </h2>
          <p className="mt-4 text-gray-700">
            AI kan skapa automatiska prov som är anpassade efter elevens
            nuvarande kunskapsnivå, vilket gör att proven är både utmanande och
            rättvisa. Bedömning av öppen text: AI kan också bedöma öppna svar
            eller uppsatser genom att analysera textens kvalitet, struktur och
            relevans i relation till det lärda materialet.
          </p>
          {/* Knapp Sektion */}
          <div className="mt-6 flex justify-center">
            <Link
              to="/"
              className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition-all"
            >
              Läs Mer
            </Link>
          </div>
        </div>

        {/* Punkt Fem */}
        <div className="kort bg-white p-6 border rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">
            Föräldra- och Lärareverktyg Rapporter
          </h2>
          <ul className="list-none space-y-4">
            <li>
              <p className="font-bold text-xl text-blue-500">Rapporter:</p>
              <p className="text-gray-700">
                Plattformen kan generera detaljerade rapporter som visar elevens
                framsteg, områden som behöver förbättras och rekommendationer
                för vidare lärande.
              </p>
            </li>
            <li>
              <p className="font-bold text-xl text-blue-500">Samarbete:</p>
              <p className="text-gray-700">
                Lärare och föräldrar kan få tillgång till plattformens data för
                att hjälpa till att stödja elevens lärande.
              </p>
            </li>
          </ul>
          {/* Knapp Sektion */}
          <div className="mt-6 flex justify-center">
            <Link
              to="/"
              className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition-all"
            >
              Läs Mer
            </Link>
          </div>
        </div>

        {/* Punkt Sex */}
        <div className="kort bg-white p-6 border rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold">
            Språk- och Kulturunderstöd Flerspråkighet:
          </h2>
          <ul className="list-none space-y-4">
            <li>
              <p className="font-bold text-xl text-blue-500">
                Natural Language Processing (NLP):
              </p>
              <p className="text-gray-700">
                För att analysera och förstå elevens frågor och svar på ett mer
                mänskligt sätt.
              </p>
            </li>

            <li>
              <p className="font-bold text-xl text-blue-500">
                Machine Learning:
              </p>
              <p className="text-gray-700">
                För att kontinuerligt förbättra och anpassa plattformens
                rekommendationer baserat på användardata. Dataanalys: För att
                skapa insikter om elevens inlärningsmönster och ge
                rekommendationer till både elever och lärare.
              </p>
            </li>
          </ul>
          {/* Knapp Sektion */}
          <div className="mt-6 flex justify-center">
            <Link
              to="/"
              className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition-all"
            >
              Läs Mer
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HurDetFungerarSektion;
