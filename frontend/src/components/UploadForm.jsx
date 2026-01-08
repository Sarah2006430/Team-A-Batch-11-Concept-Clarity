import { useState } from "react";
import axios from "axios";

const UploadForm = ({ setResult, setLoading, setError }) => {
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select an image or video file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const res = await axios.post(
        "http://localhost:8000/predict",
        formData
      );

      setResult(res.data);
    } catch {
      setError("Backend not connected or error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="border-2 border-dashed border-indigo-400 rounded-xl p-6 bg-indigo-50 text-center"
    >
      <p className="text-gray-700 font-medium mb-3">
        Upload Driver Image / Video
      </p>

      <input
        type="file"
        accept="image/*,video/*"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4 w-full file:bg-indigo-600 file:text-white file:px-4 file:py-2 file:rounded-lg file:border-0 file:cursor-pointer"
      />

      <button
        type="submit"
        className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-2 rounded-lg transition-all duration-300 shadow-md"
      >
        Upload & Analyze
      </button>
    </form>
  );
};

export default UploadForm;
