const ResultCard = ({ result }) => {
  if (!result) return null;

  const riskColor =
    result.risk === "High"
      ? "text-red-600"
      : result.risk === "Medium"
      ? "text-yellow-500"
      : "text-green-600";

  return (
    <div className="bg-white p-6 rounded-xl shadow mt-6">
      <h2 className="text-xl font-bold mb-2">Result</h2>

      <p><b>Driver State:</b> {result.state}</p>
      <p className={riskColor}><b>Risk Level:</b> {result.risk}</p>
      <p><b>Confidence:</b> {(result.confidence * 100).toFixed(2)}%</p>
    </div>
  );
};

export default ResultCard;
