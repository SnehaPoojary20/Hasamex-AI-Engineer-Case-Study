from typing import Literal
from pydantic import BaseModel, ConfigDict
class StrictModel(BaseModel):
    """Base for every schema. Forbids extra fields, which is what makes
    Groq'"'"'s strict JSON mode accept the schema."""
    model_config = ConfigDict(extra="forbid")
class RawEvidence(StrictModel):          # LLM output
    turn_id: str
    quote: str
class Evidence(StrictModel):             # API output, after verification
    call_id: str
    turn_id: str
    timestamp: str
    speaker: str
    quote: str                            # exact substring of the source turn
class RawGuideAnswer(StrictModel):
    question_id: str
    answered: bool
    answer: str
    evidence: list[RawEvidence]
class RawGuideResult(StrictModel):
    answers: list[RawGuideAnswer]
class RawPosition(StrictModel):
    call_id: str
    stance: str
    evidence: list[RawEvidence]
class RawTheme(StrictModel):
    title: str
    kind: Literal["consensus", "disagreement", "partial"]
    summary: str
    positions: list[RawPosition]
    note: str                             # scope or vantage-point differences
class RawThemeReport(StrictModel):
    themes: list[RawTheme]
class RawAsk(StrictModel):
    answerable: bool
    answer: str
    evidence: list[RawEvidence]
