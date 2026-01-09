function ResultCard({ result }) {
  if (!result) {
    return (
      <p className="text-center text-gray-500 mt-6">
        Result will be shown here
      </p>
    );
  }

  const riskColor =
    result.risk === "High"
      ? "text-red-600"
      : result.risk === "Medium"
      ? "text-yellow-600"
      : "text-green-600";

  return (
    <div className="mt-8 p-6 border rounded-xl bg-gray-50 text-center">
      <h2 className="text-xl font-bold text-gray-700 mb-2">
        Analysis Result
      </h2>

      <p className="text-lg">
        Driver State:{" "}
        <span className="font-semibold text-indigo-600">
          {result.state}
        </span>
      </p>

      <p className="text-lg mt-2">
        Risk Level:{" "}
        <span className={`font-bold ${riskColor}`}>
          {result.risk}
        </span>
      </p>
    </div>
  );
}

export default ResultCard;
