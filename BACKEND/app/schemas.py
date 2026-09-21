from typing import Literal
from pydantic import BaseModel


# make a form called RawEvidence
class RawEvidence(BaseModel):
    #the address of one speaker turn (Call 1, turn 5)
    turn_id:str  
    quote:str


# API output, after verification
class Evidence(BaseModel):
    call_id:str
    turn_id:str
    timestamp:str
    speaker:str
    quote:str       # exact substring of the source turn


# AI's answer to one interview question
class RawGuideAnswer(BaseModel):
    question_id:str
    answered: bool
    answer : str
    evidence: list[RawEvidence]


# the whole batch of answers
class RawGuideResult(BaseModel):
    answers: list[RawGuideAnswer]


# what one expert thinks about one theme
class RawPosition(BaseModel):
    call_id:str
    stance:str
    evidence: list[RawEvidence]


# one topic compared across experts
class RawTheme(BaseModel):
    title:str
    kind: Literal["consensus", "disagreement", "partial"]
    summary:str
    positions: list[RawPosition]
    note:str


# the folder for all themes
class RawThemeReport(BaseModel):
    themes: list[RawTheme]


# the AI's answer to a free-form user question
class RawAsk(BaseModel):
    answerable:bool
    answer: str
    evidence: list[RawEvidence]



 
# MODELS needed
# code checks each quote against the transcript
# good quotes become Evidence (timestamp and speaker added)
# bad quotes are thrown away
# the final result goes to the screen