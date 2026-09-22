import "./QuoteBlock.css";

function QuoteBlock ({evidence}){

    if(! evidence || evidence.length==0){
        return <p className="qb-empty">Not addressed in this call.</p>;
    }

    return (
    <div className="qb-list">
      {evidence.map((e, i) => (
        <blockquote key={i} className="qb-quote">
          <p>&ldquo;{e.quote}&rdquo;</p>
          <footer>
            <span className="qb-speaker">{e.speaker}</span>
            <span className="qb-time">{e.timestamp}</span>
          </footer>
        </blockquote>
      ))}
    </div>
    );
}


export default QuoteBlock;