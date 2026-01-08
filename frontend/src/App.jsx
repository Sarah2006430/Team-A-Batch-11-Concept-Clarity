import bgImage from "./assets/bg.png";
import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ResultCard from "./components/ResultCard";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  return (
    <div
      className="min-h-screen flex items-center justify-center px-4"
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className="bg-white/90 backdrop-blur-md w-full max-w-3xl rounded-2xl shadow-2xl p-8">
        
        <h1 className="text-4xl font-extrabold text-center text-indigo-700">
          Driver Facial Analysis System
        </h1>

        <p className="text-center text-gray-600 mt-2 mb-8">
          Detect driver drowsiness and risk level using facial analysis
        </p>

        <UploadForm
          setResult={setResult}
          setLoading={setLoading}
          setError={setError}
        />

        {loading && (
          <p className="text-center text-indigo-600 mt-4 font-semibold animate-pulse">
            Analyzing driver state...
          </p>
        )}

        {error && (
          <p className="text-center text-red-600 mt-4 font-medium">
            {error}
          </p>
        )}

        <ResultCard result={result} />
      </div>
    </div>
  );
}

export default App;
