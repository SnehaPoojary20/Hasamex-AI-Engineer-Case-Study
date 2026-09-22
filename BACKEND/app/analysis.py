from app.llm import call_llm_json
from app.prompts import render_call, GUIDE_SYSTEM, THEMES_SYSTEM, ASK_SYSTEM
from app.schemas import RawGuideResult, RawThemeReport, RawAsk
from app.verify import verify_evidence

def _verify_list(raw_evidence_list, turns_by_id, all_turns, stats):
    good = []
    for ev in raw_evidence_list:
        stats["proposed"] += 1
        v = verify_evidence(ev, turns_by_id, all_turns)
        if v:
            stats["verified"] += 1
            good.append(v.model_dump())
    return good

def build_guide(calls, guide, turns_by_id, all_turns):
    """
    For each call, ask the model to answer every guide question at once.
    Returns {"questions", "calls", "cells", "quote_stats"} ready for the
    /api/guide endpoint and the Guide Answers tab.
    """
    questions_text = "\n".join(f"{q['id']}: {q['text']}" for q in guide)
    cells = {}
    stats = {"proposed": 0, "verified": 0}
    for call in calls:
        user = f"{render_call(call)}\n\nINTERVIEW GUIDE:\n{questions_text}"
        raw = call_llm_json(GUIDE_SYSTEM, user, RawGuideResult)
        for answer in raw.answers:
            good = _verify_list(answer.evidence, turns_by_id, all_turns, stats)
            cells.setdefault(answer.question_id, {})[call["id"]] = {
                "answered": answer.answered and bool(good),
                "answer": answer.answer,
                "evidence": good,
            }
    return {
        "questions": guide,
        "calls": [c["id"] for c in calls],
        "cells": cells,
        "quote_stats": stats,
    }
def build_themes(calls, turns_by_id, all_turns):
    """
    Send all calls together and ask for cross-call themes. Returns
    {"themes", "quote_stats"} ready for the /api/themes endpoint.
    """
    all_calls_text = "\n\n".join(render_call(c) for c in calls)
    stats = {"proposed": 0, "verified": 0}
    raw = call_llm_json(THEMES_SYSTEM, all_calls_text, RawThemeReport)
    themes = []
    for theme in raw.themes:
        positions = []
        for pos in theme.positions:
            good = _verify_list(pos.evidence, turns_by_id, all_turns, stats)
            positions.append({
                "call_id": pos.call_id,
                "stance": pos.stance,
                "evidence": good,
            })
        themes.append({
            "title": theme.title,
            "kind": theme.kind,
            "summary": theme.summary,
            "positions": positions,
            "note": theme.note,
        })
    return {"themes": themes, "quote_stats": stats}
def answer_question(question, state):
    """
    Answer a free-form question across all calls in `state`.
    `state` must have "calls", "turns" (flat list) and "by_id".
    Returns a dict ready for the /api/ask endpoint.
    """
    all_calls_text = "\n\n".join(render_call(c) for c in state["calls"])
    user = f"{all_calls_text}\n\nQUESTION: {question}"
    raw = call_llm_json(ASK_SYSTEM, user, RawAsk)
    stats = {"proposed": 0, "verified": 0}
    good = _verify_list(raw.evidence, state["by_id"], state["turns"], stats)
    return {
        "answerable": raw.answerable and (bool(good) or not raw.evidence),
        "answer": raw.answer,
        "evidence": good,
        "quote_stats": stats,
    }
