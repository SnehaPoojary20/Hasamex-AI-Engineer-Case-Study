from pathlib import Path
from app.parser import parse_transcript, validate



def load_calls():
    files = sorted(Path("data/raw").glob("*.txt"))
    return [parse_transcript(f, i + 1) for i, f in enumerate(files)]



def test_all_three_transcripts_parse():
    calls = load_calls()
    assert len(calls) == 3
    for c in calls:
        validate(c)
        assert len(c["turns"]) == 14



def test_expert_names_and_markets():
    calls = load_calls()
    assert calls[0]["expert"] == "Dr. Jean Martin"
    assert calls[0]["market"] == "France"
    assert calls[1]["expert"] == "Anna Keller"
    assert calls[2]["market"] == "United Kingdom"



def test_known_quote_and_timestamp():
    calls = load_calls()
    t = calls[0]["turns"][11]
    assert t["id"] == "C1-T011"
    assert t["ts"] == "05:07"
    assert t["role"] == "expert"
    assert "15 to 20 percent" in t["text"]



def test_interviewer_turns_are_tagged():
    calls = load_calls()
    assert calls[0]["turns"][0]["role"] == "interviewer"
