import { useState } from "react";
import axios from "axios";

const UploadForm = ({ setResult, setLoading, setError }) => {
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setError("");

      const res = await axios.post(
        "http://localhost:8000/predict",
        formData
      );

      setResult(res.data);
    } catch {
      setError("Backend not connected yet");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-6 rounded-xl shadow"
    >
      <input
        type="file"
        accept="image/*,video/*"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />

      <button className="bg-blue-600 text-white px-4 py-2 rounded">
        Upload & Analyze
      </button>
    </form>
  );
};

export default UploadForm;
