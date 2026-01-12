function ResultCard({ result }) {
  if (!result) {
    return (
      <p className="text-center text-gray-500 mt-6">
        Result will be shown here
      </p>
    );
  }

  const prob = result.raw_probability;

  let risk = "Low";
  if (prob >= 0.7) risk = "High";
  else if (prob >= 0.4) risk = "Medium";

  const riskColor =
    risk === "High"
      ? "text-red-600"
      : risk === "Medium"
      ? "text-yellow-600"
      : "text-green-600";

  return (
    <div className="mt-8 p-6 border rounded-xl bg-gray-50 text-center">
      <h2 className="text-xl font-bold text-gray-700 mb-2">
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

        <p className="text-lg">
          Risk Level:{" "}
          <span className={`font-bold ${riskColor}`}>
            {risk}
          </span>
        </p>
      </div>
    </div>
  );
}

export default ResultCard;
