import { useState, useEffect } from "react";
import axios from "axios";

function UploadForm({ setToast, setResult }) {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    setFile(f);

    if (f) {
      setPreviewUrl(URL.createObjectURL(f));
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setToast("Please select an image or video file");
      setTimeout(() => setToast(""), 3000);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const isVideo = file.type.startsWith("video");
      const endpoint = isVideo
        ? "http://127.0.0.1:8000/predict/video"
        : "http://127.0.0.1:8000/predict/image";

      setToast("Uploading...");
      const res = await axios.post(endpoint, formData);
      const data = res.data;

      console.log("BACKEND RESPONSE:", data);

      setToast("Analyzing driver state...");
      setTimeout(() => setToast(""), 2000);

      setResult({
        prediction: data.prediction,
        raw_probability:
          data.raw_probability ?? data.confidence ?? data.average_probability,
      });
    } catch (err) {
      setToast("Backend error");
      setTimeout(() => setToast(""), 3000);
    }
  };

  return (
    <div className="border-2 border-dashed border-indigo-400 rounded-lg p-6 text-center">
      <input
        type="file"
        accept="image/*,video/*"
        onChange={handleFileChange}
        className="mb-4"
      />

      {previewUrl && (
        <div className="mb-4 flex justify-center">
          {file?.type.startsWith("video") ? (
            <video
              src={previewUrl}
              controls
              className="w-64 rounded-lg border shadow"
            />
          ) : (
            <img
              src={previewUrl}
              alt="Preview"
              className="w-40 h-40 object-cover rounded-lg border shadow"
            />
          )}
        </div>
      )}

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
