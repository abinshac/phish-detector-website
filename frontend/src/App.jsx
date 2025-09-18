import { useState } from "react";
import { Mail } from "lucide-react";

export default function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          subject: "",
          body: message,
          urls: [],
        }),
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "❌ Could not connect to backend" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center">
      {/* top spacing */}
      <div className="w-full max-w-6xl px-8 pt-8">
        <h1 className="neon-title mx-auto text-center">
          DQCS_5 DATAQUEST 2.0
        </h1>
      </div>

      <div className="flex-1 w-full flex flex-col items-center justify-start pt-8 px-6">
        <Mail className="w-28 h-28 mb-8 text-white" strokeWidth={1.6} />

        <h2 className="text-2xl md:text-3xl font-semibold mb-8">
          Is This Mail Safe?
        </h2>

        <form
          onSubmit={handleSubmit}
          className="w-full max-w-4xl flex items-center gap-4"
        >
          <input
            type="text"
            placeholder="Paste email text here..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="flex-1 h-14 rounded-full px-8 bg-white text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-300 transition"
          />

          <button
            type="submit"
            disabled={loading}
            className="h-14 px-6 rounded-full bg-white text-black font-semibold hover:bg-gray-100 transition"
          >
            {loading ? "Analysing..." : "Analyse"}
          </button>
        </form>

        {/* Result area (keeps same style but hidden until a result exists) */}
        {result && (
          <div className="mt-10 w-full max-w-4xl p-6 rounded-xl bg-transparent text-left">
            {result.error ? (
              <p className="text-red-400">{result.error}</p>
            ) : (
              <>
                <p className="text-lg">
                  <strong>Score:</strong> {result.score?.toFixed(3)}
                </p>
                <p className="text-lg mt-2">
                  <strong>Prediction:</strong>{" "}
                  {result.label === 1 ? (
                    <span className="text-red-400 font-bold">Suspicious 🚨</span>
                  ) : (
                    <span className="text-green-400 font-bold">Safe ✅</span>
                  )}
                </p>

                {result.reasons?.length > 0 && (
                  <div className="mt-3">
                    <strong>Reasons:</strong>
                    <ul className="list-disc ml-6 text-gray-300">
                      {result.reasons.map((r, i) => (
                        <li key={i}>{r}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>

      {/* small bottom padding */}
      <div className="h-12" />
    </div>
  );
}
