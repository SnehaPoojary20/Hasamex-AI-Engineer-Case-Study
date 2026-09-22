import os
import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.parser import parse_transcript, validate
from app.analysis import build_guide, build_themes, answer_question


BASE = Path(__file__).resolve().parent.parent
RAW_DIR = BASE / "data" / "raw"
PROCESSED_DIR = BASE / "data" / "processed"

STATE = {}


def load_calls():
    files = sorted(RAW_DIR.glob("*.txt"))

    calls = [
        parse_transcript(f, i + 1)
        for i, f in enumerate(files)
    ]

    for c in calls:
        validate(c)

    return calls


def cached(name, builder):
    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    path = PROCESSED_DIR / name

    if path.exists():
        return json.loads(
            path.read_text(encoding="utf-8")
        )

    result = builder()

    path.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8"
    )

    return result


def rebuild_state():
    calls = load_calls()

    turns = [
        t
        for c in calls
        for t in c["turns"]
    ]

    STATE["calls"] = calls
    STATE["turns"] = turns
    STATE["by_id"] = {
        t["id"]: t
        for t in turns
    }

    guide = json.loads(
        (
            BASE / "data" / "guide.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    STATE["guide"] = cached(
        "guide_result.json",
        lambda: build_guide(
            calls,
            guide,
            STATE["by_id"],
            turns
        ),
    )

    STATE["themes"] = cached(
        "themes_result.json",
        lambda: build_themes(
            calls,
            STATE["by_id"],
            turns
        ),
    )


@asynccontextmanager
async def lifespan(app):
    rebuild_state()
    yield


# Create the FastAPI application
app = FastAPI(
    title="Expert Call Analyzer",
    lifespan=lifespan
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://hasamex-ai-engineer-case-study.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskBody(BaseModel):
    question: str


@app.get("/api/calls")
def get_calls():
    return [
        {
            "id": c["id"],
            "expert": c["expert"],
            "role": c["role"],
            "market": c["market"]
        }
        for c in STATE["calls"]
    ]


@app.get("/api/guide")
def get_guide():
    return STATE["guide"]


@app.get("/api/themes")
def get_themes():
    return STATE["themes"]


@app.post("/api/ask")
def post_ask(body: AskBody):

    if not body.question.strip():
        raise HTTPException(
            400,
            "Question cannot be empty"
        )

    return answer_question(
        body.question,
        STATE
    )


@app.get("/api/turn/{turn_id}")
def get_turn(
    turn_id: str,
    context: int = 2
):

    turn = STATE["by_id"].get(turn_id)

    if not turn:
        raise HTTPException(
            404,
            "Unknown turn id"
        )

    same_call = [
        t
        for t in STATE["turns"]
        if t["call_id"] == turn["call_id"]
    ]

    i = same_call.index(turn)

    window = same_call[
        max(0, i - context):
        i + context + 1
    ]

    return {
        "focus": turn,
        "context": window
    }


@app.post("/api/upload")
async def upload_transcript(
    file: UploadFile = File(...)
):
    """
    Lets a reviewer upload a transcript.

    The uploaded .txt file is saved into data/raw,
    cached guide/themes results are cleared,
    and the application state is rebuilt.
    """

    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            400,
            "Only .txt transcripts are supported"
        )

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    dest = RAW_DIR / file.filename

    dest.write_bytes(
        await file.read()
    )

    for name in (
        "guide_result.json",
        "themes_result.json"
    ):

        p = PROCESSED_DIR / name

        if p.exists():
            p.unlink()

    rebuild_state()

    return {
        "saved": file.filename,
        "calls": get_calls()
    }