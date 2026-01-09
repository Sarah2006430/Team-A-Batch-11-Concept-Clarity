import { useState } from "react";

function UploadForm({ setToast, setResult }) {
  const [file, setFile] = useState(null);

  const handleUpload = () => {
    if (!file) {
      setToast("Please select an image or video file");
      setTimeout(() => setToast(""), 3000);
      return;
    }

    setToast("Analyzing driver state...");
    setTimeout(() => setToast(""), 3000);

    // Dummy result (until backend is connected)
    setTimeout(() => {
      setResult({
        state: "Drowsy",
        risk: "High",
      });
    }, 1500);
  };

  return (
    <div className="border-2 border-dashed border-indigo-400 rounded-lg p-6 text-center">
      <input
        type="file"
        accept="image/*,video/*"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />

      <br />

      <button
        onClick={handleUpload}
        className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-2 rounded-lg font-semibold transition"
      >
        Upload & Analyze
      </button>
    </div>
  );
}

export default UploadForm;
