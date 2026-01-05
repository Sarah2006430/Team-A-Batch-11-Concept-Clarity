import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ResultCard from "./components/ResultCard";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-6">
        Driver Facial Analysis System
      </h1>

      <UploadForm
        setResult={setResult}
        setLoading={setLoading}
        setError={setError}
      />

      {loading && <p className="mt-4">Analyzing...</p>}
      {error && <p className="text-red-500 mt-4">{error}</p>}

      <ResultCard result={result} />
    </div>
  );
}

export default App;
