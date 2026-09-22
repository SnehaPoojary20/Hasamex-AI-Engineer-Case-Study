import { useEffect, useState } from "react";
import {getGuide} from "../api";
import QuoteBlock from "../Quote Block/quoteBlock.jsx";
import "./guideTab.css";

function GuideTab (){

  const[data, setData] = useState(null);
  const[error, setError]=useState(null);

  useEffect(()=>{
    getGuide()
    .then(setData)
    .catch((e)=>setError(e.message));
  },[]);

  if(error){
    return <p className="gt-error">Could not load guide answers: {error}</p>;
  }

 if (!data) {
  return <p className="gt-loading">Reading the transcripts…</p>;
}

 const verifiedPct =
  data.quote_stats.proposed > 0
    ? Math.round(
        (data.quote_stats.verified / data.quote_stats.proposed) * 100
      )
    : 0;


    return (
    <div>
      {data.questions.map((q) => (
        <section key={q.id} className="gt-question">
          <h2>{q.text}</h2>
          <div className="gt-grid">
            {data.calls.map((callId) => (
              <div key={callId} className="gt-cell">
                <div className="gt-call-label">{callId}</div>
                <p className="gt-answer">{data.cells[q.id][callId].answer}</p>
                <QuoteBlock evidence={data.cells[q.id][callId].evidence} />
              </div>
            ))}
          </div>
        </section>
      ))}
      <p className="gt-stats">
        Quotes verified: {data.quote_stats.verified} of {data.quote_stats.proposed} ({verifiedPct}%)
      </p>
    </div>
  );
}


export default GuideTab;