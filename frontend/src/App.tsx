import { useState, type FormEvent } from "react";
import "./App.css";

const API_BASE = "http://localhost:8000";

interface AskResponse {
  mp4: string;
  session: string;
  attempts: number;
}

export default function App() {
  const [concept, setConcept] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AskResponse | null>(null);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!concept.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ concept }),
      });
      if (!response.ok) {
        const detail = await response.text();
        throw new Error(`HTTP ${response.status}: ${detail.slice(0, 400)}`);
      }
      const data = (await response.json()) as AskResponse;
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header>
        <h1>MathMentor</h1>
        <p className="tagline">
          On-device AI math tutor. Type a concept, get a Manim animation.
        </p>
      </header>

      <form onSubmit={submit}>
        <textarea
          value={concept}
          onChange={(e) => setConcept(e.target.value)}
          placeholder="e.g. Visualise that the derivative of sin(x) is cos(x), with a moving tangent line."
          rows={4}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !concept.trim()}>
          {loading ? "Generating…" : "Generate"}
        </button>
      </form>

      {loading && (
        <p className="status">
          Calling Gemma 4 and rendering Manim. This can take 1–5 minutes.
        </p>
      )}

      {error && (
        <pre className="error" aria-live="polite">
          {error}
        </pre>
      )}

      {result && (
        <section className="result">
          <video
            key={result.mp4}
            src={`${API_BASE}${result.mp4}`}
            controls
            autoPlay
            loop
          />
          <p className="meta">
            Session <code>{result.session}</code> ·{" "}
            {result.attempts} attempt{result.attempts === 1 ? "" : "s"}
          </p>
        </section>
      )}
    </main>
  );
}
