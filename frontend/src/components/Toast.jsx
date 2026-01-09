function Toast({ message }) {
  if (!message) return null;

  return (
    <div className="fixed top-5 right-5 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg z-50">
      {message}
    </div>
  );
}

export default Toast;
