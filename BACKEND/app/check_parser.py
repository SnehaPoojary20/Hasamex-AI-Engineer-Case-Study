from pathlib import Path
from app.parser import parse_transcript,validate

files = sorted(Path("data").glob("*.txt"))
calls = [parse_transcript(f, i + 1) for i, f in enumerate(files)]
for c in calls:
    validate(c)
    print("   ", c["role"], "|", c["market"])

t = calls[0]["turns"][11]
print(t["id"], t["ts"], t["speaker"], t["role"])
print(t["text"])