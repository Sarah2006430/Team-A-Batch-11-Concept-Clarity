const ResultCard = ({ result }) => {
  if (!result) return null;

  const riskStyles = {
    High: "bg-red-100 text-red-700 border-red-300",
    Medium: "bg-yellow-100 text-yellow-700 border-yellow-300",
    Low: "bg-green-100 text-green-700 border-green-300",
  };

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
            {result.state}
          </span>
        </p>

        <div
          className={`inline-block px-4 py-2 rounded-full font-semibold border ${
            riskStyles[result.risk]
          }`}
        >
          Risk Level: {result.risk}
        </div>

        <p className="text-lg">
          <span className="font-semibold text-gray-700">
            Confidence:
          </span>{" "}
          {(result.confidence * 100).toFixed(2)}%
        </p>
      </div>
    </div>
  );
};

export default ResultCard;
