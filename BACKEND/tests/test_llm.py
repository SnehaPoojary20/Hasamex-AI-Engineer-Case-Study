import pytest
from app.llm import call_llm_json
from app.prompts import ASK_SYSTEM, GUIDE_SYSTEM
from app.schemas import RawAsk, RawGuideResult

TRANSCRIPT = "[C1-T001|00:18|expert] Adoption is growing steadily in larger hospitals."
@pytest.mark.llm



def test_ask_answers_when_transcript_covers_it():
    user = f"TRANSCRIPT: {TRANSCRIPT}\n\nQUESTION: Is adoption growing?"
    r = call_llm_json(ASK_SYSTEM, user, RawAsk)
    assert r.answerable is True
    assert len(r.evidence) >= 1
    assert r.evidence[0].turn_id == "C1-T001"
@pytest.mark.llm



def test_ask_says_unanswerable_when_transcript_does_not_cover_it():
    user = f"TRANSCRIPT: {TRANSCRIPT}\n\nQUESTION: What color is the sky?"
    r = call_llm_json(ASK_SYSTEM, user, RawAsk)
    assert r.answerable is False
@pytest.mark.llm



def test_guide_answer_has_correct_question_id():
    guide_text = "Q1: Is adoption growing?"
    user = f"[C1-T001|00:18|expert] Adoption is growing steadily.\n\nINTERVIEW GUIDE:\n{guide_text}"
    r = call_llm_json(GUIDE_SYSTEM, user, RawGuideResult)
    assert len(r.answers) == 1
    assert r.answers[0].question_id == "Q1"
    assert r.answers[0].answered is True
