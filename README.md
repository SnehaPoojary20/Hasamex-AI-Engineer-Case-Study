# Expert Call Analyzer

A small app built for the Hasamex AI Engineer case study. It reads three expert-call
transcripts about robotic surgery adoption in Europe, answers the interview guide for
each expert, pulls out exact quotes with timestamps, compares the three experts to find
themes and disagreements, and lets a reviewer ask their own questions across all three
calls.

## What it does

1. **Reads the three transcripts** (France, Germany, United Kingdom) and breaks each one
   into individual turns — who spoke, what they said, and when.
2. **Answers the six interview-guide questions** for each expert, with a supporting quote
   and timestamp for every answer.
3. **Finds themes across all three experts** — where they agree, where they disagree, and
   why a disagreement might just be two experts describing different parts of the market.
4. **Lets you ask your own question** and get an answer with citations, or a clear "not
   covered" if the transcripts do not address it.
5. **Every single quote is checked against the real transcript text** before it is shown.
   If a quote cannot be found, it is dropped rather than shown as if it were real.

## How to run it

### Backend

```powershell
cd BACKEND
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a file called `.env` in `BACKEND` with:

GROQ_API_KEY=your-key-here
LLM_MODEL=openai/gpt-oss-120b


A free key with no card required is available at console.groq.com.

Place the three transcript files in `data\raw\` (already included), then start the
server:

```powershell
uvicorn app.main:app --reload --port 8000
```

The first start calls the AI to build the guide answers and the themes, and saves the
result to `data\processed\`. This takes a short while and uses a small amount of API
usage. Every start after that is instant, because it reads from the saved files. Delete
the files in `data\processed\` if you want it to build fresh answers again.

Open `http://127.0.0.1:8000/docs` to try every part of the API by hand.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open the address it prints (normally `http://localhost:5173`). The backend must already
be running for the screen to show anything.

## How it is built

transcripts (.txt)
| parser.py turns the text into a list of turns, each with an id and a timestamp
v
turns.json
|
+--> guide answers -> AI call -> quote checker -> saved as JSON
+--> themes -> AI call -> quote checker -> saved as JSON
+--> ask a question -> AI call -> quote checker -> sent back straight away
v
FastAPI serves this as an API, and the React screen shows it in three tabs


**Why it is built this way, in plain words:**

- **The AI never writes a timestamp itself.** It only points at a turn id, like
  `C1-T011`. My own code looks up the real timestamp for that turn. This means a
  timestamp shown on screen can never be one the AI made up.
- **Every quote is checked against the real transcript text before it is shown.** If the
  AI proposes a quote and that exact quote cannot be found in the transcript, it is
  thrown away rather than shown as real. This is the main way the app avoids making
  things up.
- **The AI has to answer in a fixed, checked format.** Rather than writing a free-form
  paragraph, the AI fills in a strict form (built with Pydantic) that always has the same
  fields. If it tries to add an extra field or leave one out, the request fails and is
  retried, so the app never has to guess at what an answer means.
- **All three transcripts are given to the AI directly, in full, in one request.**
  Each transcript is short — about 400 words — so all three together are still small.
  This keeps things simple for three calls. Section "how this would scale" below explains
  what changes for a much larger number of calls.
- **Results are calculated once and saved**, rather than being recalculated on every
  screen load. This makes the app fast and repeatable to demo, and only spends API usage
  when something actually needs to change.

## Tests

Tests are split into two kinds, and the split matters:

- **Fast tests** need no internet and no AI, so they run in under a second and cost
  nothing. Run these constantly while working.
- **AI tests** make a real call to the AI, so they cost a small amount and take a few
  seconds. Run these occasionally, on purpose.

```powershell
python -m pytest -m "not llm" -v      # fast tests only
python -m pytest -m llm -v            # tests that call the AI
python -m pytest -v                   # everything
```

**`tests/test_parser.py`** — checks that the parser correctly turns all three raw
transcript files into turns. Confirms each transcript produces the right number of
turns, the right expert name and market are read from the header, a specific known
quote is found at the right timestamp, and the interviewer's turns are correctly told
apart from the expert's.

**`tests/test_verify.py`** — checks the part of the app that decides whether a quote is
real. Confirms a quote that really is in the transcript is found, a quote that was never
said is rejected, and that when a quote is confirmed, the correct timestamp and speaker
are attached to it.

**`tests/test_llm.py`** — checks that the AI genuinely answers from the transcript, not
from its own knowledge. Confirms it correctly answers a question the transcript does
cover, correctly says "not covered" for a question about something never mentioned (for
example, asking about the weather), and correctly labels its answer with the right
guide-question id.

**`tests/test_api.py`** — checks the actual API a browser would call. Confirms that
asking for a specific turn returns the right text and timestamp along with two turns of
context either side, that asking for a turn id that does not exist returns a proper "not
found" response instead of crashing, and that the context window defaults to two turns
either side when not specified.

## What the app found (for reference)

Running the guide and themes against the three transcripts, every proposed quote was
successfully verified against the transcript text (20 out of 20 for the guide answers,
15 out of 15 for the themes, 0 dropped). Two genuine differences between the experts came
up:

- **Growth rate over the next 3–5 years:** Dr. Martin (France) expects 15–20% more
  procedures a year, but only in stronger centres. Anna Keller (Germany) expects high
  single digits to low double digits across the whole market. Dr. Carter (UK) expects
  above 15% in some areas. The app correctly notes this may not be a true disagreement —
  each expert may be describing a different slice of their market rather than genuinely
  disagreeing about the same thing.
- **Purchase decision timeline:** Martin says 6–12 months, Keller says 9–18 months,
  Carter says 6–9 months if funding is already available. The app notes Keller's longer
  estimate may come from needing more stakeholders to align before a purchase is
  approved.

## Limitations

- Timestamps mark the **start** of a turn, not the exact position of a sentence within a
  longer turn.
- Checking that a quote exists word-for-word in the transcript is not the same as
  checking that the quote truly supports the claim next to it. A wrong pairing of a real
  quote with the wrong claim would not be caught by the current checker.
- Built and tested against three short transcripts (about 400 words each). See below for
  what would need to change at a larger scale.
- The free AI tier used here has request limits, and the specific AI model available for
  free may change over time, since providers periodically retire older models.

## How this would scale from 3 transcripts to 30+

- Right now, each transcript is small enough to send to the AI in full inside one
  request. With many more transcripts, or much longer ones, they would no longer all fit
  in a single request together.
- The fix is to first turn each transcript into smaller, searchable pieces (a process
  called "chunking"), and turn those pieces into number-based representations of their
  meaning (called "embeddings") using a library such as sentence-transformers. When a
  question comes in, the app would search for the most relevant pieces first, and send
  only those to the AI, rather than every transcript in full.
- Themes and guide answers would also be worked out in two steps instead of one: first,
  each transcript would be summarised on its own; then a second pass would compare those
  summaries to each other, instead of comparing every full transcript at once.
- The quote-checking approach used here would stay exactly the same at any scale, since
  it works on one quote against one transcript at a time and does not depend on how many
  transcripts there are in total.
