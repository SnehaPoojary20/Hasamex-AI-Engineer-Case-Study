import { useEffect, useState } from "react";
import { getThemes } from "../api";
import QuoteBlock from "./QuoteBlock";
import "./ThemesTab.css";

const KIND_LABEL = {
  consensus: "Consensus",
  disagreement: "Disagreement",
  partial: "Partial agreement",
};

function ThemesTab() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getThemes().then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="tt-error">Could not load themes: {error}</p>;
  if (!data) return <p className="tt-loading">Comparing calls…</p>;

  return (
    <div>
      {data.themes.map((t, i) => (
        <section key={i} className={`tt-theme tt-${t.kind}`}>
          <div className="tt-head">
            <h2>{t.title}</h2>
            <span className="tt-badge">{KIND_LABEL[t.kind] ?? t.kind}</span>
          </div>
          <p className="tt-summary">{t.summary}</p>
          <div className="tt-positions">
            {t.positions.map((p) => (
              <div key={p.call_id} className="tt-position">
                <div className="tt-call-label">{p.call_id}</div>
                <p className="tt-stance">{p.stance}</p>
                <QuoteBlock evidence={p.evidence} />
              </div>
            ))}
          </div>
          {t.note && <p className="tt-note">{t.note}</p>}
        </section>
      ))}
    </div>
  );
}

export default ThemesTab;