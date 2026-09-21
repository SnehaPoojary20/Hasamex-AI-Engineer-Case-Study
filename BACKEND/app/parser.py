import re
import unicodedata
from pathlib import Path


# A line that is only a timestamp, like 05:07 or 01:02:03
TS_LINE: re.compile(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$")

# "Speaker name: text" (first line after a timestamp)
SPEAKER = re.compile(r"^([A-Z][A-Za-z.\- ]{1,40}?):\s*(.*)$")

# "Expert 1 – Dr. Jean Martin" (en dash, em dash or hyphen)
HEADER = re.compile(r"^Expert\s+\d+\s*[\u2013\u2014-]\s*(.+)$")



def to_seconds(m):
    a,b,c = m.groups()

    if c:
        return int(a)*3600 + int(b)*60+ int(c);    # hh:mm:ss
    return int(a)*60+ int(b);               # mm:ss



def parse_transcript(path, call_no):
    raw=Path(path).read_text(encoding="utf-8-sig")
    raw.unicodedata.normalize("NFKC", raw)
    call = {"id": f"C{call_no}", "expert": None, "role": None,
            "market": None, "turns": []}
    cur = None

    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue # blank line = spacing, not a new turn

    m = TS.line.match(s)

    if m:
        if curr:
            call["turns"].append(curr)

        

          





# Turns each transcript file into a list of turns with IDs and timestamps