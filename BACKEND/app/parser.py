import re
import unicodedata
from pathlib import Path
TS_LINE = re.compile(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$")
SPEAKER = re.compile(r"^([A-Z][A-Za-z.\- ]{1,40}?):\s*(.*)$")
HEADER = re.compile(r"^Expert\s+\d+\s*[\u2013\u2014-]\s*(.+)$")
def to_seconds(m):
    a, b, c = m.groups()
    if c:
        return int(a) * 3600 + int(b) * 60 + int(c)
    return int(a) * 60 + int(b)
def parse_transcript(path, call_no):
    raw = Path(path).read_text(encoding="utf-8-sig")
    raw = unicodedata.normalize("NFKC", raw)
    call = {"id": f"C{call_no}", "expert": None, "role": None,
            "market": None, "turns": []}
    cur = None
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        m = TS_LINE.match(s)
        if m:
            if cur:
                call["turns"].append(cur)
            cur = {"ts": s, "seconds": to_seconds(m), "speaker": None, "text": ""}
            continue
        if cur is None:
            h = HEADER.match(s)
            if h:
                call["expert"] = h.group(1).strip()
            elif s.lower().startswith("role:"):
                call["role"] = s.split(":", 1)[1].strip()
            elif s.lower().startswith("market:"):
                call["market"] = s.split(":", 1)[1].strip()
            continue
        if cur["speaker"] is None:
            sm = SPEAKER.match(s)
            if not sm:
                raise ValueError(f"{path}: no 'Speaker: text' after {cur['ts']}: {s!r}")
            cur["speaker"] = sm.group(1).strip()
            cur["text"] = sm.group(2).strip()
        else:
            cur["text"] += " " + s
    if cur:
        call["turns"].append(cur)
    for i, t in enumerate(call["turns"]):
        t["id"] = f"{call['id']}-T{i:03d}"
        t["call_id"] = call["id"]
        t["role"] = "interviewer" if t["speaker"].lower() == "interviewer" else "expert"
        t["text"] = re.sub(r"\s+", " ", t["text"]).strip()
    return call
def validate(call):
    prev = -1
    for t in call["turns"]:
        assert t["seconds"] > prev, f"timestamps not increasing at {t['id']}"
        assert t["speaker"] and t["text"], f"empty turn {t['id']}"
        prev = t["seconds"]
    print(call["id"], call["expert"], "-", len(call["turns"]), "turns")
