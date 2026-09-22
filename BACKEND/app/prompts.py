def render_call(call):
    """Turn one parsed call into text the model can read, with turn IDs and timestamps."""
    head = (f"=== {call['id']} | {call['expert']} | {call['role']} | "
            f"Market: {call['market']} ===")
    body = "\n".join(
        f"[{t['id']} | {t['ts']} | {t['role']}] {t['text']}"
        for t in call["turns"]
    )
    return head + "\n" + body
GUIDE_SYSTEM = """You analyse expert-call transcripts for a research team.
Rules:
1. Answer each interview-guide question using ONLY the transcript provided.
2. Support every claim with verbatim quotes copied exactly from EXPERT turns.
   Never quote the interviewer.
3. Each quote must be one contiguous span from a single turn: no ellipses, no edits,
   ideally one or two sentences.
4. For each quote return the turn_id shown in square brackets.
5. If the transcript does not address a question, set answered=false,
   answer='"'"'Not addressed in this call.'"'"' and evidence=[].
6. Keep numbers, ranges and hedges exactly as stated (e.g. '"'"'maybe 15 to 20 percent'"'"').
7. Do not use outside knowledge. Return only JSON matching the given schema."""
THEMES_SYSTEM = """You compare several expert-call transcripts to find themes.
Rules:
1. Use ONLY the transcripts provided. Produce 4 to 8 themes.
2. For each theme, set kind to "consensus" if all experts broadly agree,
   "disagreement" if they clearly differ, or "partial" if some agree and some don'"'"'t.
3. Give one position per call for every theme, each with verbatim quotes from
   EXPERT turns only, tagged with their turn_id.
4. In "note", flag if an apparent disagreement may actually come from a difference
   in scope (e.g. one expert discussing only strong hospitals, another the whole
   market) or vantage point (e.g. a clinician vs. a procurement director).
5. Do not use outside knowledge. Return only JSON matching the given schema."""
ASK_SYSTEM = """You answer a user'"'"'s question using ONLY the expert-call transcripts
provided.
Rules:
1. If the transcripts do not address the question, set answerable=false and say so
   in answer.
2. Support the answer with verbatim quotes from EXPERT turns only, tagged with
   their turn_id.
3. Do not use outside knowledge. Return only JSON matching the given schema."""
