from app.verify import snap_quote, verify_evidence
from app.schemas import RawEvidence
TURN = {
    "id": "C1-T005", "call_id": "C1", "ts": "02:18", "seconds": 138,
    "speaker": "Dr. Martin", "role": "expert",
    "text": "Very important. The clinical argument may get surgeons interested.",
}
TURNS_BY_ID = {"C1-T005": TURN}
ALL_TURNS = [TURN]
def test_real_quote_is_found():
    result = snap_quote("the clinical argument may get surgeons interested", TURN["text"])
    assert result is not None
def test_fake_quote_is_rejected():
    result = snap_quote("the doctors hated it completely", TURN["text"])
    assert result is None
def test_verify_evidence_fills_in_timestamp_and_speaker():
    ev = RawEvidence(turn_id="C1-T005", quote="the clinical argument may get surgeons interested")
    result = verify_evidence(ev, TURNS_BY_ID, ALL_TURNS)
    assert result is not None
    assert result.timestamp == "02:18"
    assert result.speaker == "Dr. Martin"
    assert result.call_id == "C1"
def test_verify_evidence_drops_unfindable_quote():
    ev = RawEvidence(turn_id="C1-T005", quote="something never said in this turn")
    result = verify_evidence(ev, TURNS_BY_ID, ALL_TURNS)
    assert result is None
