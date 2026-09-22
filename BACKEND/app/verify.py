import re 
from .schemas import Evidence



def snap_quote(quote:str, text:str, min_words:int=2):
    words = re.findall(r"\w+", quote)

    if len(words) < min_words:
        return None

    pattern = r"\W+".join(re.escape(w) for w in words)
    m = re.search(pattern, text,flags=re.IGNORECASE)
    return m.group(0) if m else None



def verify_evidence(ev, turns_by_id, all_turns):
    """Return Evidence or None (None = not verifiable, drop it)."""

    turn= turns_by_id.get(ev.turn_id)
    exact = snap_quote(ev.quote, turn["text"]) if turn else None

    if exact is None:
        for t in all_turns:
            if t["role"]== "expert":
                exact = snap_quote(ev.quote, t["text"], min_words=6)

                if exact:
                    turn = t
                    break

    if exact is None and turn["role"] != "expert":
        return None

    return Evidence(call_id=turn["call_id"], turn_id=turn["id"], timestamp=turn["ts"],
    speaker=turn["speaker"], quote=exact)


    

# Checks each quote against the transcript and builds the Evidence objects