import { useState } from "react";
import { askQuestion } from "../api";
import QuoteBlock from "../Quote Block/quoteBlock.jsx";
import "./AskTab.css";

function AskTab() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function submit(e) {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    try {
      setResult(await askQuestion(question));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="at-wrap">
      <form onSubmit={submit} className="at-form">
        <input
          className="at-input"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask across all three calls…"
        />
        <button className="at-submit" type="submit" disabled={loading}>
          {loading ? "Asking…" : "Ask"}
        </button>
      </form>

      {error && <p className="at-error">{error}</p>}

      {result && (
        <div className="at-result">
          {!result.answerable && (
            <p className="at-unanswerable">The calls do not address this question.</p>
          )}
          <p className="at-answer">{result.answer}</p>
          <QuoteBlock evidence={result.evidence} />
        </div>
      )}
    </div>
  );
}


export default AskTab;