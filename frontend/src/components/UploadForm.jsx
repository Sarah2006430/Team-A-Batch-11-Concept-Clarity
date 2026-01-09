import { useState, useEffect } from "react";
import axios from "axios";

const UploadForm = ({ setResult, setLoading, setError }) => {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [fileType, setFileType] = useState(null);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    if (selectedFile) {
      setPreviewUrl(URL.createObjectURL(selectedFile));
      setFileType(selectedFile.type.startsWith("video") ? "video" : "image");
    }
  };

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

      const isVideo = file.type.startsWith("video");
      const endpoint = isVideo
        ? "http://127.0.0.1:8000/predict/video"
        : "http://127.0.0.1:8000/predict/image";

      const res = await axios.post(endpoint, formData);
      const data = res.data;

      const confidence = data.confidence ?? data.average_confidence;

      setResult({
        state: data.prediction,
        confidence,
        risk: confidence > 0.7 ? "High" : confidence > 0.4 ? "Medium" : "Low",
      });
    } catch (err) {
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
        onChange={handleFileChange}
        className="mb-4 w-full file:bg-indigo-600 file:text-white file:px-4 file:py-2 file:rounded-lg file:border-0 file:cursor-pointer"
      />

      {previewUrl && (
        <div className="mb-4 flex justify-center">
          {fileType === "image" ? (
            <img
              src={previewUrl}
              alt="Preview"
              className="w-40 h-40 object-cover rounded-lg border shadow"
            />
          ) : (
            <video
              src={previewUrl}
              controls
              className="w-64 rounded-lg border shadow"
            />
          )}
        </div>
      )}

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
