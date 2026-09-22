import re
from app.schemas import Evidence
def snap_quote(quote: str, text: str, min_words: int = 2):
    """
    Look for `quote` inside `text`, ignoring punctuation and spacing
    differences. Returns the exact matching text from `text` if found
    (so casing/punctuation come from the real transcript), or None.
    """
    words = re.findall(r"\w+", quote)
    if len(words) < min_words:
        return None
    pattern = r"\W+".join(re.escape(w) for w in words)
    m = re.search(pattern, text, flags=re.IGNORECASE)
    return m.group(0) if m else None
def verify_evidence(ev, turns_by_id, all_turns):
    """
    Take one RawEvidence (turn_id + quote, as the LLM proposed it).
    Return an Evidence with call_id/timestamp/speaker added, or None
    if the quote cannot be found anywhere reliable.
    """
    turn = turns_by_id.get(ev.turn_id)
    exact = snap_quote(ev.quote, turn["text"]) if turn else None
    if exact is None:
        # the model may have cited the wrong turn_id; search other
        # expert turns as a fallback, requiring a longer match so we
        # don'"'"'t accidentally match on a short common phrase
        for t in all_turns:
            if t["role"] == "expert":
                exact = snap_quote(ev.quote, t["text"], min_words=6)
                if exact:
                    turn = t
                    break
    if exact is None or turn["role"] != "expert":
        return None
    return Evidence(
        call_id=turn["call_id"],
        turn_id=turn["id"],
        timestamp=turn["ts"],
        speaker=turn["speaker"],
        quote=exact,
    )
