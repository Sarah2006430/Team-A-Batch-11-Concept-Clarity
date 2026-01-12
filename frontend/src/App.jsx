import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ResultCard from "./components/ResultCard";
import Toast from "./components/Toast";
import bg from "./assets/bg.png";

function App() {
  const [toast, setToast] = useState("");
  const [result, setResult] = useState(null);

  return (
    <div
      className="min-h-screen flex items-center justify-center p-6"
      style={{
        backgroundImage: `url(${bg})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <Toast message={toast} />

      <div className="bg-white/90 backdrop-blur-md w-full max-w-3xl rounded-2xl shadow-2xl p-10">
        <h1 className="text-4xl font-extrabold text-center text-indigo-700">
          Driver Facial Analysis System
        </h1>

        <p className="text-center text-gray-600 mt-3 mb-8">
          Detect driver drowsiness and risk level using facial analysis
        </p>

        <UploadForm setToast={setToast} setResult={setResult} />

        <ResultCard result={result} />
      </div>
    </div>
  );
}

export default App;
