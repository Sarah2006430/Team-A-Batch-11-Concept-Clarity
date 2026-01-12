const ResultCard = ({ result }) => {
  if (!result) return null;

  const prob = result.raw_probability;

  return (
    <div className="mt-8 border rounded-xl p-6 shadow bg-gray-50">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        Analysis Result
      </h2>

      <div className="space-y-4">
        <p className="text-lg">
          <span className="font-semibold text-gray-700">
            Driver State:
          </span>{" "}
          <span className="text-indigo-700 font-bold">
            {result.prediction}
          </span>
        </p>

        <p className="text-lg">
          <span className="font-semibold text-gray-700">
            Raw Model Output:
          </span>{" "}
          {(prob * 100).toFixed(2)}%
        </p>
      </div>
    </div>
  );
};

export default ResultCard;
